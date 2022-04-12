from unittest import TestCase
from tests.test_things import my_dict, hello, Baby, fun, my_list2
from Serializer import SerializerFactory


class TestFunction(TestCase):
    def setUp(self):
        self.my_parser = SerializerFactory.Serializer.create_serializer('toml')
        self.file = 'temp.toml'

    def test_parser_obj(self):
        self.my_parser.Toml.dump(my_dict, self.file)
        result = self.my_parser.Toml.load(self.file)
        self.assertEqual(result, my_dict)

        self.my_parser.Toml.dump(my_list2, self.file)
        result = self.my_parser.Toml.load(self.file)
        self.assertEqual(result, my_list2)

    def test_parser_function(self):
        data = self.my_parser.Toml.dumps(hello)
        result = self.my_parser.Toml.loads(data)
        self.assertEqual(result(), hello())

        data = self.my_parser.Toml.dumps(fun)
        result = self.my_parser.Toml.loads(data)
        self.assertEqual(result(42), fun(42))

    def test_parser_class(self):
        self.my_parser.Toml.dump(Baby, self.file)
        data = self.my_parser.Toml.load(self.file)
        result = data('Misha', 'Grigorchuk')
        test_result = Baby('Misha', 'Grigorchuk')
        self.assertEqual(result.get_full_name(), test_result.get_full_name())
