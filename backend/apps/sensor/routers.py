from fastapi import APIRouter, Depends, Body, Request
from fastapi.encoders import jsonable_encoder

from .models import SensorType, SensorOut, SensorValueOut, CreateSensorRecordModel, to_sensor_out

from apps.user.auth import User, get_current_active_user

router = APIRouter()


def get_sensors_db(request: Request):
    return request.app.mongodb["sensors"]

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
    sensor_record = jsonable_encoder(sensor_record.dict() | {"owner_id": current_user})

    new_record = await sensors_db.update_one({"type": sensor_type, "behive_id": behive_id, "owner_id": current_user.id}, {
        "$push": { "values": sensor_record }
    })
    created_record = await new_record.find_one({"_id": new_record.inserted_id})

    return SensorValueOut(**created_record)


@router.get("/behive/{behive_id}/{sensor_type}", response_description="Get behive sensor values by type", response_model=SensorOut)
async def list_sensor_records_by_type(
    *,
    current_user: User = Depends(get_current_active_user),
    sensor_type: SensorType,
    behive_id: str,
    request: Request
):
    sensors_db = get_sensors_db(request)
    sensor_value = await sensors_db.find_one({"type": sensor_type, "behive_id": behive_id, "owner_id": current_user.id})

    return SensorOut(**sensor_value)
