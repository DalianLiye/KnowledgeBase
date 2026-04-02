[目录](../目录.md)

# 关于信号和槽 #
信号(Signals)和槽(slots)是QT独有的特性，它们可以让界面上的各个组件，或组件和后台代码之间进行交互

# 代码 #
```python
#!/usr/bin/python

import sys
from PySide2.QtWidgets import QApplication, QPushButton #使用Button，需要导入QPushButton模块
from PySide2.QtCore import Slot #使用信号和槽，需要导入Slot模块

@Slot()
def say_hello(): #@Slot()表示修饰器，用于说明该函数是一个槽，最好写上它，否则可能会出现一些不可预知的错误
    print("Button clicked, Hello!")

app = QApplication(sys.argv)
button = QPushButton("Click me")
button.clicked.connect(say_hello) #说明1
button.show()
app.exec_()
```

# 说明 #
- **说明1**\
QPushButton有一个预先定义号的信号"clicked"，每当按钮被点击，它会被触发\
将connect设置为对应的槽(say_hello)，即表示将信号"clicked"与槽(函数say_hello)进行连接




