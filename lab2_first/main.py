import math
import types

import Serializer.SerializerFactory
import Serializer.SerializerJson

def hello():
    print('hello')

    def world():
        print('world')

    world()
def fib(n):
    if n == 0 or n == 1:
        return 1

    else:
        return fib(n - 1) + fib(n - 2)
my_number = 42
my_list = [True, [False, 228], 'pamagiti', []]
my_dict = {'1': {'2': 'aaaaaaaaaaa'}, '-5': 228, 'fd': [my_list]}
my_list2 = {'Халява':'прийди'}
def main():
    pass

class My:
    a=5

class Dad:
    def __init__(self, second_name):
        self.second_name = second_name


class Baby(Dad):
    def __init__(self, first_name, second_name):
        Dad.__init__(self, second_name)
        self.first_name = first_name

    def get_full_name(self):
        return [self.first_name, self.second_name]
st = Serializer.SerializerFactory.Serializer.create_serializer('toml')
uy=Serializer.SerializerFactory.Serializer.create_serializer('json')
la = Serializer.SerializerFactory.Serializer.create_serializer('yaml')
'''c01=uy.Json.dumps(My)
print(c01)'''
def f9():
    return 511111111111111111111111111111111111111111111111111111111111111111111111
c11=la.Yaml.dumps(f9)
print(c11)
c21=la.Yaml.loads(c11)
print(c21())
print(c21.__bases__)
#print(Baby.__bases__)
print(c21.__init__.__globals__)
my=c21('aaaa','aaa')

c113=la.Yaml.dumps(my)

c213=la.Yaml.loads(c113)
print(c213)
print(my)
print(get_full_name(c213))
'''x=c2
print(x.a)'''
'''c1=uy.Json.dumps(My)
print(c1)
c2=la.Yaml.loads(c1)'''


'''v1=st.Toml.dumps(hello)
print(v1)'''
#c=st.Toml.dumps(my_number)
if __name__ == '__main__':
    main()
