[目录](../目录.md)

# 打印对象(__str__()和__repr__()) #
当打印一个类的实例时，返回的字符串是对象的地址信息，如<__main__.Student object at 0x109afb310>，很不好看\
可通过在类内定义__str__()，这样打印实例时就会返回一个好看的字符串，而且容易看出实例内部重要的数据

# 定义__str__() #

```python
class Student(object):

    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'Student object (name: %s)' % self.name
    
print(Student('Michael'))    #输出：Student object (name: Michael)
```
 

# 定义__repr__() #
```python
s = Student('Michael')
s    #输出：<__main__.Student object at 0x109afb310>，打印出来的实例还是不好看
```

因为直接显示实例变量时，它调用的不是__str__()，而是__repr__()
__str__()和__repr__()区别
- __str__()：返回用户看到的字符串
- __repr__()：返回程序开发者看到的字符串，即__repr__()是为调试服务的

解决办法是再定义一个__repr__()，但是通常__str__()和__repr__()代码都是一样的
所以，有个偷懒的写法，就是直接将__str__ 赋给__repr__

```python
class Student(object):

    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        return 'Student object (name=%s)' % self.name
        
    __repr__ = __str__    
    
s = Student('Michael')
s    #输出：Student object (name: Michael)
```
