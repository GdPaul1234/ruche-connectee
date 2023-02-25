from datetime import timedelta
from faker import Faker
from faker.providers import person, internet, python
from motor.motor_asyncio import AsyncIOMotorClient
import pytest

from apps.user.models import UserInDB
from apps.beehive.models import BehiveMetrics
from apps.beehive.models import BehiveMetric, BehiveModel
from apps.sensor.models import SensorModel

from apps.user.auth import create_access_token

from config import settings

fake = Faker()
fake.add_providers(person)
fake.add_providers(internet)
fake.add_providers(python)


@pytest.fixture(autouse=True)
def mongodb_client():
    return AsyncIOMotorClient(settings.DB_URL, replicaSet="rs0")


@pytest.fixture(autouse=True)
def mongodb(mongodb_client):
    return mongodb_client[settings.DB_NAME]


def get_userindb_payload(
    *,
    hashed_password="$2b$12$5xOtPg/7ye1/7oEeOZkhM.HitMUGOWdFI5uBuhf9gzd8vNCJ3Avda",  # = password
    username=fake.user_name(),
    firstname=fake.first_name(),
    lastname=fake.last_name(),
    email=fake.email(),
    disabled=None
):
    return UserInDB(
        hashed_password=hashed_password,
        username=username,
        firstname=firstname,
        lastname=lastname,
        email=email,
        disabled=disabled
    )


@pytest.fixture
@pytest.mark.anyio
async def user(mongodb):
    userindb_payload = get_userindb_payload().dict()
    user = await mongodb.users.insert_one(userindb_payload)

    yield user

    await mongodb.users.delete_one({"_id":  user.inserted_id})


@pytest.fixture
def token(user):
    return create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def fake_last_metrics():
    return BehiveMetrics(
        temperature_indoor=BehiveMetric(value=fake.pyfloat(
            left_digits=2, right_digits=1, min_value=20, max_value=40), unit="°C"),
        temperature_outdoor=BehiveMetric(value=fake.pyfloat(
            left_digits=2, right_digits=1, min_value=-10, max_value=25), unit="°C"),
        humidity=BehiveMetric(value=fake.pyfloat(
            left_digits=2, right_digits=1, min_value=40, max_value=80), unit="%"),
        weight=BehiveMetric(value=fake.pyfloat(
            left_digits=2, right_digits=1, min_value=0, max_value=100), unit="kg"),
        battery=BehiveMetric(value=fake.pyfloat(
            left_digits=2, right_digits=1, min_value=0, max_value=100), unit="%"),
        alert=BehiveMetric(value=fake.pyint(max_value=3), unit=None)
    )


def get_behive_with_payload(
    *,
    owner_id: str,
    name=f"Ruche #{fake.user_name()}"
):
    return BehiveModel(name=name, owner_id=owner_id, last_metrics=fake_last_metrics())


@pytest.fixture
@pytest.mark.anyio
async def behive(mongodb, user):
    behive_payload = get_behive_with_payload(owner_id=str(user.id)).dict()
    behive = await mongodb.behives.insert_one(behive_payload)

    yield behive

    await mongodb.behives.delete_one({"_id":  behive.inserted_id})


@pytest.fixture
@pytest.mark.anyio
async def behive_sensors(mongodb, behive, user):
    all_sensors = [
        SensorModel(type='temperature_indoor', behive_id=str(
            behive.id), owner_id=str(user.id), values=[]).dict(),
        SensorModel(type='temperature_outdoor', behive_id=str(
            behive.id), owner_id=str(user.id), values=[]).dict(),
        SensorModel(type='humidity', behive_id=str(behive.id),
                    owner_id=str(user.id), values=[]).dict(),
        SensorModel(type='weight', behive_id=str(behive.id),
                    owner_id=str(user.id), values=[]).dict(),
        SensorModel(type='battery', behive_id=str(behive.id),
                    owner_id=str(user.id), values=[]).dict(),
    ]

    inserted_sensors = await mongodb.sensors.insert_many(all_sensors)

    yield all_sensors

    await mongodb.sensors.delete_many({"_id": inserted_sensors.inserted_ids})
