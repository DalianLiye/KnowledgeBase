[目录](../目录.md)

# 关于filter #
Python内建的filter()函数，用于从一个序列中筛出符合条件的元素\
filter()的作用是。由于filter()使用了惰性计算，所以只有在取filter()结果的时候，才会真正筛选并每次返回下一个筛出的元素\
filter()函数返回的是一个Iterator，也就是一个惰性序列，所以要强迫filter()完成计算结果，需要用list()函数获得所有结果并返回list

# filter()与map()比较 #
- **相同点：**\
  都是接收一个函数和一个序列
- **不同点：**\
  filter()把传入的函数依次作用于每个元素，然后根据返回值是True还是False决定保留还是丢弃该元素\
  filter()函数的作用在于筛选，只返回符合条件的list元素，即list的元素个数在filter前后会有变化\
  map()函数的作用在于将list每个元素传入函数进行处理

 

# 使用示例 #
删掉list中的偶数，只保留奇数
```python
def is_odd(n):
    return n % 2 == 1

print(list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15])))  #输出: [1, 5, 9, 15]　
```

把一个序列中的空字符串删掉
```python
def not_empty(s):
    return s and s.strip()
    
print(list(filter(not_empty, ['A', '', 'B', None, 'C', '  '])))# 输出: ['A', 'B', 'C']
```
