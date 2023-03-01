from pydantic import BaseModel, BaseSettings

class Credential(BaseModel):
    username: str
    password: str

class Settings(BaseSettings):
    endpoint: str
    fallback_endpoint: str
    behive_id: str

    sck_pin: int
    dt_pin: int
    ref_unit: int
    offset: int

    credential: Credential
