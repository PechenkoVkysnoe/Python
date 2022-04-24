import yaml
from lab2.Serializer.SerializerYaml.SerializerYaml import serialize
from lab2.Deserializer.DeserializerYaml.DeserializerYaml import deserialize


class Yaml:
    @staticmethod
    def dump(obj, f):
        data = serialize(obj)
        with open(f, 'w') as file:
            yaml.dump(data, file)

    @staticmethod
    def dumps(obj):
        data = serialize(obj)
        result = yaml.dump(data)
        return result

    @staticmethod
    def load(f):
        with open(f, 'r') as file:
            data = yaml.unsafe_load(file)
        result = deserialize(data)
        return result

    @staticmethod
    def loads(s):
        data = yaml.unsafe_load(s)
        result = deserialize(data)
        return result
