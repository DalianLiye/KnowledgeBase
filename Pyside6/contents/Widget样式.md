[目录](../目录.md)

# 关于Widget样式 #
Qt Widgets应用会使用所在平台默认的主题，当然这些是可以定制的

可以为每一个Widget指定不同的样式，但一个一个的指定Widget样式，会很麻烦\
可以使用QSS(Qt Style Sheets)来做到批量指定样式，类似于CSS那样

**QSS URL:**\
https://doc.qt.io/qt-5/stylesheet-reference.html

**QSS样例URL:**\
https://doc.qt.io/qt-5/stylesheet-examples.html

```python
import sys
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    app = QApplication()
    w = QLabel("This is a placeholder text")
    w.setAlignment(Qt.AlignCenter)
    w.setStyleSheet("""
        background-color: #262626;
        color: #FFFFFF;
        font-family: Titillium;
        font-size: 18px;
        """)
    w.show()
    sys.exit(app.exec_())
```


# QSS #
QSS全称为：Qt Style Sheets\
一个QSS文件类似于一个CSS文件

可以在QSS中指定组件的样式，也可通过可选的方式指定其的objectName值，将样式适用于指定范围的组件\
以下QSS中，第一个指定的是全体QLabel("label01"和"label02")的样式，第二个仅指定objectName是"title"的QLabel("label01")的样式

QSS代码：
```CSS
QLabel {
    background-color: red;
}

QLabel#title {
    font-size: 20px;
}
```
python代码：
```python
...
label01 = QLabel("label01")
label01.setObjectName("title")

label02= QLabel("label02")
...
```

通过setStyleSheet()方法来读取QSS文件
```python
if __name__ == "__main__":
    app = QApplication()

    w = Widget()
    w.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec_())
```

全体代码：
```python
import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *

class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        menu_widget = QListWidget()
        for i in range(10):
            item = QListWidgetItem("Item {}".format(i))
            item.setTextAlignment(Qt.AlignCenter)
            menu_widget.addItem(item)

        text_widget = QLabel("_placeholder")
        button = QPushButton("Something")

        content_layout = QVBoxLayout()
        content_layout.addWidget(text_widget)
        content_layout.addWidget(button)
        main_widget = QWidget()
        main_widget.setLayout(content_layout)

        layout = QHBoxLayout()
        layout.addWidget(menu_widget, 1)
        layout.addWidget(main_widget, 4)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication()

    w = Widget()
    w.show()

    with open("style.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    sys.exit(app.exec_())
```

style.qss
```CSS
QListWidget {
    color: #FFFFFF;
    background-color: #33373B;
}

QListWidget::item {
    height: 50px;
}

QListWidget::item:selected {
    background-color: #2ABf9E;
}

QLabel {
    background-color: #FFFFFF;
    qproperty-alignment: AlignCenter;
}

QPushButton {
    background-color: #2ABf9E;
    padding: 20px;
    font-size: 18px;
}
```
**注:** 由于QSS指定的是全局的样式，QSS文件在改动时，一定要注意整体的式样是否有影响