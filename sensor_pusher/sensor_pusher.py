import concurrent.futures
import logging
from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

from sensor_pusher.sensors.base_sensor_reader import BaseSensorReader
from sensor_pusher.sensors.temperature_reader import TemperatureReader
from sensor_pusher.sensors.weight_reader import WeightReader

SENSOR_SECTIONS = ['Weight Sensor', 'Temperature Sensor', 'Gps Sensor']

# TODO: set logger config in main
logger = logging.getLogger(__name__)

class SensorFactory:
    @staticmethod
    def create_sensor_from_type(sensor_type: str) -> BaseSensorReader:
        if sensor_type == 'Weight Sensor':
            return WeightReader()
        elif sensor_type == 'Temperature Sensor':
            return TemperatureReader()

class SensorPusher:
    def __init__(self, config_path: Path):
        # load config
        self._config = ConfigParser(interpolation=ExtendedInterpolation())
        self._config.read(config_path, encoding='utf-8')

    @property
    def activated_sensors(self):
        return [
            sensor_section
            for sensor_section in SENSOR_SECTIONS
            if self._config.getboolean(sensor_section, 'active', fallback=False)
        ]

    def initialize_sensors(self) -> list[BaseSensorReader]:
        return [SensorFactory.create_sensor_from_type(sensor_type)
                for sensor_type in self.activated_sensors]

    def send_data(self, sensor_type: str, sensor_value):
        endpoint = self._config.get('Connection', 'endpoint', fallback='https://example.org')
        ...

    def run(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.activated_sensors)) as executor:
            future_tasks = {
                executor.submit(sensor.read()): sensor.__name__.split('_')[0]
                for sensor in self.initialize_sensors()
            }

            for future in concurrent.futures.as_completed(future_tasks):
                sensor_type = future_tasks[future]

                try:
                    sensor_value = future.result()
                except Exception as e:
                    # TODO send alert about faulty sensor
                    ...
                else:
                    self.send_data(sensor_type, sensor_value)