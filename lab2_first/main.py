import math
import types

import Serializer.SerializerFactory
import Serializer.SerializerJson
'''

def f9():
    print(8)
a=55

def f():
    print(5)
    #print(a)
    #print(math.sin(3))

f()

l = {"1": {'2': 3}}
d = [None, 1]
s = Serializer.SerializerFactory.Serializer.create_serialiser('json')
r1=s.Json.dumps(f,indent=2)
print(r1)
r2=s.Json.loads(r1)
r3=s.Json.dumps(r2,indent=2)
class f22():
    g=5
    def h(self):
        self.g+=1
#print(getattr(f22))
print(r2.__code__.co_names)
print(r3==r1)
print(f)
print(f.__globals__)
#f.__globals__['__build__']=__import__('print')
s.Json.dump(f,'test.json',indent=2)
kj=s.Json.load('test.json')
kj()

# yt=<_frozen_importlib_external.SourceFileLoader object at 0x7fdc95dd64f0>
print(f22.__dict__['__dict__'])'''
def main():
    pass
class H():
    pass
class Vehicle():
    def __init__(self,name):
        self.name=name
    def hidden(self, name):
        print(self.name)
class Car(Vehicle):
    def __init__(self,name,engine):
        Vehicle.__init__(self,name)
        self.engine=engine

    def ride(self):
        print(f'{self.name} is ridding now')
def hello():
    print("hello")
q12=Car('1','2')
q12.car=hello
print(q12)
#print(Car)
q1=False
s = Serializer.SerializerFactory.Serializer.create_serializer('json')
qwe=s.Json.dumps(q12,indent=2)

qwer=s.Json.loads(qwe)
print(isinstance(q12.car,types.FunctionType ))
print(111111111111111111111111111111111111111111111111111111111111111111111111)
print(qwer)
global l
l = {"1": {'2': 3}}
def fib(n):
    if n==0 or n==1:
        return 1
    return fib(n-1)+fib(n-2)
def f1(a):
    x=a+l['1']['2']
    o=7
    print(o)
    def f2(r):
       print(r)
    f2(4)
    print(math.sin(3))
    return x

def x():
    def y():
        print('ww')
    y()
def y():
    print(2)
kjh='asdas'
def f3():
    p=[1,2,3]
    print(p)
ex=Car(12,14)
def nb():
    print('Hello')
print(ex.__dict__)
d=s.Json.dumps(y,indent=2)
print(nb.__name__)
print(d)
d3=s.Json.loads(d)
d3()
def mathematics(a,b):
    print(a+b)
    print(a-b)
    print(a/b)
    print(a*b)
    print(math.sin(a))
test1=s.Json.dumps(mathematics,indent=2)
test2=s.Json.loads(test1)
test2(4,2)
#d_1=s.Json.dumps(,indent=2)
kbf=[1,2]
st = Serializer.SerializerFactory.Serializer.create_serializer('toml')
la = Serializer.SerializerFactory.Serializer.create_serializer('yaml')
dh=la.Yaml.dumps(Car)

print(dh)
res=la.Yaml.loads(dh)
print(res)
yd=res('1','2')
yd.ride()
dh=la.Yaml.dumps(yd)

print(dh)
'''es=la.Yaml.loads(dh)
res.ride()'''

#ret=st.Toml.loads(jh)
if __name__ == '__main__':
    main()
