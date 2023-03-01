import asyncio
import pytest

from .dummy_sensor_pusher import Settings, Credential, DummyWeightPusher

class TestSensorPusher:
    base_url = "http://localhost:8888"

    @pytest.mark.anyio
    async def test_sensor_pusher(self, server, mongodb, token_behive, behive, behive_sensors):
        behive_id = str(behive["_id"])

        settings = Settings(
            endpoint=self.base_url,
            fallback_endpoint=self.base_url,
            behive_id=behive_id,
            credential=Credential(username=f"behive_{behive_id}", password="password")
        )

        DummyWeightPusher(settings).send()
        await asyncio.sleep(.1) # wait for insertion

        behive = await mongodb.behives.find_one({"_id": behive["_id"] })
        assert behive["last_metrics"]["weight"]["value"] == 42

    @pytest.mark.anyio
    async def test_sensor_pusher_fallback(self, server, mongodb, token_behive, behive, behive_sensors):
        behive_id = str(behive["_id"])

        settings = Settings(
            endpoint="http://localhost:6666",
            fallback_endpoint=self.base_url,
            behive_id=behive_id,
            credential=Credential(username=f"behive_{behive_id}", password="password")
        )

        DummyWeightPusher(settings).send()
        await asyncio.sleep(.1) # wait for insertion

        behive = await mongodb.behives.find_one({"_id": behive["_id"] })
        assert behive["last_metrics"]["weight"]["value"] == 42

    @pytest.mark.anyio
    async def test_sensor_pusher_fail(self, server, mongodb, token_behive, behive, behive_sensors):
        import httpx

        behive_id = str(behive["_id"])

        settings = Settings(
            endpoint="http://localhost:6666",
            fallback_endpoint="http://localhost:6666",
            behive_id=behive_id,
            credential=Credential(username=f"behive_{behive_id}", password="password")
        )

        with pytest.raises(httpx.TransportError):
            DummyWeightPusher(settings).send()
