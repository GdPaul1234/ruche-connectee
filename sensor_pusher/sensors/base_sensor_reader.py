from abc import ABC
from configparser import ConfigParser

class BaseSensorReader(ABC):
    def __init__(self, config: ConfigParser):
        ...

    def read(self):
        ...
