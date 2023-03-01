from datetime import datetime, timedelta

from faker import Faker
from faker.providers import python
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import pytest

from apps.sensor.models import CreateSensorRecordModel
from main import app

fake = Faker()
fake.add_provider(python)


class TestSensorRouter:
    base_url = "http://localhost:8888"
    sensor_types = ["temperature_indoor", "temperature_outdoor", "humidity_indoor", "humidity_outdoor", "weight", "battery"]

    @pytest.mark.anyio
    @pytest.mark.parametrize("sensor_type", sensor_types)
    async def test_list_sensor_records_type(self, token, behive, behive_sensors, sensor_type):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get(f"/api/sensors/behive/{behive['_id']}/{sensor_type}", headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 200

        response_body = response.json()
        assert { "id", "behive_id", "values" } <= response_body.keys()
        assert response_body.get("behive_id") == str(behive["_id"])

        from_date = datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        to_date = datetime.today().replace(hour=23, minute=59, second=59, microsecond=999999)

        assert len(response_body["values"]) == (to_date - from_date).total_seconds() // 60 // 30 // 2
        assert { "updated_at", "value", "unit" } <= response_body["values"][0].keys()

    @pytest.mark.anyio
    @pytest.mark.parametrize("sensor_type", ["temperature_indoor"])
    async def test_list_sensor_records_type_incoherent_date_range(self, token, behive, behive_sensors, sensor_type):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get(
                f"/api/sensors/behive/{behive['_id']}/{sensor_type}",
                params={
                    "from_date": (datetime.today() - timedelta(days=4)).isoformat(),
                    "to_date": (datetime.today() - timedelta(days=5)).isoformat()
                },
                headers={"Authorization": f"Bearer ${token}"}
            )

        assert response.status_code == 400

        response_body = response.json()
        assert response_body.get("detail") == "Inconsistent date range"

    @pytest.mark.anyio
    @pytest.mark.parametrize("sensor_type", sensor_types)
    async def test_list_sensor_records_type_valid_date_range(self, token, behive, behive_sensors, sensor_type):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get(
                f"/api/sensors/behive/{behive['_id']}/{sensor_type}",
                params={
                    "from_date": (datetime.today() - timedelta(days=5)).isoformat(),
                    "to_date": (datetime.today() - timedelta(days=4)).isoformat()
                },
                headers={"Authorization": f"Bearer ${token}"}
            )

        assert response.status_code == 200

        response_body = response.json()
        assert { "id", "behive_id", "values" } <= response_body.keys()
        assert response_body.get("behive_id") == str(behive["_id"])

        assert len(response_body["values"]) == 48 # 1 event every 30 minutes for one day
        assert { "updated_at", "value", "unit" } <= response_body["values"][0].keys()

    @pytest.mark.anyio
    @pytest.mark.parametrize("sensor_type,payload", [
        ("temperature_indoor", CreateSensorRecordModel(updated_at=datetime.today(), value=fake.pyfloat(left_digits=2, right_digits=1, min_value=20, max_value=40), unit="°C")),
        ("temperature_outdoor", CreateSensorRecordModel(updated_at=datetime.today(), value=fake.pyfloat(left_digits=2, right_digits=1, min_value=-10, max_value=25), unit="°C")),
        ("humidity_indoor", CreateSensorRecordModel(updated_at=datetime.today(), value=fake.pyfloat(left_digits=2, right_digits=1, min_value=40, max_value=80), unit="%")),
        ("humidity_outdoor", CreateSensorRecordModel(updated_at=datetime.today(), value=fake.pyfloat(left_digits=2, right_digits=1, min_value=40, max_value=80), unit="%")),
        ("weight", CreateSensorRecordModel(updated_at=datetime.today(), value=fake.pyfloat(left_digits=2, right_digits=1, min_value=20, max_value=100), unit="kg")),
        ("battery", CreateSensorRecordModel(updated_at=datetime.today(), value=fake.pyfloat(left_digits=2, right_digits=1, min_value=20, max_value=100), unit="%")),
    ])
    async def test_create_sensor_record(self, token_behive, behive, behive_sensors, sensor_type, payload):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.post(
                f"/api/sensors/behive/{behive['_id']}/{sensor_type}",
                json=jsonable_encoder(payload.dict()),
                headers={"Authorization": f"Bearer ${token_behive}"}
            )

        assert response.status_code == 201

        response_body = response.json()
        assert { "updated_at", "value", "unit" } <= response_body.keys()
        print(response.json())
        assert response_body.get("value") == payload.value
        assert response_body.get("unit") == payload.unit

