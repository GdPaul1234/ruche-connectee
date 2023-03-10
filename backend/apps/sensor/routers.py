from datetime import datetime
from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pymongo import ReturnDocument
from bson import ObjectId, DatetimeMS

from .models import SensorType, SensorOut, SensorValueOut, CreateSensorRecordModel, to_sensor_out

from apps.beehive.actions import update_behive_sensor_last_value
from apps.user.auth import User, get_current_active_user

router = APIRouter()


def get_sensors_db(request: Request):
    return request.app.mongodb["sensors"]


def get_behives_db(request: Request):
    return request.app.mongodb["behives"]


def get_mongo_db_client(request: Request):
    return request.app.mongodb_client


@router.post("/behive/{behive_id}/{sensor_type}", response_description="Add new sensor type record to behive", status_code=status.HTTP_201_CREATED, response_model=SensorValueOut)
async def create_sensor_record(
    *,
    current_user: User = Depends(get_current_active_user), # TODO: authorize only balance user
    sensor_type: SensorType,
    behive_id: str,
    sensor_record: CreateSensorRecordModel = Body(...),
    request: Request
):
    sensors_db = get_sensors_db(request)
    behives_db = get_behives_db(request)

    # TODO: harden behive user disjonction
    # add signature...

    if current_user.username != f'behive_{behive_id}':
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    behive_owner_id = await behives_db.find_one({ "_id": ObjectId(behive_id) }, { "owner_id": 1 })
    owner_id = behive_owner_id["owner_id"]

    serialized_sensor_record = jsonable_encoder(sensor_record.dict(exclude={"updated_at"}) | {"owner_id": owner_id}) | { "updated_at": DatetimeMS(sensor_record.updated_at) }

    async with await get_mongo_db_client(request).start_session() as s:
        async with s.start_transaction():
            updated_sensor = await sensors_db.find_one_and_update(
                {"type": sensor_type, "behive_id": behive_id, "owner_id": owner_id},
                {"$push": {"values": serialized_sensor_record}},
                return_document=ReturnDocument.AFTER,
                session=s
            )

            if updated_sensor is not None:
                last_record = updated_sensor["values"][-1]
                await update_behive_sensor_last_value(behives_db, behive_id, sensor_type, last_record, s)
                return SensorValueOut(**last_record)

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
                                {"$gte": ["$$value.updated_at", from_date]},
                                {"$lt": ["$$value.updated_at", to_date]}
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


