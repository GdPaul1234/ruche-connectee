from datetime import datetime, timezone
import itertools
from typing import cast
from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .models import EventType, EventOut, EventsOut, CreateEventRecordModel, GroupedEventOut

from apps.user.auth import User, get_current_active_user

router = APIRouter()


def get_events_db(request: Request):
    return request.app.mongodb["events"]


def get_behive_db(request: Request):
    return request.app.mongodb["behives"]


def get_mongo_db_client(request: Request):
    return request.app.mongodb_client


@router.post("/", response_description="Add new behive event", response_model=EventOut)
async def create_event_record(
    *,
    current_user: User = Depends(get_current_active_user),
    event_record: CreateEventRecordModel = Body(...),
    request: Request
):
    events_db = get_events_db(request)

    if await get_behive_db(request).find_one({"_id": event_record.behive_id}, {"owner_id": 1}) != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    event_record = jsonable_encoder(
        event_record.dict() | {"owner_id": current_user.id})

    async with await get_mongo_db_client(request).start_session() as s:
        async with s.start_transaction():
            new_event = await events_db.insert_one(event_record, session=s)
            created_event = await events_db.find_one({"_id": new_event.inserted_id}, session=s)

            return EventOut(**created_event)


@router.get("/behive/{behive_id}/", response_description="Get behive events", response_model=EventsOut)
async def list_events(
    *,
    current_user: User = Depends(get_current_active_user),
    behive_id: str,
    from_date: datetime = datetime.today().replace(
        day=1, hour=0, minute=0, second=0, microsecond=0),
    to_date: datetime = datetime.today().replace(
        hour=23, minute=59, second=59, microsecond=999999),
    request: Request
) -> EventsOut:
    events_db = get_events_db(request)

    if from_date > to_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inconsistent date range")

    events = await events_db.find({
        "behive_id": behive_id,
        "owner_id": current_user.id,
        "updated_at": {
            "$gte": from_date.astimezone(timezone.utc).isoformat(),
            "$lt": to_date.astimezone(timezone.utc).isoformat()
        }
    }).to_list(length=100)

    grouped_events = itertools.groupby(
        events, lambda e: e["updated_at"].split("T")[0])

    return EventsOut(
        behive_id=behive_id,
        values=[
            GroupedEventOut(
                updated_at=datetime.fromisoformat(day),
                value=len(event_list := list(events)),  # NOSONAR
                messages=[EventOut(**event) for event in event_list]
            ) for day, events in grouped_events
        ]
    )
