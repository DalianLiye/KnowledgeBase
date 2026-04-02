# 关于QRadioButton类 #
RadioButton是一种可选的按钮，它可以切换开关\
用于为用户提供"多选一"的操作\
在一组RadioButton中，一次只能选中一个\
但只有同一QButtonGroup的RadioButton才具有排他性，不同QButtonGroup的RadioButton互不干扰

- **信号和槽**\
    当任何一个RadioButton进行开或关的转换时, 它会发出toggled()信号，然后执行该信号对应的槽\
    当某一个RadioButton进行开或关的转换时，它会发出isChecked()信号，然后执行该信号对应的槽

- **显示**\
    RadioButton可以像QPushButton那样，显示文本，或以可选的方式显示小图标\
    通过setIcon()函数设置小图标，通过构造函数，或者setText()函数设置文本\

- **热键**\
    可以为按钮设置热键, 就是在Name前加一个"&",具体方式如下:
    ```python
    button = QRadioButton("Search from the &cursor", self) #热键： alt + c
    ```