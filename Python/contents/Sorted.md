[目录](../目录.md)

# 关于Sorted #
Python内置的sorted()函数就可以对list进行排序\
sorted()也是一个高阶函数。用sorted()排序的关键在于实现一个映射函数，也就是key函数

# 使用示例 #
- 数字排序
```python
sorted([36, 5, -12, 9, -21])  #输出：[-21, -12, 5, 9, 36]
```

- 接收一个key函数来实现自定义的排序
key指定的函数将作用于list的每一个元素上，并根据key函数返回的结果进行排序
```python
sorted([36, 5, -12, 9, -21], key=abs)  #输出：[5, 9, -12, -21, 36]
```

- 字符串排序
默认情况下，对字符串排序，是按照ASCII的大小比较的，由于'Z' < 'a'，结果，大写字母Z会排在小写字母a的前面
```python
sorted(['bob', 'about', 'Zoo', 'Credit'])  #输出：['Credit', 'Zoo', 'about', 'bob']
```

- 字符串排序(忽略大小写)
```python
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower)  #输出：['about', 'bob', 'Credit', 'Zoo']
```

- 字符串排序(忽略大小写，且反方向)
```python
sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower, reverse=True)  #输出：['Zoo', 'Credit', 'bob', 'about']
```
