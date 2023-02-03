
from typing import Any
import uuid

from pydantic import BaseModel, Field
from fastapi.encoders import jsonable_encoder


# adapted from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(BaseModel):
    id: str
    username: str
    email: str
    firstname: str
    lastname: str
    disabled: bool | None = None

    class Config:
        schema_extra = {
            "example": {
                 "id": "00010203-0405-0607-0809-0a0b0c0d0e0f",
                 "username": "roger123",
                 "firstname": "Roger",
                 "lastname": "Doe",
                 "email": "roger123@superhive.org",
                 "disabled": False
            }
        }


class UserInDB(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    hashed_password: str
    username: str
    email: str
    firstname: str
    lastname: str
    disabled: bool | None = None

    class Config:
        allow_population_by_field_name = True


class CreateUserModel(BaseModel):
    username: str
    email: str
    password: str
    firstname: str
    lastname: str

    class Config:
        schema_extra = {
            "example": {
                 "username": "roger123",
                 "email": "roger123@superhive.org",
                 "password": "ogisguhddhngcbv098%$",
                 "firstname": "Roger",
                 "lastname": "Doe"
            }
        }


def to_user_out(user: Any):
    return jsonable_encoder(User(id=str(user["_id"]),**user))
