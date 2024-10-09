[目录](../目录.md)

# 限制属性绑定(__slots__) #
正常情况下，当定义了一个class并创建实例后，可以给该实例绑定任何属性和方法，这就是动态语言的灵活性\
属性和方法是可以直接定义在class中的，但动态绑定允许在程序运行的过程中动态给class加上属性和方法，这在静态语言中很难实现

对于python这种动态语言，给一个实例绑定的属性和方法，对另一个实例是不起作用的\
为了给所有实例都绑定方法，可以通过给class绑定属性和方法的方式实现，就是定义类属性和类方法

但如果所有对象都可随意绑定，则会导致程序很混乱，因此需要对实例的绑定进行一些限制\
为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，用来限制该class实例能添加的属性


# 使用示例 #
```python
class Student(object):
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称
        
s = Student() # 创建新的实例
s.name = 'Michael' # 绑定属性'name'
s.age = 25 # 绑定属性'age'
s.score = 99 # 报错，要绑定的属性'score'没有被放到__slots__中，所以不能绑定score属性，试图绑定score将得到AttributeError的错误
```

__slots__仅对当前类实例起作用，对继承的子类是不起作用的
```python
class GraduateStudent(Student):
    pass
        
g = GraduateStudent()
g.score = 9999 #不报错，子类没有定义__slots__，因此不受影响
```

如果子类也需要进行限制，则在子类中也定义__slots__，这样子类实例允许定义的属性就是自身的__slots__加上父类的__slots__
```python
class GraduateStudent01(Student):
	__slots__ = ('score') # 用tuple定义允许绑定的属性名称
	
g01 = GraduateStudent01()
g01.name = 'Michael' # 绑定属性'name'，父类定义允许绑定该属性
g01.age = 25 # 绑定属性'age'，父类定义允许绑定该属性
g01.score = 99 # 绑定属性'score'，子类定义允许绑定该属性
g01.city = 'DaLian' #报错，要绑定的属性'city'没有被放到父类和子类的__slots__中
```
