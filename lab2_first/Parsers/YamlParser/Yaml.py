import yaml
from Serializer.SerializerToml.SerializerToml import serialize
from Deserializer.DeserializerToml.DeserializerToml import deserialize


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
            data = yaml.load(file, Loader=yaml.FullLoader)
        result = deserialize(data)
        return result

    @staticmethod
    def loads(s):
        data = yaml.load(s, Loader=yaml.FullLoader)
        result = deserialize(data)
        return result
