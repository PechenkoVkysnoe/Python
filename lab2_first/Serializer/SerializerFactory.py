from Serializer.SerializerJson.constants import JSON, YAML, TOML
from Parsers.JsonParser import Json
from Parsers.TomlParser import Toml
from Parsers.YamlParser import Yaml


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
