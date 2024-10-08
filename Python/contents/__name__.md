[目录](../目录.md)

# 关于__name__ #
\_\_name__是系统内置变量(前后缀有双下划线"_"),用于标识模块名\
当前模块是主模块(即调用其他模块的模块)，则此模块名字就是__main__\
若此模块是被import的，则此模块名字为文件名字(不加后面的.py)

demo1.py
```python
def printName():
	print("demo1的__name__为：" + __name__)
```

demo2.py
```python
import demo1

if __name__ == '__main__':
	printName()
	print("demo2的__name__为：" + __name__)
```

pycharm中右键点击demo2.py执行，输出结果为：\
demo1的__name__为：demo1\
demo2的__name__为：__main__
