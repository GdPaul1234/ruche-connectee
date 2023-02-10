from fastapi import FastAPI
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

from apps.beehive.routers import router as behive_router
from apps.sensor.routers import router as sensor_router
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


app.include_router(user_router, tags=["users"])
app.include_router(token_router, tags=["tokens"])
app.include_router(behive_router, tags=["behives"], prefix="/behives")
app.include_router(sensor_router, tags=["sensors"], prefix="/sensors")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        port=settings.PORT,
    )
