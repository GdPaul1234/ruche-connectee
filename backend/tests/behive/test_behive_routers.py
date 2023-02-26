from fastapi.testclient import TestClient
import pytest

from main import app

class TestBehiveRouter:
    base_url = "http://localhost:8888"

    @pytest.mark.anyio
    async def test_create_behive(self, token):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.post("/api/behives", json={"name": "Ruche 1"}, headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 201

        response_body = response.json()
        assert {"id", "name", "last_metrics"} <= response_body.keys()
        assert {"temperature_indoor", "temperature_outdoor", "humidity", "weight", "battery", "alert"} <= response_body.get("last_metrics").keys()
        assert response_body.get("name") == "Ruche 1"

        # delete created behive
        with TestClient(app=app, base_url=self.base_url) as client:
            client.delete(f"/api/behives/{response_body['id']}", headers={"Authorization": f"Bearer ${token}"})


    @pytest.mark.anyio
    async def test_get_all_user_behives(self, token, behive):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get("/api/behives", headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 200

        response_body = response.json()
        assert len(response_body) == 1
        assert response_body[0]["id"] == str(behive["_id"])
        assert response_body[0]["name"] == behive["name"]

    @pytest.mark.anyio
    async def test_get_behive(self, token, behive):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get(f"/api/behives/{behive['_id']}", headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 200

        response_body = response.json()
        assert {"id", "name", "last_metrics"} <= response_body.keys()
        assert {"temperature_indoor", "temperature_outdoor", "humidity", "weight", "battery", "alert"} <= response_body.get("last_metrics").keys()
        assert response_body.get("id") == str(behive["_id"])
        assert response_body.get("name") == behive["name"]

    @pytest.mark.anyio
    async def test_update_behive_name(self, token, behive):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.put(f"/api/behives/{behive['_id']}", json={"name": "Ruche 1"}, headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 200

        response_body = response.json()
        assert {"id", "name", "last_metrics"} <= response_body.keys()
        assert {"temperature_indoor", "temperature_outdoor", "humidity", "weight", "battery", "alert"} <= response_body.get("last_metrics").keys()
        assert response_body.get("id") == str(behive["_id"])
        assert response_body.get("name") == "Ruche 1"

    @pytest.mark.anyio
    async def test_delete_behive(self, token, behive):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.delete(f"/api/behives/{str(behive['_id'])}", headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 204
