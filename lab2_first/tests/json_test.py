from unittest import TestCase
from tests.test_things import my_number, my_list, my_dict, fib, mathematics, hello, Baby
from Serializer import SerializerFactory


class TestFunction(TestCase):
    def setUp(self):
        self.my_parser = SerializerFactory.Serializer.create_serializer('json')
        self.file = 'temp.json'

    def test_parser_obj(self):
        self.my_parser.Json.dump(my_number, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result, my_number)

        self.my_parser.Json.dump(my_list, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result, my_list)

        self.my_parser.Json.dump(my_dict, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result, my_dict)

    def test_parser_function(self):
        self.my_parser.Json.dump(fib, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result(10), fib(10))

        self.my_parser.Json.dump(mathematics, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result(4.2, 2.4), mathematics(4.2, 2.4))

        self.my_parser.Json.dump(hello, self.file, indent=2)
        result = self.my_parser.Json.load(self.file)
        self.assertEqual(result(), hello())

    def test_parser_class(self):
        self.my_parser.Json.dump(Baby, self.file, indent=2)
        data = self.my_parser.Json.load(self.file)
        result = data('Misha', 'Grigorchuk')
        test_result = Baby('Misha', 'Grigorchuk')
        self.assertEqual(result.get_full_name(), test_result.get_full_name())

        self.my_parser.Json.dump(result, self.file, indent=2)
        data = self.my_parser.Json.load(self.file)
        self.assertEqual(result.get_full_name(), data.get_full_name())
