[目录](../目录.md)

# 定义
\<dl\>标签用于定义描述列表

自定义列表常用于对术语或名词进行解释和描述\
定义列表的列表项前没有任何项目符号\

- **dl**\
代表单词Definition List，意为定义列表
- **dt**\
代表单词Definition Term，意为定义术语
- **dd**\
代表单词Definition Description，意为定义描述

# 使用
\<dl\>标签会与\<dt\>(定义项目/名字)和\<dd\>(描述每一个项目/名字)一起使用\
\<dl\>中只能嵌套\<dt\>和\<dd\>,不能有其他标签或纯文本\
\<dt\>和\<dd\>的个数没有限制，经常是一个\<dt\>对应多个\<dd\>\
\<dt\>和\<dd\>里面可以放任何标签

# 示例
```html
<h4>自定义列表</h4>
<dl>
    <dt>总项目1</dt>
        <dd>项目1</dd> 
        <dd>项目2</dd>
    <dt>总项目2</dt>
        <dd>项目3</dd> 
        <dd>项目4</dd>
</dl>
```