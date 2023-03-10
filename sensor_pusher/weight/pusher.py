from datetime import datetime, timedelta
from HX711 import *
import httpx

from .config import Settings

class WeightPusher:
    def __init__(self, settings: Settings) -> None:
        self._sck_pin = settings.sck_pin
        self._dt_pin = settings.dt_pin
        self._ref_unit = settings.ref_unit
        self._offset = settings.offset

        self._credential = settings.credential
        self._behive_id = settings.behive_id
        self._endpoint = settings.endpoint
        self._fallback_endpoint = settings.fallback_endpoint

    def read_sensor_value(self):
        # minimise the time spent by the CPU checking whether data is ready to be obtained from the HX711 module
        # while remaining as efficient as possible (use a separate thread)
        with AdvancedHX711(self._dt_pin, self._sck_pin, self._ref_unit, self._offset) as hx:
            weight = hx.weight(timedelta(seconds=1))

        return weight

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
            httpx.post(
                f"{endpoint}/api/sensors/behive/{self._behive_id}/weight",
                json={"updated_at": datetime.today().isoformat(),"value": weight,"unit": "kg"},
                headers={"Authorization": f"Bearer ${self.get_token(endpoint)}"}
            )
        except httpx.NetworkError:
            self.send(endpoint=self._fallback_endpoint, sensor_value=sensor_value, attempt=attempt+1, error=error)

if __name__ == '__main__':
    import argparse
    import traceback
    import sys
    import os

    scriptname = os.path.basename(__file__)
    parser = argparse.ArgumentParser(scriptname)
    parser.add_argument('--env-file', default='.env', help='.env file path')

    options = parser.parse_args()

    try:
        settings = Settings(_env_file=options.env_file)
        WeightPusher(settings).send()
    except:
        traceback.print_exc()
        sys.exit(1)
