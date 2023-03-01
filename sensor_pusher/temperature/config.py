from typing import Literal
from pydantic import BaseModel, BaseSettings

class Credential(BaseModel):
    username: str
    password: str

class Settings(BaseSettings):
    endpoint: str
    fallback_endpoint: str
    behive_id: str

    sensor_pin: int
    sensor_location: Literal['indoor', 'outdoor']

    credential: Credential

