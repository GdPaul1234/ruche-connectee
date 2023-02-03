from datetime import timedelta

from fastapi import Depends, APIRouter, Request, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from config import settings
from .auth import authenticate_user, create_access_token
from .models import Token

router = APIRouter()

def get_users_db(request: Request):
    return request.app.mongodb["users"]


@router.post("/token", response_model=Token)
async def login_for_access_token(
    *,
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request
):
    users_db = get_users_db(request)

    if not (user := await authenticate_user(users_db, form_data.username, form_data.password)):
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

