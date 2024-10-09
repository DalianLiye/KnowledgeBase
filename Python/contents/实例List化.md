[目录](../目录.md)

# 实例List化(__getitem__()，__setitem__()和__delitem__()) #
实现了__iter__()的实例虽能用于for循环，看似像list，但并不能将其当做list来使用，比如，Fib()[5]还是报错\
可通过实现__getitem__()方法，；来实现让实例像list那样按照下标取出元素

- 实现按下标取元素
```python
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a
        
f = Fib()
f[0]    #输出：1
f[1]    #输出：1
f[2]    #输出：2
f[3]    #输出：3
f[10]    #输出：89
f[100]    #输出：573147844013817084101
```

- 实现切片功能
__getitem__()传入的参数可能是一个int，也可能是一个切片对象slice，因此需要做判断\
如果把对象看成dict，__getitem__()的参数也可能是一个可以作key的object，例如str

```python
class Fib(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice): # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L
        
f[0:5]    #输出：[1, 1, 2, 3, 5]
f[:10]    #输出：[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
#该例没有对step参数作处理，也没有对负数作处理，所以，要正确实现一个__getitem__()还是有很多工作要做的
```

- 实现元素的设定与删除
与之对应的还有__setitem__()方法和__delitem__()方法，分别用于为某个元素设值和删除某个元素\
总之，通过上面的方法，可自定义的类表现得和Python自带的list、tuple、dict没什么区别，这完全归功于动态语言的"鸭子类型"，不需要强制继承某个接口
