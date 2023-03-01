from datetime import datetime
from pydantic import BaseModel, BaseSettings
import httpx

class Credential(BaseModel):
    username: str
    password: str


class Settings(BaseSettings):
    endpoint: str
    fallback_endpoint: str
    behive_id: str

    credential: Credential


class DummyWeightPusher:
    def __init__(self, settings: Settings) -> None:
        self._credential = settings.credential
        self._behive_id = settings.behive_id
        self._endpoint = settings.endpoint
        self._fallback_endpoint = settings.fallback_endpoint

    def read_sensor_value(self):
        return 42

    def get_token(self, endpoint):
        response = httpx.post(f"{endpoint}/api/token", data=self._credential.dict())
        response.raise_for_status()

        return response.json()["access_token"]

    def send(self, *, endpoint=None, sensor_value=None, attempt=1, error: Exception|None=None):
        if endpoint == None:
            endpoint = self._endpoint

        if not sensor_value:
            sensor_value = self.read_sensor_value()
        weight = sensor_value

        if attempt > 2: raise (error if error else RuntimeError("Too many attemps"))

        try:
            response = httpx.post(
                f"{endpoint}/api/sensors/behive/{self._behive_id}/weight",
                json={"updated_at": datetime.today().isoformat(), "value": weight, "unit": "kg"},
                headers={"Authorization": f"Bearer ${self.get_token(endpoint)}"}
            )
            response.raise_for_status()
        except httpx.NetworkError as error:
            self.send(endpoint=self._fallback_endpoint, sensor_value=sensor_value, attempt=attempt+1, error=error)
