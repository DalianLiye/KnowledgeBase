[目录](../目录.md)

# 代码 #
```python
import sys
from PySide2.QtWidgets import QApplication, QLabel #说明1

app = QApplication(sys.argv) #说明2
label = QLabel("<font color=red size=40>Hello World!</font>") #说明3
label.show() #说明4
app.exec_() #说明5
```

# 说明 #
- **说明1**\
只要程序中，使用了Widgets组件，就必须导入PySide2.QtWidgets模块

- **说明2**\
创建application实例时，需创建一个QApplication对象\
如果程序是通过命令行的方式启动的，则创建QApplication对象时可接收命令行的参数，比如:

    **命令行：**
    ```cmd
    python demo.py test1 test2 test 3
    ```

    **python脚本：**
    ```python
    ...
    app = QApplication(sys.argv)  
    print(sys.argv[1]) #输出：test1
    ...
    ```
    **注：** sys.argv是一个包含各个参数的列表，列表第一个元素是python文件本身，即demo.py，然后依次是各个参数

    一般情况下不设置参数，因为GUI程序往往是通过执行exe文件启动的，很少通过命令行启动，因此可以像下面这样,干脆设置成空
    ```python
    ...
    app = QApplication([]) 
    ...
    ```

- **说明3**\
创建QLabel，一个QLabel就是一个widget。它可以显示文本和图片\
它可以像HTML那样按照指定的样式显示文本

- **说明4**\
widget对象调用show()方法，表示调用该方法的widget会显示在应用上

- **说明5**\
application对象调用exec_()方法，表示启动应用\
GUI程序的执行其实就是一个无限循环\
如果不执行该方法，程序执行时它会执行完一遍就结束，效果上看就是一闪一过就结束了\
执行该方法后，会让程序会进入无限循环，其实就是让这一闪一过的效果一直持续下去\
这样就给人一种代码一直在启动的感觉

