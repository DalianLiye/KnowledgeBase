[目录](../目录.md)

# 实例调用(__call__()) #
任何类，只需要定义一个__call__()方法，就可直接对实例进行调用\
对实例进行直接调用就好比对一个函数进行调用一样

__call__()还可定义参数，所以调用完全可以把对象看成函数，把函数看成对象，因为这两者之间本来就没啥根本的区别\
如果把对象看成函数，那么函数本身其实也可以在运行期动态创建出来，因为类的实例都是运行期创建出来的，因此也就模糊了对象和函数的界限

判断变量是对象还是函数\
更多的时候，需判断对象是否能被调用，如果对象能被调用，则该对象就是一个Callable对象\
比如函数和上面定义的带有__call__()的类实例，它们就是就是能被调用的，它们都是一个Callable对象

```python
class Student(object):
    def __init__(self, name):
        self.name = name

    def __call__(self): 
        print('My name is %s.' % self.name)
        
s = Student('Michael')
s()    #输出：My name is Michael.

#通过callable()函数，可以判断一个对象是否是"可调用"对象
callable(Student())  #True
callable(max)  #True
callable([1, 2, 3])  #False
callable(None)  #False
callable('str')  #False
```
