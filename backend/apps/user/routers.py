from datetime import timedelta

from fastapi import Depends, APIRouter, Body, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from .auth import get_password_hash, get_current_active_user, authenticate_user, create_access_token
from .models import User, Token, CreateUserModel, to_user_out

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    if not (user := await authenticate_user(request.app.mongodb["users"], form_data.username, form_data.password)):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=User)
async def read_users_me(*, current_user: User = Depends(get_current_active_user)):
    return current_user


@router.post("/users", response_description="Add new behive", response_model=User)
async def create_user(request: Request, user: CreateUserModel = Body(...)):
    user = jsonable_encoder(user.dict(exclude={"password"}) | { "hashed_password": get_password_hash(user.password) })

    new_user = await request.app.mongodb["users"].insert_one(user)
    created_user = await request.app.mongodb["users"].find_one({
        "_id": new_user.inserted_id
    })

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=to_user_out(created_user))


@router.delete("/users/me", response_description="Delete user")
async def delete_user(*, current_user: User = Depends(get_current_active_user), request: Request):
    delete_result = await request.app.db["users"].delete_one({"_id": current_user.id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})

    raise HTTPException(status_code=404, detail=f"User {id} not found")
