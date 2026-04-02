[目录](../目录.md)

# 代码 #
```python
import sys
from PySide2.QtWidgets import (QLineEdit, QPushButton, QApplication,
    QVBoxLayout, QDialog)

class Form(QDialog): #可以创建任何一个类，来继承PySide2.widgets

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        self.setWindowTitle("My Form") #用于给Form设定title
        self.edit = QLineEdit("Write my name here")
        self.button = QPushButton("Show Greetings")

        layout = QVBoxLayout() #创建layout，可以管理界面排版
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
 
        self.setLayout(layout)

        self.button.clicked.connect(self.greetings)

    def greetings(self):
        print ("Hello %s" % self.edit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
```
