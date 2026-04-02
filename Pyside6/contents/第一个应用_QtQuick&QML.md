[目录](../目录.md)

# 关于QML #
QML是一个声明性语言，作用跟CSS样式差不多\
通过QML单独放到一个文件，实现了UI和代码的分离\
在QML中，各UI对象之间的关系体现为树状关系，且每个对象都有自己的属性(跟XML类似)

# 代码 #
**view.qml**
```qml
import QtQuick 2.0

Rectangle {
    width: 200
    height: 200
    color: "green"

    Text {
        text: "Hello World"
        anchors.centerIn: parent
    }
}
```
**main.py**
```python
from PySide2.QtWidgets import QApplication
from PySide2.QtQuick import QQuickView #说明1
from PySide2.QtCore import QUrl 

app = QApplication([])
view = QQuickView()
url = QUrl("view.qml")

view.setSource(url)
view.setResizeMode(QQuickView.SizeRootObjectToView) #说明2
view.show()
app.exec_()
```

# 说明 #
- **说明1**\
使用QML，必须要引入QtQuick.QQuickView模块和QtCore.QUrl模块\
QtCore.QUrl模块用于引用QML文件\
QtQuick.QQuickView模块用于设置QUrl(通过setSource()方法)，使QML生效

- **说明2**\
设定该属性后，GUI里的内容会随着边框的大小变化而不断调整位置
