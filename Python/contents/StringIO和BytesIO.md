[目录](../目录.md)

# 关于StringIO和BytesIO #
数据读写不一定是文件，也可在内存中读写\
在内存中读写可分为两种:
- 读写字符(StringIO)，其操作的是str
- 字节读写(BytesIO)，其操作的二进制数据

# StringIO #
StringIO就是在内存中读写str\
要把str写入StringIO，需先创建一个StringIO，然后像文件一样写入即可\
要读取StringIO，可以用一个str初始化StringIO，然后像读文件一样读取
```python
from io import StringIO
        
f_w = StringIO()
f_w.write('hello')
f_w.write(' ')
f_w.write('world!')
print(f_w.getvalue())   #getvalue()方法用于获得写入后的str
                        #output --> hello world!
        
f_r = StringIO('Hello!\nHi!\nGoodbye!')
while True:
    s = f_r.readline() #readline()方法从StringIO中读取str
    if s == '':
        break
    print(s.strip())
```
 

# BytesIO #
BytesIO就是在内存中读写bytes\
要把bytes写入BytesIO，需先创建一个BytesIO，然后像文件一样写入即可\
要读取BytesIO，可以用一个bytes初始化BytesIO，然后像读文件一样读取

```python
from io import BytesIO

f_w = BytesIO()
f_w.write('中文'.encode('utf-8')) #写入的不是str，而是经过UTF-8编码的bytes
print(f_w.getvalue()) #getvalue()方法用于获得写入后的bytes
                      #output --> b'\xe4\xb8\xad\xe6\x96\x87'
                                     
f_r = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(f_r.read()) #output --> b'\xe4\xb8\xad\xe6\x96\x87'
```
