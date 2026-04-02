# 关于QPushButton类 #
按钮是UI中最常用的widget之一\
通过点击按钮可以让计算机执行一些动作\
典型的按钮用例，包括诸如"确定"，"使用", "取消", "关闭", "是", "否"和"帮助"等

- **热键**\
    可以为按钮设置热键, 就是在Name前加一个"&",具体方式如下:
    ```python
    button = QPushButton("&Download", self) #热键: Alt+D
    ```
    如果"&"本身就是按钮文本的一部分，可以双写该字符
    ```python
    button = QPushButton("&&Download", self) #按钮的文本为"&Download",但不会有热键"Alt+D"
    ```

- **显示**\
按钮可以显示为带有文本的label，也可通过可选的方式显示为小图标\
可以通过构造函数设置，或创建对象后通过setText()和setIcon()函数设置\
如果按钮被禁用，将根据GUI样式来显示text和icon的外观，使按钮看起来"禁用"\
按钮是矩形的，通常按钮的文本内容描述了点击该按钮时，要执行的对应动作\
**注：** 在macOS系统，如果一个按钮的长度小于50或高小于30，则按钮的边角会从圆形变成方形,可以通过使用setMinimumSize()函数来解决该问题

- **信号和槽**\
当鼠标，空格键或键盘热键点击了按钮时,按钮会发出信号"clicked()"(Signal),并执行连接该信号的相关动作(槽Slots)\
按钮也提供了一些其他的信号，比如pressed()和released()

- **光标**\
当打开对话框时，光标会被默认的停留在按钮上，这样打开对话框后直接按回车就可以点击它了\
可以通过setAutoDefault()方法来改变设置\
自动默认按钮会在按钮周围保留一定空间，用于显示默认键标识\
可以通过setAutoDefault(False)的方式来取消

- **使用场景**
    - **使用按钮的场景：**
      - 当用户执行点击操作后，需要应用或窗体执行一个动作时
      - 当widget是一个矩形，且为有文本的label时

    - **不使用按钮的场景：**
      - widget小，且为方形，可以改变窗体的状态而不是执行某一动作时，它们则是工具按钮(tool button)而非命令按钮(Push Button或Command Button)，Qt有专门的类来定义工具按钮
      - 如果需要切换行为(请参见setCheckable())，或者需要一个按钮，在按下时自动重复激活信号，如滚动条中的箭头(请参见setAutoRepeat())，则命令按钮可能不是您想要的
        如有疑问，请使用工具按钮

- **其他按钮**\
命令按钮的变体是菜单按钮,它不仅提供一个命令，还提供多个命令\
当单击它时，会弹出一个选项菜单\
使用方法setMenu()方法将弹出菜单与按钮关联\
其他的按钮，还包括了Radio(QRadioButton)和CheckBox按钮(QCheckBox)

- **QAbstractButton类**\
在Qt，QAbstractButton类是按钮的基类\
它提供了大部分的模型和API，而QPushButton提供了GUI的逻辑\
可参照QAbstractButton查看更多的关于API的信息