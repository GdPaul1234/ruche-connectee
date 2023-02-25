from dataclasses import dataclass
from typing import Any, Optional
import uuid

from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder


@dataclass
class BehiveMetric:
    value: str | float
    unit: str | None


class BehiveMetrics(BaseModel):
    temperature_indoor: BehiveMetric
    temperature_outdoor: BehiveMetric
    humidity: BehiveMetric
    weight: BehiveMetric
    battery: BehiveMetric
    alert: BehiveMetric


class BehiveModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    owner_id: str
    name: str
    last_metrics: BehiveMetrics

    class Config:
        allow_population_by_field_name = True


class BehiveOut(BaseModel):
    id: str
    name: str
    last_metrics: BehiveMetrics

    class Config:
        schema_extra = {
            "example": {
                "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "name": "Ruche 1",
                "last_metrics": {
                    "temperature": { "value": 15, "unit": '°C' },
                    "humidity": { "value": 70, "unit": '%' },
                    "weight": { "value": 50, "unit": 'kg' },
                    "battery": { "value": 20, "unit": '%' },
                    "alert": { "value": 2, "unit": None }
                }
            }
        }


class CreateBehiveModel(BaseModel):
    name: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Ruche 1"
            }
        }


class UpdateBehiveModel(CreateBehiveModel):
    pass

def to_behive_out(behive: Any):
    return jsonable_encoder(BehiveOut(id=str(behive["_id"]), **behive))
