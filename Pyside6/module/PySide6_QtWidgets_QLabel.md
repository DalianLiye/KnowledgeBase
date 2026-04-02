# 注
以下所有方法都在PySide6.QtWidgets.QLabel中


# alignment()
- **返回值**\
PySide6.QtCore.Qt.Alignment
- **说明**\
获取label内容的对齐方式\
label默认的对齐方式为: 水平左对齐，垂直居中


# setAlignment(arg__1)
- **参数**\
PySide6.QtCore.Qt.Alignment
- **说明**\
设置label的对齐方式


# buddy()
- **返回值**\
PySide6.QtWidgets.QWidget
- **说明**\
获取label的buddy, 如果没有则返回null


# setBuddy(arg__1)
- **参数**\
arg__1: PySide6.QtWidgets.QWidget
- **说明**\
当用户按下label指示的快捷键时，键盘焦点将转移到标签的好友QWidget上

好友机制仅适用于包含一个字符以"&"为前缀的文本的QLabel
此字符设置为快捷键
要取消以前设置的好友，请在好友设置为nullptr的情况下调用此函数

**例：**\
在对话框中，可创建两个数据input控件及其对应label, 通过设置几何布局，使两个label位于其数据input控件的左侧，例如：
```python
nameEdit = QLineEdit(self)
QLabel nameLabel = QLabel("Name:", self)
nameLabel.setBuddy(nameEdit)
phoneEdit = QLineEdit(self)
QLabel phoneLabel = QLabel("Phone:", self)
phoneLabel.setBuddy(phoneEdit)
```
当用户按 Alt+N 时，焦点将跳转到“名称”字段\
当用户按 Alt+P 时，焦点将跳转到“电话”字段


# clear()
- **返回值**\
void
- **说明**\
清空label的内容


# hasScaledContents()
- **返回值**\
bool
- **说明**\
用于获取label是否将缩放其内容以填充所有可用空间
如果该属性是true, label显示像素图, 它将缩放像素图以填充可用空间
默认是false


# setScaledContents(arg__1)
- **参数**\
arg__1: bool
- **说明**\
设置label是否ScaledContents


# hasSelectedText()
- **返回值**\
bool
- **说明**\
获取label是否有文本被选中
如果有任何文本被选中, 则返回true, 否则返回false
默认是false
- **注**\
label的textInteractionFlags属性至少要包含以下其中一个选项
  - TextSelectableByMouse
  - TextSelectableByKeyboard


# selectedText()
- **返回值**\
str
- **说明**\
获取被选中的文本\
如果没有选中的文本, 则返回空字符串\
默认是空字符串\
label的textInteractionFlags属性至少要包含以下其中一个选项
	TextSelectableByMouse
	TextSelectableByKeyboard
	
	
# selectionStart()
- **返回值**\
int
- **说明**\
获取label中第一个选定字符的索引, 如果未选择文本则返回-1\
label的textInteractionFlags属性至少要包含以下其中一个选项
	TextSelectableByMouse
	TextSelectableByKeyboard


# indent()
- **返回值**\
int
- **说明**\
获取label的文本缩进大小(单位：像素)\
以像素为单位保存标签的文本缩进
默认是-1

- **注**
1) 如果label显示文本，则indent会以下列方式生效
     - 如果alignment()为AlignLeft，则缩进应用于左边缘
     - 如果alignment()为AlignRight，则缩进应用于右边缘
     - 如果alignment()为AlignTop，则应用于上边缘
     - 如果alignment()为AlignBottom，则缩进应用于下边缘

2) 如果缩indent为负数，或未设置，则indent会以下列方式生效
     - 如果frameWidth()=0, 则有效缩进变为0
     - 如果frameWidth()>0, 则有效缩进变为widget font()的'x'字符宽度的一半


# setIndent(arg__1)
- **参数**\
arg__1: int
- **说明**\
设置label的缩进方式

# linkActivated(link)
- **参数**\
link: str
- **说明**\
当用户单击链接时发出此信号\
anchor引用的URL在链接中传递


# linkHovered(link)
- **参数**\
link: str
- **说明**\
当用户悬停在链接时发出此信号\
anchor引用的URL在链接中传递


# margin()
- **返回值**\
int
- **说明**\
获取label的边距宽度\
默认边距为 0
- **注**\
边距是边框的最内层像素与内容最外层像素之间的距离\


# setMargin(arg__1)
- **参数**\
arg__1: int
- **说明**\
设置label的边距

# movie()
- **返回值**\
PySide6.QtGui.QMovie
- **说明**\
获取lable move的指针, 如果未设置, 则返回 nullptr


# setMovie(movie)
- **参数**\
movie: PySide6.QtGui.QMovie
- **说明**\
设置label的Movie，label不是movie的owner\
好友快捷方式(如果有)已禁用


# openExternalLinks()
- **返回值**\
bool
- **说明**\
指定QLabel是否应使用openUrl()自动打开链接，而不是发出linkActivated()信号
默认是false
- **注**\
label的textInteractionFlags属性至少要包含以下其中一个选项
	LinksAccessibleByMouse
	LinksAccessibleByKeyboard


# setOpenExternalLinks(open)
- **参数**\
open: bool
- **说明**\
设置label是否OpenExternalLinks


# picture()
- **返回值**\
PySide6.QtGui.QPicture
- **说明**\
获取label的picture


# setPicture(arg__1)
- **参数**\
arg__1: PySide6.QtGui.QPicture
- **说明**\
设置label的picture


# pixmap()
- **返回值**\
PySide6.QtGui.QPixmap
- **说明**\
获取label的像素地图\
设置pixmap会清除任何以前的内容\
如果有好友快捷方式，它已禁用\


# setPixmap(arg__1)
- **参数**\
arg__1: PySide6.QtGui.QPixmap
- **说明**\
设置label的Pixmap


# setSelection(arg__1, arg__2)
- **参数**\
arg__1: int
arg__2: int
- **说明**\
设置label选中文本的范围
- **注**\
label的textInteractionFlags属性至少要包含以下其中一个选项
	TextSelectableByMouse
	TextSelectableByKeyboard


# setNum(arg__1)
- **参数**\
arg__1: double
- **说明**\
该方法是重载载过来的\
将label内容设置为包含双精度数字的文本表示形式的纯文本\
如果双精度的字符串表示形式与标签的当前内容相同，则不执行任何操作\
好友快捷方式(如果有)已禁用\


# text()
- **返回值**\
str
- **说明**\
获取label的文本信息


# setText(arg__1)
- **参数**\
arg__1: str
- **说明**\
设置label的文本\
如果没有则返回空字符串,重新设定文本时，上一次设定的文本会被覆盖\
文本将被解释为纯文本或富文本，具体取决于文本格式设置 setTextFormat()\
默认是AutoText

- **注**\
QLabel会自动检测文本的格式\
如果已设置好友，则会从新文本更新好友助记键\
请注意，QLabel 非常适合显示小型富文本文档\
例如从标签的调色板和字体属性获取其文档特定设置（字体、文本颜色、链接颜色）的小型文档
对于大型文档，请改用只读模式下的 QTextEdit。QTextEdit还可以在必要时提供滚动条\
如果文本包含富文本，此函数将启用鼠标跟踪


# textFormat()
- **返回值**\
PySide6.QtCore.Qt.TextFormat
- **说明**\
该方法定义了label文本的格式\
值是TextFormat枚举类型\
默认是AutoText


# setTextFormat(arg__1)
- **返回值**\
arg__1: TextFormat
- **说明**\
设置label的textFormat


# textInteractionFlags()
- **返回值**\
PySide6.QtCore.Qt.TextInteractionFlags
- **说明**\
该方法定义了当有交互动作时，QLabel该如何响应\
如果flags包含LinksAccessibleByKeyboard，则焦点策略是被自动设置为StrongFocus\
如果flags包含TextSelectableByKeyboard，则焦点策略是被自动设置为ClickFocus\
默认是LinksAccessibleByMouse



# setTextInteractionFlags(flags) 
- **参数**\
flags: PySide6.QtCore.Qt.TextInteractionFlags
- **说明**\
设置label的TextInteractionFlags\
设置后，上次设置的值会被清空


PySide6.QtCore.Qt.TextInteractionFlag.LinksAccessibleByKeyboard
PySide6.QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse
PySide6.QtCore.Qt.TextInteractionFlag.NoTextInteraction
 PySide6.QtCore.Qt.TextInteractionFlag.TextBrowserInteraction
PySide6.QtCore.Qt.TextInteractionFlag.TextEditable
PySide6.QtCore.Qt.TextInteractionFlag.TextEditorInteraction
PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByKeyboard
PySide6.QtCore.Qt.TextInteractionFlag.TextSelectableByMouse



# wordWrap()
- **返回值**\
bool
- **说明**\
获取label是否wordwrap\
如果返回true，则说明label会在文本合适处自动换行，否则就不会\
例如，如果label的文本很长，则文本会随着窗体的大小伸缩而自当换行，以适应窗体大小\
默认情况下，是不换行


# setWordWrap(flag)
- **返回值**\
flag – bool
- **说明**\
设置lable是否wordwrap
```python
label = QLabel()
label.setText("long text...")
label.setWordWrap(True)
```