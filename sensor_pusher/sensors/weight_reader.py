from datetime import timedelta
from HX711 import *

from configparser import ConfigParser
from sensor_pusher.sensors.base_sensor_reader import BaseSensorReader


class WeightReader(BaseSensorReader):
    def __init__(self, config: ConfigParser):
        self._sck_pin = config.getint('Weight Sensor', 'sck_pin')
        self._dt_pin = config.getint('Weight Sensor', 'dt_pin')
        self._ref_unit = config.getint('Weight Sensor', 'ref_unit')
        self._offset = config.getint('Weight Sensor', 'offset')

    def read(self):
        # minimise the time spent by the CPU checking whether data is ready to be obtained from the HX711 module
        # while remaining as efficient as possible (use a separate thread)
        with AdvancedHX711(self._sck_pin, self._dt_pin, self._ref_unit, self._offset) as hx:
            weight = hx.weight(timedelta(seconds=1))
            return { "weight": weight }
