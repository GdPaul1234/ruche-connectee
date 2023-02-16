from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

EventType = Literal['theft', 'connectivity', 'battery',
                    'disease', 'harvest', 'weather', 'maintenance']


class EventModel(BaseModel):
    behive_id: str
    owner_id: str
    type: EventType | str
    updated_at: datetime = Field(default=datetime.utcnow())
    content: str


class EventOut(BaseModel):
    type: EventType | str
    updated_at: datetime
    content: str


class GroupedEventOut(BaseModel):
    updated_at: datetime
    value: int
    messages: list[EventOut]


class EventsOut(BaseModel):
    behive_id: str
    values: list[GroupedEventOut]

    class Config:
        schema_extra = {
            "example": {
                "values": [
                    {
                        "updated_at": "2023-02-10T08:41:01.118Z",
                        "type": "connectivity",
                        "content": "Behive 'Hello World' lost connectivity 5 minutes ago"
                    }
                ]
            }
        }


class CreateEventRecordModel(BaseModel):
    behive_id: str
    type: EventType | str
    content: str

    class Config:
        schema_extra = {
            "example": {
                "behive_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "type": "custom",
                "content": "My custom event message"
            }
        }
