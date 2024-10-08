[目录](../目录.md)

# 关于Map/Reduce #
Map/Reduce概念就是出自Google的那篇大名鼎鼎的论文

# 关于Map #
map()函数接收两个参数，一个是函数，一个是Iterable\
map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回\

从结果上看，for循环也可以实现该功能，但从for循环代码看是无法一眼看明白其把f作用在Iterable的每一个元素并把结果生成一个新的Iterable的\
map()作为高阶函数，事实上它把运算规则抽象了，因此不但可以计算简单函数运算，还可以计算任意复杂的函数

```python
def f(x):
    return x * x
    r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9]) #map()传入的第一个参数是f，即函数对象本身
    print(list(r)) 
    #输出：[1, 4, 9, 16, 25, 36, 49, 64, 81]
    #由于结果r是一个Iterator，Iterator是惰性序列，因此通过list()函数让它把整个序列都计算出来并返回一个list

    list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9])) 
    #输出：['1', '2', '3', '4', '5', '6', '7', '8', '9']
    #把这个list所有数字转为字符串
```
 

# 关于Reduce #
reduce()把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，reduce把结果继续和序列的下一个元素做累积计算\
reduce(f, [x1, x2, x3, x4])的执行过程为： f(f(f(x1, x2), x3), x4)

对一个序列求和
```python
from functools import reduce
def add(x, y):
    return x + y
    reduce(add, [1, 3, 5, 7, 9]) #输出：25，当然求和运算可以直接用Python内建函数sum()，没必要动用reduce
``` 

把序列[1, 3, 5, 7, 9]变换成整数13579
```python
from functools import reduce
def add(x, y):
    return x * 10 + y
    reduce(add, [1, 3, 5, 7, 9]) #输出：13579
``` 

把str转换为int的函数
```python
from functools import reduce
def fn(x, y):
    return x * 10 + y

    def char2num(s):
        digits = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
        return digits[s]
    print(reduce(fn, map(char2num, '13579'))) #输出：13579
``` 
 
整理成一个str2int的函数
```python
from functools import reduce
DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        return DIGITS[s]
    return reduce(fn, map(char2num, s))

print(str2int(['1','3','5','7','9']))
```

给到一个字符串，通过map/reduce方式转换为数字13579(lamada表达式实现)
```python
from functools import reduce

DIGITS = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}

def char2num(s):
    return DIGITS[s]

def str2int(s):
    return reduce(lambda x, y: x * 10 + y, map(char2num, s))

print(str2int(['1','3','5','7','9'])) #输出：13579
```
