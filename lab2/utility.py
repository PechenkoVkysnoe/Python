import argparse
import os, shutil
from utility_constant import JSON, YAML, TOML, FORMAT_TOML, FORMAT_JSON, FORMAT_YAML
from lab2 import SerializerJson, SerializerFactory, SerializerYaml, DeserializerYaml, DeserializerJson, Json, Toml, Yaml

'''from factory.factory import SerializerFactory
from factory.serializer_types import SerializerTypes'''

parser = argparse.ArgumentParser()

parser.add_argument(
    '--path',
    type=str,
    required=True
)
parser.add_argument(
    '--format',
    type=str,
    choices=[
        JSON,
        YAML,
        TOML
    ],
    required=True
)

args = parser.parse_args()

if __name__ == '__main__':

    if os.path.exists(args.path):

        filename, file_format = os.path.splitext(args.path)
        if (file_format == FORMAT_JSON and args.format == JSON) \
                or (file_format == FORMAT_YAML and args.format == YAML) \
                or (file_format == FORMAT_TOML and args.format == TOML):
            print('the file is already in such format')

            exit()

        if file_format == FORMAT_JSON:
            json = SerializerFactory.Serializer.create_serializer(JSON)

            buff = json.Json.load(args.path)

            new_filename = ''
            if args.format == YAML:
                new_filename = filename + FORMAT_YAML

            elif args.format == TOML:
                new_filename = filename + FORMAT_TOML

            os.rename(args.path, new_filename)

            if args.format == YAML:
                yaml = SerializerFactory.Serializer.create_serializer(YAML)
                yaml.Yaml.dump(buff, new_filename)

            elif args.format == TOML:
                toml = SerializerFactory.Serializer.create_serializer(TOML)
                toml.Toml.dump(buff, new_filename)

        elif file_format == FORMAT_YAML:
            yaml = SerializerFactory.Serializer.create_serializer(YAML)

            buff = yaml.Yaml.load(args.path)

            new_filename = ''
            if args.format == JSON:
                new_filename = filename + FORMAT_JSON

            elif args.format == TOML:
                new_filename = filename + FORMAT_TOML

            os.rename(args.path, new_filename)

            if args.format == JSON:
                json = SerializerFactory.Serializer.create_serializer(JSON)
                json.Json.dump(buff, new_filename)

            elif args.format == TOML:
                toml = SerializerFactory.Serializer.create_serializer(TOML)
                toml.Toml.dump(buff, new_filename)

        elif file_format == FORMAT_TOML:
            toml = SerializerFactory.Serializer.create_serializer(TOML)

            buff = toml.Toml.load(args.path)

            new_filename = ''
            if args.format == YAML:
                new_filename = filename + FORMAT_YAML

            elif args.format == JSON:
                new_filename = filename + FORMAT_JSON

            os.rename(args.path, new_filename)

            if args.format == YAML:
                yaml = SerializerFactory.Serializer.create_serializer(YAML)
                yaml.Yaml.dump(buff, new_filename)

            elif args.format == JSON:
                json = SerializerFactory.Serializer.create_serializer(JSON)
                json.Json.dump(buff, new_filename)


    else:
        print('File is not found')
