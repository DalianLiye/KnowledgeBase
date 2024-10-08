[目录](../目录.md)

# 关于logging #
logging不会抛出错误，而且可以输出到文件\
虽然用IDE调试起来比较方便，但是最后你会发现，logging才是终极武器

# logging的好处 #
- 允许指定记录信息的级别，有debug，info，warning，error等几个级别\
  当指定level=INFO时，logging.debug就不起作用了，同理，指定level=WARNING后，debug和info就不起作用了\
  这样就可放心地输出不同级别的信息，也不用删除，最后统一控制输出哪个级别的信息
- 通过简单的配置，一条语句可以同时输出到不同的地方，比如console和文件


```python
import logging
logging.basicConfig(level=logging.INFO)

s = '0'
n = int(s)
logging.info('n = %d' % n)    #logging.info()就可以输出一段文本
print(10 / n)

#输出：
INFO:root:n = 0
Traceback (most recent call last):
    File "err.py", line 8, in <module>
    print(10 / n)
ZeroDivisionError: division by zero
```
