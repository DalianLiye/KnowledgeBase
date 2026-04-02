[目录](../目录.md)

# Qt Creator #
可以使用Qt Creator创建ui文件，来设计ui界面\
**URL：**\
https://doc.qt.io/qtcreator/creator-using-qt-designer.html

# 两种方式 #
使用UI文件, 有两种方式
- **生成python类**\
    将生成的.ui文件生成为python代码，并嵌入到应用程序中\
    该种方式需要借助工具pyside2-uic,对.ui文件进行转换,生成一个.py文件
  
    ```python
    pyside2-uic mainwindow.ui > ui_mainwindow.py
    ```

    然后在应用程序中，需要导入该生成的文件

    ```python
    from ui_mainwindow import Ui_MainWindow
    ```
    全体代码:
    ```python
    import sys
    from PySide2.QtWidgets import QApplication, QMainWindow
    from PySide2.QtCore import QFile
    from ui_mainwindow import Ui_MainWindow

    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)

    if __name__ == "__main__":
        app = QApplication(sys.argv)

        window = MainWindow()
        window.show()

        sys.exit(app.exec_())
    ```
    **注:** 
    该种方式需要每次修改UI文件时，都要执行下pyside2-uic操作

- **直接加载.ui文件**\
    直接加载.ui文件需要引入QtUiTools模块
    ```python
    from PySide2.QtUiTools import QUiLoader

    ...
    ui_file = QFile("mainwindow.ui")
    ui_file.open(QFile.ReadOnly)
    ...
    loader = QUiLoader()
    window = loader.load(ui_file)
    window.show()
    ...
    ```

    全体代码:
    ```python
    import sys
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import QFile, QIODevice

    if __name__ == "__main__":
        app = QApplication(sys.argv)

        ui_file_name = "mainwindow.ui"
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open {}: {}".format(ui_file_name, ui_file.errorString()))
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)
        window.show()

        sys.exit(app.exec_())
    ```
