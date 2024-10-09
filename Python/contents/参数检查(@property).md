[目录](../目录.md)

# 参数检查(@property) #
绑定属性时，如果直接把属性暴露出去，虽然写起来很简单，但无法对参数进行检查，导致属性被随便修改\
因此，可以通过在类内定义get()获取属性值，定义set()对属性值进行设定并对设定值进行检查

但通过定义get()和set()会让程序显得复杂，没有直接用属性这么直接简单\
Python内置的@property装饰器就是用来负责把一个方法变成属性调用的，它可以通过更加简单的方式来实现上述功能而无需自定义get()和set()\
@property广泛应用在类的定义中，可以让调用者写出简短的代码，同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性


```python
class Student(object):

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value
        
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):  #birth是可读写属性，因为它有setter
        self._birth = value
    
    #还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性
    @property
    def age(self):    #age就是一个只读属性，因为它没有setter
        return 2019 - self._birth
    
    
s = Student()
s.score = 60  # OK，实际转化为s.set_score(60)
print(s.score)  # 输出：60，实际转化为s.get_score()
s.score = 9999  # 报预定错误
s.birth = 1988  # OK，实际转化为s.set_birth(1988)
print(s.birth)  # 输出：1988，实际转化为s.get_birth()
print(s.age)  # 输出：31，实际转化为s.get_age()
```
