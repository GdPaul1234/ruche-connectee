from configparser import ConfigParser
import Adafruit_DHT

from sensor_pusher.sensors.base_sensor_reader import BaseSensorReader


class TemperatureReader(BaseSensorReader):
    def __init__(self, config: ConfigParser):
        self._sensor = Adafruit_DHT.AM2302
        self._pin = config.getint('Temperature Sensor', 'pin', fallback=2)

    def read(self):
        humidity, temperature = Adafruit_DHT.read_retry(self._sensor, self._pin)
        return { "humidity": humidity, "temperature": temperature }
