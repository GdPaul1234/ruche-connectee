from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings

from apps.beehive.routers import router as behive_router
from apps.sensor.routers import router as sensor_router
from apps.event.routers import router as event_router
from apps.user.user_router import router as user_router
from apps.user.token_router import router as token_router

app = FastAPI()

# source: https://www.mongodb.com/developer/languages/python/farm-stack-fastapi-react-mongodb/


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL, replicaSet="rs0")
    app.mongodb = app.mongodb_client[settings.DB_NAME]


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(user_router, tags=["users"], prefix='/api')
app.include_router(token_router, tags=["tokens"], prefix='/api')
app.include_router(behive_router, tags=["behives"], prefix="/api/behives")
app.include_router(sensor_router, tags=["sensors"], prefix="/api/sensors")
app.include_router(event_router, tags=["events"], prefix="/api/events")

origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


def run_server():
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )


if __name__ == "__main__":
    run_server()
