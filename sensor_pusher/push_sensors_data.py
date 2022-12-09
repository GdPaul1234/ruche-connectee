import argparse
from configparser import ConfigParser
import concurrent.futures
import logging
import logging.handlers
import os
from pathlib import Path
import time
import schedule
import sys

from sensor_pusher.config_loader import ConfigLoader
from sensor_pusher.sensors.temperature_reader import TemperatureReader
from sensor_pusher.sensors.weight_reader import WeightReader
from sensor_pusher.sensors.gps_reader import GpsReader

# config -> sensor reader class
SENSORS_MAPPING = {
    'Weight Sensor': WeightReader,
    'Temperature Sensor': TemperatureReader,
    'Gps Sensor': GpsReader
}

# sensor reader class -> sensor type for API
SENSOR_TYPE_MAPPING = {
    WeightReader: 'weight',
    TemperatureReader: 'temperature',
    GpsReader: 'location'
}

# TODO: set logger config in main
logger = logging.getLogger(__name__)


class SensorFactory:
    @staticmethod
    def create_sensor_from_type(sensor_type: str):
        return SENSORS_MAPPING[sensor_type]()


class SensorsPusher:
    def __init__(self, config: ConfigParser):
        self._config = config
        self._sensors = [SensorFactory.create_sensor_from_type(sensor_type)
                         for sensor_type in self.activated_sensors]

    @property
    def activated_sensors(self):
        return [
            sensor_section
            for sensor_section in SENSORS_MAPPING.keys()
            if self._config.getboolean(sensor_section, 'active', fallback=False)
        ]

    def send_data(self, sensor_type: str, sensor_value):
        endpoint = self._config.get(
            'Connection', 'endpoint', fallback='https://example.org')
        ...

    def get_and_push_data(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(self.activated_sensors)) as executor:
            future_tasks = {
                executor.submit(sensor.read): sensor.__class__
                for sensor in self._sensors
            }

            for future in concurrent.futures.as_completed(future_tasks):
                sensor_type = SENSOR_TYPE_MAPPING[future_tasks[future]]

                try:
                    sensor_value = future.result()
                except Exception as e:
                    # TODO send alert about faulty sensor
                    ...
                else:
                    self.send_data(sensor_type, sensor_value)


def main():
    scriptname = os.path.basename(__file__)
    parser = argparse.ArgumentParser(scriptname)
    levels = ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')

    parser.add_argument('--log-level', default='INFO', choices=levels)
    parser.add_argument(
        '--config-path', default='config.ini', help='Config path')

    options = parser.parse_args()
    config_path = Path(options.config_path)
    config = ConfigLoader(config_path).config

    fh = logging.handlers.TimedRotatingFileHandler(
        filename=config.get('Logger', 'file_path', fallback='log.txt'))
    fh.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # TODO add cloud logger

    logging.basicConfig(level=options.log_level, handlers=(fh,))

    sensors_pusher = SensorsPusher(config)
    schedule.every(3).minutes.do(sensors_pusher.get_and_push_data)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    sys.exit(main())
