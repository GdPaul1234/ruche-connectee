from datetime import datetime, timezone
from typing import cast
from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .models import SensorType, SensorOut, SensorValueOut, CreateSensorRecordModel, to_sensor_out

from apps.user.auth import User, get_current_active_user

router = APIRouter()


def get_sensors_db(request: Request):
    return request.app.mongodb["sensors"]


def get_behive_db(request: Request):
    return request.app.mongodb["behives"]


def get_mongo_db_client(request: Request):
    return request.app.mongodb_client


@router.post("/behive/{behive_id}/{sensor_type}", response_description="Add new sensor type record to behive", response_model=SensorValueOut)
async def create_sensor_record(
    *,
    current_user: User = Depends(get_current_active_user), # TODO: authorize only balance user
    sensor_type: SensorType,
    behive_id: str,
    sensor_record: CreateSensorRecordModel = Body(...),
    request: Request
):
    sensors_db = get_sensors_db(request)

    if await get_behive_db(request).find_one({ "_id": behive_id }, { "owner_id": 1 }) != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    sensor_record = jsonable_encoder(sensor_record.dict() | {"owner_id": current_user.id})

    async with await get_mongo_db_client(request).start_session() as s:
        async with s.start_transaction():
            update_result = await sensors_db.update_one(
                {"type": sensor_type, "behive_id": behive_id, "owner_id": current_user.id},
                {"$push": {"values": sensor_record}},
                session=s
            )

            serialized_updated_at = datetime.fromisoformat(cast(dict, sensor_record)["updated_at"]).astimezone(timezone.utc).isoformat()

            if update_result.modified_count == 1 and (
                updated_sensor := await sensors_db.find_one({
                    "owner_id": current_user.id,
                    "values.updated_at": serialized_updated_at
                }, session=s)
            ) is not None:
                return SensorValueOut(**updated_sensor["values"][0])

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor not found")


@router.get("/behive/{behive_id}/{sensor_type}", response_description="Get behive sensor values by type", response_model=SensorOut)
async def list_sensor_records_by_type(
    *,
    current_user: User = Depends(get_current_active_user),
    sensor_type: SensorType,
    behive_id: str,
    from_date: datetime = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0),
    to_date: datetime = datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999),
    request: Request
):
    sensors_db = get_sensors_db(request)

    if from_date > to_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inconsistent date range")

    async for doc in sensors_db.aggregate([
        {"$match": {"type": sensor_type, "behive_id": behive_id, "owner_id": current_user.id}},
        {
            "$project": {
                "_id": 1,
                "behive_id": 1,
                "values": {
                    "$filter": {
                        "input": "$values",
                        "as": "value",
                        "cond": {
                            "$and": [
                                {"$gte": ["$$value.updated_at", from_date.astimezone(timezone.utc).isoformat()]},
                                {"$lt": ["$$value.updated_at", to_date.astimezone(timezone.utc).isoformat()]}
                            ]
                        }
                    }
                }
            }
        },
        { "$limit": 1 }
    ]):
        return to_sensor_out(doc)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


