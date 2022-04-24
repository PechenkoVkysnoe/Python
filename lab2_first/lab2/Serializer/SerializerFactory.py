from lab2.Serializer.SerializerJson.constants import JSON, YAML, TOML
from lab2.Parsers.JsonParser import Json
from lab2.Parsers.TomlParser import Toml
from lab2.Parsers.YamlParser import Yaml


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
