[目录](../目录.md)

# 关于Python解释器 #
由于Python语言从规范到解释器都是开源的，所以理论上任何人都可以编写Python解释器来执行Python代码\
目前存在以下几种主流的Python解释器

# CPython #
CPython是官方版本的解释器，是使用最广的Python解释器\
CPython是用C语言开发的，所以叫CPython\
在命令行下运行python就是启动CPython解释器

# IPython #
IPython是基于CPython之上的一个交互式解释器，即IPython只是在交互方式上有所增强，但执行代码的功能和CPython完全一样\
好比很多国产浏览器虽然外观不同，但内核其实都是调用了IE\
CPython用>>>作为提示符，而IPython用In [序号]:作为提示符

# PyPy #
PyPy是另一个Python解释器，它的目标是执行速度\
PyPy采用JIT技术，对Python代码进行动态编译而不是解释，所以可显著提高Python代码的执行速度\
绝大部分Python代码都可以在PyPy下运行，但是PyPy和CPython有一些是不同的,这导致相同代码在两种解释器下的执行结果不同\
因此如果代码需要在Pypy下运行，需事先了解PyPy和CPython的不同点

# Jython #
Jython是运行在Java平台上的Python解释器，可以直接把Python代码编译成Java字节码执行\
也就是说，python代码经过Jython编译后，可直接在JVM上运行

# IronPython #
IronPython和Jython类似，只不过IronPython是运行在微软.Net平台上的Python解释器，可以直接把Python代码编译成.Net的字节码\
也就是说，python代码经过IronPython编译后，可直接在.NET平台上运行
