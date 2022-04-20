import math
import types

import Serializer.SerializerFactory
import Serializer.SerializerJson

my_number = 42
my_list = [True, [False, 228], 'pamagiti', []]
my_dict = {'1': {'2': 'aaaaaaaaaaa'}, '-5': 228, 'fd': [my_list]}
my_list2 = {'Халява':'прийди'}
def main():
    pass

st = Serializer.SerializerFactory.Serializer.create_serializer('toml')
la = Serializer.SerializerFactory.Serializer.create_serializer('yaml')
c1=la.Yaml.dumps(my_number)
print(c1)
#c=st.Toml.dumps(my_number)
if __name__ == '__main__':
    main()
