import pytomlpp
import lab2.SerializerYaml
import lab2.DeserializerYaml

class Toml:
    @staticmethod
    def dump(obj, f):
        data = lab2.SerializerYaml.serialize(obj)
        with open(f, 'w') as file:
            pytomlpp.dump(data, file)

    @staticmethod
    def dumps(obj):
        data = lab2.SerializerYaml.serialize(obj)
        return pytomlpp.dumps(data)

    @staticmethod
    def load(f):
        with open(f, 'r+') as file:
            data = pytomlpp.load(file)
        return lab2.DeserializerYaml.deserialize(data)

    @staticmethod
    def loads(s):
        data = pytomlpp.loads(s)
        result = lab2.DeserializerYaml.deserialize(data)

        return result
