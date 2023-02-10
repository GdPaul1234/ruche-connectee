from datetime import datetime
from typing import Any, Literal
import uuid

from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder


class SensorValue(BaseModel):
    updated_at: datetime = Field(default=datetime.utcnow())
    value: float
    unit: str


SensorType = Literal['temperature', 'humidity', 'weight', 'battery']


class SensorModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    type: SensorType
    behive_id: str
    owner_id: str
    values: list[SensorValue]

    class Config:
        allow_population_by_field_name = True


class SensorValueOut(BaseModel):
    updated_at: datetime
    value: float
    unit: str


class SensorOut(BaseModel):
    id: str
    behive_id: str
    values: list[SensorValueOut]


class CreateSensorRecordModel(BaseModel):
    updated_at: datetime
    value: float
    unit: str

    class Config:
        schema_extra = {
            "example": {
                "updated_at": "2023-02-10T08:41:01.118Z",
                "value": 25,
                "unit": "°C"
            }
        }

def to_sensor_out(sensor: Any):
    return jsonable_encoder(SensorOut(id=str(sensor["_id"]), **sensor))
