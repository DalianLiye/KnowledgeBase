# 关于QWidget类 #
QWidget类是所有UI对象的基类


# Slots #
- **def setEnabled (arg__1)**\
  **路径：** PySide6.QtWidgets.QWidget.setEnabled(arg__1)\
  **参数：** bool, 默认值true\
  **说明：**\
  用于设定该widget是否启用\
  通常，如果一个widget是启用状态时，它能够接受来自键盘和鼠标的事件;相反，处于禁用状态时就不能(QAbstractButton除外)\
  一些widget处于禁用状态时，显示的样式也不尽相同，比如按钮在禁用状态时是灰色的\
  如果需要知道widget何时启用或禁用，可使用带有EnabledChange类型的changeEvent()

  禁用父widget的同时，也会隐式的禁用其所有子widget\
  当父widget从禁用状态变为启用状态时，则其子widget也会变为启用状态(若子widget被显式的设定为禁用状态，则其依然是禁用的状态)\
  如果一个子widget不是一个window，而且它的父widget处于禁用状态，则无法设定该widget为启用状态

