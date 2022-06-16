from lab2.constants import JSON, YAML, TOML
from lab2 import Json
from lab2 import Toml
from lab2 import Yaml


class Serializer:

    @staticmethod
    def create_serializer(t):
        if t == JSON:
            return Json

        elif t == YAML:
            return Yaml

        elif t == TOML:
            return Toml

        else:
            raise ValueError
