from datetime import datetime, timedelta
import os

from faker import Faker
from faker.providers import person, internet, python
from fastapi.testclient import TestClient
import pytest

from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

from apps.user.models import UserInDB
from apps.beehive.models import BehiveMetrics, BehiveMetric, BehiveModel
from apps.sensor.models import SensorModel, SensorValue

from apps.user.auth import get_password_hash

from config import settings
from main import app

fake = Faker()
fake.add_provider(person)
fake.add_provider(internet)
fake.add_provider(python)


@pytest.fixture
def anyio_backend():
    return 'asyncio'


###############################################################################
###                                   APP                                   ###
###############################################################################

@pytest.fixture
def mongodb_client():
    print(os.getenv('PYTHON_ENV'))

    return AsyncIOMotorClient(settings.DB_URL, replicaSet="rs0")


@pytest.fixture
def mongodb(mongodb_client):
    return mongodb_client[settings.DB_NAME]


###############################################################################
###                                  USER                                   ###
###############################################################################


def get_userindb_payload(*, hashed_password, username, firstname, lastname, email, disabled):
    return UserInDB(
        hashed_password=hashed_password,
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        disabled=disabled
    ).dict(exclude={"id"}) | {"_id": ObjectId()}


@pytest.fixture
@pytest.mark.anyio
async def user(mongodb):
    userindb_payload = get_userindb_payload(
        hashed_password=get_password_hash("password"),
        username=fake.user_name(),
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        email=fake.email(),
        disabled=None
    )
    inserted_user = await mongodb.users.insert_one(userindb_payload)

    yield await mongodb.users.find_one({"_id": inserted_user.inserted_id})

    await mongodb.users.delete_one({"_id":  inserted_user.inserted_id})


@pytest.fixture()
@pytest.mark.anyio
async def token(user):
    print('token user_id', user)

    with TestClient(app=app, base_url="http://localhost:8888") as client:
        response = client.post("/api/token", data={"username": user["username"], "password": "password"})
        return response.json()["access_token"]


###############################################################################
###                                 BEHIVE                                  ###
###############################################################################


def fake_last_metrics():
    return BehiveMetrics(
        temperature_indoor=BehiveMetric(value=fake.pyfloat(left_digits=2, right_digits=1, min_value=20, max_value=40), unit="°C"),
        temperature_outdoor=BehiveMetric(value=fake.pyfloat(left_digits=2, right_digits=1, min_value=-10, max_value=25), unit="°C"),
        humidity_indoor=BehiveMetric(value=fake.pyfloat(left_digits=2, right_digits=1, min_value=40, max_value=80), unit="%"),
        humidity_outdoor=BehiveMetric(value=fake.pyfloat(left_digits=2, right_digits=1, min_value=40, max_value=80), unit="%"),
        weight=BehiveMetric(value=fake.pyfloat(left_digits=2, right_digits=1, min_value=20, max_value=100), unit="kg"),
        battery=BehiveMetric(value=fake.pyfloat(left_digits=2, right_digits=1, min_value=20, max_value=100), unit="%"),
        alert=BehiveMetric(value=fake.pyint(max_value=3), unit=None)
    )


def get_behive_with_payload(*, owner_id, name):
    return BehiveModel(
        name=name,
        owner_id=owner_id,
        last_metrics=fake_last_metrics()
    ).dict(exclude={"id"}) | {"_id": ObjectId()}


@pytest.fixture
@pytest.mark.anyio
async def behive(mongodb, user):

    behive_payload = get_behive_with_payload(owner_id=str(user["_id"]), name=f"Ruche #{fake.user_name()}")
    inserted_behive = await mongodb.behives.insert_one(behive_payload)

    yield await mongodb.behives.find_one({"_id": inserted_behive.inserted_id})

    await mongodb.behives.delete_one({"_id":  inserted_behive.inserted_id})



###############################################################################
###                                SENSORS                                  ###
###############################################################################

def fake_sensor_values(
    *,
    start=datetime.today() - timedelta(days=7),
    end=datetime.today(),
    min_value: float,
    max_value: float,
    unit: str
):
    return [
        SensorValue(
            updated_at=datetime.fromtimestamp(updated_at_timestamp),
            value=fake.pyfloat(left_digits=2, right_digits=1, min_value=min_value, max_value=max_value),
            unit=unit
        )
        for updated_at_timestamp in range(
            int(start.timestamp()),
            int((end + timedelta(seconds=1)).timestamp()),
            int(timedelta(minutes=30).total_seconds())
        )
    ]

@pytest.fixture
@pytest.mark.anyio
async def behive_sensors(mongodb, behive, user):
    behive_id = str(behive["_id"])
    owner_id = str(user["_id"])

    all_sensors = [
        SensorModel(type='temperature_indoor', behive_id=behive_id, owner_id=owner_id, values=fake_sensor_values(min_value=20, max_value=40, unit="°C")).dict(exclude={"id"}) | {"_id": ObjectId()},
        SensorModel(type='temperature_outdoor', behive_id=behive_id, owner_id=owner_id, values=fake_sensor_values(min_value=-10, max_value=25, unit="°C")).dict(exclude={"id"}) | {"_id": ObjectId()},
        SensorModel(type='humidity_indoor', behive_id=behive_id, owner_id=owner_id, values=fake_sensor_values(min_value=40, max_value=80, unit="%")).dict(exclude={"id"}) | {"_id": ObjectId()},
        SensorModel(type='humidity_outdoor', behive_id=behive_id, owner_id=owner_id, values=fake_sensor_values(min_value=40, max_value=80, unit="%")).dict(exclude={"id"}) | {"_id": ObjectId()},
        SensorModel(type='weight', behive_id=behive_id, owner_id=owner_id, values=fake_sensor_values(min_value=20, max_value=100, unit="kg")).dict(exclude={"id"}) | {"_id": ObjectId()},
        SensorModel(type='battery', behive_id=behive_id, owner_id=owner_id, values=fake_sensor_values(min_value=20, max_value=100, unit="%")).dict(exclude={"id"}) | {"_id": ObjectId()},
    ]

    inserted_sensors = await mongodb.sensors.insert_many(all_sensors)

    yield all_sensors

    await mongodb.sensors.delete_many({"_id": {"$in": inserted_sensors.inserted_ids}})

