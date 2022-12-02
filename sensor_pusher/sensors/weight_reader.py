from sensor_pusher.sensors.base_sensor_reader import BaseSensorReader


class WeightReader(BaseSensorReader):
    def read(self):
        ...