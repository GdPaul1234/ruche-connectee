from fastapi.testclient import TestClient
import pytest

from main import app

class TestSensorRouter:
    base_url = "http://localhost:8888"

    @pytest.mark.anyio
    @pytest.mark.parametrize(
        "sensor_type",
        [
            "temperature_indoor",
            "temperature_outdoor",
            "humidity",
            "weight",
            "battery"
        ]
    )
    async def test_list_sensor_records_type(self, token, behive, behive_sensors, sensor_type):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get(f"/api/sensors/behive/{behive['_id']}/{sensor_type}", headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 200

        response_body = response.json()
        assert { "id", "behive_id", "values" } <= response_body.keys()
        assert response_body.get("behive_id") == str(behive["_id"])

        assert len(response_body["values"]) == 337
        assert { "updated_at", "value", "unit" } <= response_body["values"][0].keys()

