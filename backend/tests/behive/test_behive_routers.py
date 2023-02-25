import pytest
from httpx import AsyncClient

from main import app

class TestBehiveRouter:
    base_url = "http://localhost:8888/api/behives"

    @pytest.mark.anyio
    async def test_create_behive(self, token):
        async with AsyncClient(app=app, base_url=self.base_url, headers={"Authorization": f"Bearer ${token}"}) as ac:
            response = await ac.post("/", json={"name": "Ruche 1"})
            assert response.status_code == 201

            response_body = response.json()
            assert {"id", "name", "last_metrics"} <= response_body.keys()
            assert {"temperature", "humidity", "weight", "battery", "alert"} <= response_body.get("last_metrics").keys()
            assert response_body.get("name") == "Ruche 1"

    @pytest.mark.anyio
    async def test_get_all_user_behives(self, token, behive):
        async with AsyncClient(app=app, base_url=self.base_url, headers={"Authorization": f"Bearer ${token}"}) as ac:
            response = await ac.get("/")
            assert response.status_code == 200

            response_body = response.json()
            assert len(response_body) == 1
            assert response_body[0]["id"] == str(behive["_id"])
            assert response_body[0]["name"] == behive["name"]

    @pytest.mark.anyio
    async def test_get_behive(self, token, behive):
         async with AsyncClient(app=app, base_url=self.base_url, headers={"Authorization": f"Bearer ${token}"}) as ac:
            response = await ac.get(f"/{behive['_id']}")
            assert response.status_code == 200

            response_body = response.json()
            assert {"id", "name", "last_metrics"} <= response_body.keys()
            assert {"temperature", "humidity", "weight", "battery", "alert"} <= response_body.get("last_metrics").keys()
            assert response_body.get("id") == behive["_id"]
            assert response_body.get("name") == behive["name"]

    @pytest.mark.anyio
    async def test_update_behive_name(self, token, behive):
        async with AsyncClient(app=app, base_url=self.base_url, headers={"Authorization": f"Bearer ${token}"}) as ac:
            response = await ac.put(f"/{behive['_id']}", json={"name": "Ruche 1"})
            assert response.status_code == 200

            response_body = response.json()
            assert {"id", "name", "last_metrics"} <= response_body.keys()
            assert {"temperature", "humidity", "weight", "battery", "alert"} <= response_body.get("last_metrics").keys()
            assert response_body.get("id") == behive["_id"]
            assert response_body.get("name") == "Ruche 1"

    @pytest.mark.anyio
    async def test_delete_behive(self, token, behive):
         async with AsyncClient(app=app, base_url=self.base_url, headers={"Authorization": f"Bearer ${token}"}) as ac:
            response = await ac.put(f"/{behive['_id']}")
            assert response.status_code == 204
