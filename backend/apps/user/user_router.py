
from fastapi import Depends, APIRouter, Body, Request, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .auth import get_password_hash, get_current_active_user
from .models import User, CreateUserModel, to_user_out

router = APIRouter()

def get_users_db(request: Request):
    return request.app.mongodb["users"]


@router.get("/users/me/", response_description="Get user personnal informations", response_model=User)
async def read_users_me(*, current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/users", response_description="Create new user", status_code=status.HTTP_201_CREATED, response_model=User)
async def create_user(
    users_db = Depends(get_users_db),
    user: CreateUserModel = Body(...)
):
    user = jsonable_encoder(user.dict(exclude={"password"}) | { "hashed_password": get_password_hash(user.password) })

    new_user = await users_db.insert_one(user)
    created_user = await users_db.find_one({"_id": new_user.inserted_id})

    return to_user_out(created_user)


@router.delete("/users/me", response_description="Delete user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    *,
    current_user: User = Depends(get_current_active_user),
    users_db = Depends(get_users_db)
):
    delete_result = await users_db.delete_one({"_id": current_user.id})

    if delete_result.deleted_count == 1:
        return {}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")
