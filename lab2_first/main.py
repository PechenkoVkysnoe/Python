import math
import types

import Serializer.SerializerFactory
import Serializer.SerializerJson

def hello():
    print('hello')

    def world():
        print('world')

    world()

my_number = 42
my_list = [True, [False, 228], 'pamagiti', []]
my_dict = {'1': {'2': 'aaaaaaaaaaa'}, '-5': 228, 'fd': [my_list]}
my_list2 = {'Халява':'прийди'}
def main():
    pass

st = Serializer.SerializerFactory.Serializer.create_serializer('toml')
la = Serializer.SerializerFactory.Serializer.create_serializer('yaml')
c1=la.Yaml.dumps(hello)
c2=la.Yaml.loads(c1)
print(c2.__code__.co_consts)
c2()
#c=st.Toml.dumps(my_number)
if __name__ == '__main__':
    main()
