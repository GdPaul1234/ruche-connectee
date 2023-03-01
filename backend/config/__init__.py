from pydantic import BaseSettings

import os

def get_env_path():
    environment = os.getenv('PYTHON_ENV', default='PRODUCTION')
    print(environment)

    match environment:
        case 'PRODUCTION':
            return 'env/prod.env'
        case _:
            return 'env/test.env'

class CommonSettings(BaseSettings):
    APP_NAME: str = "Super Hive - Hive"
    DEBUG_MODE: bool = False


class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000


class DatabaseSettings(BaseSettings):
    DB_URL: str
    DB_NAME: str


class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class Settings(CommonSettings, ServerSettings, DatabaseSettings, AuthSettings):
    class Config:
        env_file = get_env_path()


settings = Settings()
