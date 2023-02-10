from datetime import datetime, timezone
from typing import cast
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import APIRouter, Depends, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .models import SensorType, SensorOut, SensorValueOut, CreateSensorRecordModel, to_sensor_out

from apps.user.auth import User, get_current_active_user

router = APIRouter()


def get_sensors_db(request: Request):
    return request.app.mongodb["sensors"]


def get_mongo_db_client(request: Request):
    return request.app.mongodb_client


@router.post("/behive/{behive_id}/{sensor_type}", response_description="Add new sensor type record to behive", response_model=SensorValueOut)
async def create_sensor_record(
    *,
    current_user: User = Depends(get_current_active_user),
    sensor_type: SensorType,
    behive_id: str,
    sensor_record: CreateSensorRecordModel = Body(...),
    request: Request
):
    sensors_db = get_sensors_db(request)
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
                updated_sensor := await sensors_db.find_one({"owner_id": current_user.id, "values.updated_at": serialized_updated_at}, session=s)
            ) is not None:
                return SensorValueOut(**updated_sensor["values"][0])

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sensor not found")


@router.get("/behive/{behive_id}/{sensor_type}", response_description="Get behive sensor values by type", response_model=SensorOut)
async def list_sensor_records_by_type(
    *,
    current_user: User = Depends(get_current_active_user),
    sensor_type: SensorType,
    behive_id: str,
    request: Request
):
    sensors_db = get_sensors_db(request)
    sensor = await sensors_db.find_one({"type": sensor_type, "behive_id": behive_id, "owner_id": current_user.id})
    return to_sensor_out(sensor)
