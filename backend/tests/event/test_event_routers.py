from datetime import datetime, timedelta

from faker import Faker
from faker.providers import python
from fastapi.testclient import TestClient
from fastapi.encoders import jsonable_encoder
import pytest

from apps.event.models import CreateEventRecordModel
from main import app

class TestEventRouter:
    base_url = "http://localhost:8888"

    @pytest.mark.anyio
    async def test_list_event_records_type(self, token, behive, events):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.get(f"/api/events/behive/{behive['_id']}", headers={"Authorization": f"Bearer ${token}"})

        assert response.status_code == 200

        response_body = response.json()

        # TODO: check response


    @pytest.mark.anyio
    async def test_create_event_record(self, token_behive, behive):
        with TestClient(app=app, base_url=self.base_url) as client:
            response = client.post(
                f"/api/events",
                json=jsonable_encoder(CreateEventRecordModel(
                    behive_id=str(behive["_id"]),
                    type="battery",
                    updated_at=datetime.today(),
                    content="My event content"
                )),
                headers={"Authorization": f"Bearer ${token_behive}"}
            )

        assert response.status_code == 201

        response_body = response.json()

        assert { "type", "content", "updated_at" } <= response_body.keys()
        assert response_body.get("type") == "battery"
        assert response_body.get("content") == "My event content"

