from datetime import datetime
import Adafruit_DHT
import httpx

from config import Settings

class TemperaturePusher:
    def __init__(self, settings: Settings) -> None:
        self._sensor = Adafruit_DHT.AM2302
        self._pin = settings.sensor_pin
        self._sensor_location = settings.sensor_location

        self._credential = settings.credential
        self._behive_id = settings.behive_id
        self._endpoint = settings.endpoint
        self._fallback_endpoint = settings.fallback_endpoint

    def read_sensor_value(self):
        humidity, temperature = Adafruit_DHT.read_retry(self._sensor, self._pin)
        return humidity, temperature

    def get_token(self, endpoint):
        response = httpx.post(f"{endpoint}/api/token", data=self._credential.dict())
        response.raise_for_status()

        return response.json()["access_token"]

    def send(self, *, endpoint=None, sensor_value=None, attempt=1, error: Exception|None=None):
        if endpoint == None:
            endpoint = self._endpoint

        if not sensor_value:
            sensor_value = self.read_sensor_value()
        humidity, temperature = sensor_value

        if attempt > 2: raise (error if error else RuntimeError("Too many attemps"))

        for sensor_type, value, unit in (("humidity", humidity, "%"), ("temperature", temperature, "°C")):
            try:
                httpx.post(
                    f"{endpoint}/api/sensors/behive/{self._behive_id}/{sensor_type}_{self._sensor_location}",
                    json={"updated_at": datetime.today(),"value": value,"unit": unit},
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
    parser.add_argument('--env-file', help='.env file path', default='.env')

    options = parser.parse_args()

    try:
        settings = Settings(_env_file=options.env_file)
        TemperaturePusher(settings).send()
    except:
        traceback.print_exc()
        sys.exit(1)
