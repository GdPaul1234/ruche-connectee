from configparser import ConfigParser, ExtendedInterpolation
from pathlib import Path

class ConfigLoader:
    def __init__(self, config_path: Path) -> None:
        self._config = ConfigParser(interpolation=ExtendedInterpolation())
        self._config.read(config_path, encoding='utf-8')

    @property
    def config(self):
        return self._config
