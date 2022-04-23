import pytomlpp
import Serializer.SerializerToml.SerializerToml
import Deserializer.DeserializerToml.DeserializerToml
import Serializer.SerializerYaml.SerializerYaml
import Deserializer.DeserializerYaml.DeserializerYaml

class Toml:
    @staticmethod
    def dump(obj, f):
        data = Serializer.SerializerYaml.SerializerYaml.serialize(obj)
        with open(f, 'w') as file:
            pytomlpp.dump(data, file)

    @staticmethod
    def dumps(obj):
        data = Serializer.SerializerYaml.SerializerYaml.serialize(obj)
        return pytomlpp.dumps(data)

    @staticmethod
    def load(f):
        with open(f, 'r+') as file:
            data = pytomlpp.load(file)
        return Deserializer.DeserializerYaml.DeserializerYaml.deserialize(data)

    @staticmethod
    def loads(s):
        data = pytomlpp.loads(s)
        result = Deserializer.DeserializerYaml.DeserializerYaml.deserialize(data)

        return result
