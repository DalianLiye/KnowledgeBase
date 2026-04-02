# 关于QButtonGroup类 #
QButtonGroup提供了一个用于管理一组button widget的容器\
QButtonGroup是一个抽象的容器，用于放置button widgets, 并管理其中各button的状态\
QButtonGroup并不会在UI界面上显示出来,这点与QGroupBox不一样

在一个排他性的button group里, 选中其中一个button，则其他button都会被关闭\
默认情况下，一个button group是排他性的\
button group里的button类型，一般是Push Button，CheckBox或者Radio Button\
当创建一个排他性的button group时, 要确保group内有一个button的初始状态是选中的状态

可以通过addButton()和removeButton()函数，将按钮加入或从QButtonGroup删除\
如果该QButtonGroup是排他的，可以通过checkedButton()函数获取当前正在选中的按钮\
如果按钮被选中，则会发送信号buttonClicked()\
通过buttons()函数获取该QButtonGroup下的所有按钮

此外，QButtonGroup可以将button和数字进行映射\
可以通过setId()函数来给button设定一个id,及通过id()函数获取button对应的id\
可以通过checkedId()函数获取当前被点击按钮的id\
有一个重载的信号buttonClicked(),它可以发送按钮的id\
如果QButtonGroup内没有这个按钮，其id为-1\
这个映射机制的目的是为了简化UI中的枚举值的使用
