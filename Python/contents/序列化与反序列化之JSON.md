[目录](../目录.md)

# 序列化与反序列化之json #
在不同编程语言之间传递对象，须把对象序列化为标准格式，比如XML\
但更好的方法是序列化为JSON，因为JSON表示出来就是一个字符串，可被所有语言读取，也可方便地存储到磁盘或者通过网络传输\
JSON不仅是标准格式，并且比XML更快，而且可直接在Web页面中读取，因为JSON表示的对象就是标准的JavaScript语言的对象

JSON和Python内置的数据类型对应如下：
| JSON类型 | Python类型 |
|:--------:| :---------:|
| {} | dict |
| [] | list |
| "string" | str |
| 1234.56 | int或float |
| true/false |	True/False |
| null | None|


# 使用示例 #

- 序列化与反序列化之json(字符串)

```python
import json
d = dict(name='Bob', age=20, score=88) #dict对象可以直接序列化为JSON的{}
print(json.dumps(d)) 
#输出：{"name": "Bob", "age": 20, "score": 88}
#把对象序列化为标准的json字符串格式

json_str = '{"age": 20, "score": 88, "name": "Bob"}' 
print(json.loads(json_str))
#输出：{"name": "Bob", "age": 20, "score": 88}
#把JSON字符串反序列化出对象
```


- 序列化与反序列化之json(文件)
```python
import json
d = dict(name='Bob', age=20, score=88)
f = open('dump.txt', 'w')
json.dump(d, f)     #把对象序列化成json字符串后写入一个file-like Object
f.close()

f1 = open('dump.txt', 'r')
d1 = json.load(f1)     #从一个file-like Object中将json字符串反序列化出对象
f1.close()
print(d1)  #输出：{'name': 'Bob', 'age': 20, 'score': 88}
```

- 序列化与反序列化之json(自定义对象)
```python
import json

class Student(object):
   def __init__(self, name, age, score):
      self.name = name
      self.age = age
      self.score = score

def student2dict(std):
   return {
      'name': std.name,
      'age': std.age,
      'score': std.score
   }

def dict2student(d):
   return Student(d['name'], d['age'], d['score'])

s = Student('Bob', 20, 88)

#Student对象是无法直接通过dumps方法转换json的，需要转换成dict
print(json.dumps(s, default=student2dict)) 

#该方式可以将任意class转换为dict
#通常class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量。也有少数例外，比如定义了__slots__的class
print(json.dumps(s, default=lambda obj: obj.__dict__)) 

#loads()方法首先转换出一个dict对象，然后，传入的object_hook函数负责把dict转换为Student
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=dict2student))
```
**注：**\
由于JSON标准规定JSON编码是UTF-8，所以我们总是能正确地在Python的str与JSON的字符串之间转换
