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

    class Config:
        schema_extra = {
            "example": {
                "type": "connectivity",
                "updated_at": "2023-02-10T08:41:01.118Z",
                "content": "Behive 'Hello World' lost connectivity 5 minutes ago"
            }
        }


class GroupedEventOut(BaseModel):
    updated_at: datetime
    value: int
    messages: list[EventOut]

    class Config:
        schema_extra = {
            "example": {
                "updated_at": "2023-02-10",
                "value": 1,
                "messages": [
                    EventOut.Config.schema_extra["example"]
                ]
            }
        }


class EventsOut(BaseModel):
    behive_id: str
    values: list[GroupedEventOut]

    class Config:
        schema_extra = {
            "example": {
                "behive_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "values": [
                    GroupedEventOut.Config.schema_extra["example"]
                ]
            }
        }


class CreateEventRecordModel(BaseModel):
    behive_id: str
    type: EventType | str
    updated_at: datetime
    content: str

    class Config:
        schema_extra = {
            "example": {
                "behive_id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                "type": "custom",
                "updated_at": "2023-02-10T08:41:01.118Z",
                "content": "My custom event message"
            }
        }
