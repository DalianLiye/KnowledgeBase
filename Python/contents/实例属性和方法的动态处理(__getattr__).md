[目录](../目录.md)

# 实例属性和方法的动态处理(__getattr__) #
正常情况下，当调用类的方法或属性时，如果不存在，就会报错\
要避免这个错误，除了可以加上那个要调用但不存在的属性外，Python还有另一个机制，那就是写一个__getattr__()方法，动态返回一个属性\
只有在没有找到属性的情况下，才调用__getattr__，已有的属性会直接在类属性里查找，不会在__getattr__中查找


```python
class Student(object):

    def __init__(self):
        self.name = 'Michael'

    def __getattr__(self, attr):
        if attr=='score':
            return 99
        if attr=='age':
            return lambda: 25
        #要让class只响应特定的几个属性，我们就要按照约定，抛出AttributeError的错误
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % attr)
        

s = Student()
print(s.name)    #输出：'Michael'
print(s.score)    #输出：99，当调用不存在的score属性时，Python解释器会调用__getattr__(self, 'score')来尝试获得属性，这样就会返回score的值
s.age()   #输出：25，返回函数也是完全可以的
print(s.abc)    #输出：None，任意调用如s.abc都会返回None，因为定义的__getattr__默认返回就是None
```

可以把一个类的所有属性和方法调用全部动态化处理了，不需要任何特殊手段\
这种完全动态调用的特性的作用就是，可以针对完全动态的情况作调用
