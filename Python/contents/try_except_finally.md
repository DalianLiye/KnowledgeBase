[目录](../目录.md)

# 关于错误处理 #
Python也不例外,跟其他高级语言一样，内置了一套try...except...finally...的错误处理机制\
当认为某些代码可能会出错时，就可以用try来运行这段代码\
使用try时，要么except和finally至少要有一个存在，否则会无法通过编译\
捕获异常的意义在于，可以阻止程序意外中止，或以预想的方式中止，如果不捕获异常，错误会被解释器捕获，那么程序也就中止了

 
# try...except...finally...机制 #
如果执行出错，则后续代码不会继续执行，而是直接跳转至错误处理代码，即except语句块\
如果有finally语句块，执行完except后，则执行finally语句块，至此，执行完毕\
不管有没有报错，finally下的语句都一定会被执行
```python
try:
    ......
except ZeroDivisionError as e:
    print('except:', e)
finally:
    print('finally...')
```

# 错误的继承 #
Python的错误其实也是class，所有的错误类型都继承自BaseException\
所以在使用except时需要注意的是，它不但捕获该类对应的错误，还会捕获其子类对应的错误\
比如AError是BError的父类，如果except AError在先，except BError在后，
但若错误被except AError捕获，且该错误也属于BError，则该错误不会被except BError所捕获

Python所有的错误都是从BaseException类派生的\
常见的错误类型和继承关系请参照链接：https://docs.python.org/3/library/exceptions.html#exception-hierarchy

```python
try:
    ......
except ValueError as e:
    print('ValueError')
except UnicodeError as e: 
    #第二个except永远也捕获不到UnicodeError，因为UnicodeError是ValueError的子类，如果有，也被第一个except给捕获了
    print('UnicodeError')
```

# 跨越多层调用 #
使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用\
比如函数main()调用bar()，bar()调用foo()，如果foo()出错，则只要main()捕获即可, 无需在每个可能出错的地方去捕获错误，只要在合适的层次去捕获错误即可，因此大大减少了写try...except...finally的麻烦

```python
def foo(s):
    return 10 / int(s)

def bar(s):
    return foo(s) * 2

def main():
    try:
        bar('0')
    except Exception as e:
        print('Error:', e)
    finally:
        print('finally...')
```
