from datetime import datetime, timedelta

from fastapi import Depends, Request, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt

from config import settings
from .models import UserInDB, User, TokenData


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def get_user(db, username: str):
    if (user := await db.find_one({"username": username})) is not None:
        return UserInDB(_id=str(user["_id"]), **{k: user[k] for k in set(user.keys()) - {"_id"}})


async def authenticate_user(user_db, username: str, password: str):
    user = await get_user(user_db, username)

    if not user or not verify_password(password, user.hashed_password):
        return False

    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        if (username := payload.get("sub")) is None:
            raise credentials_exception
        else:
            token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    if (user := await get_user(request.app.mongodb["users"], username=token_data.username)) is None:
        raise credentials_exception

    return User(**user.dict())


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user
