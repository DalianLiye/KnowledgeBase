[目录](../目录.md)

# 关于HTML
HTML是超文本标记语言(HyperText Markup Language)，用于创建网页，它是一种标准标记语言，不是一种编程语言
标记语言就是一套用来描述网页的标记标签(markup tag)
HTML文档包含了HTML标签及文本内容，也叫做web页面
当前标准为HTML5
HTML运行在浏览器上，由浏览器来解析，通过HTML可以建立WEB站点

# HTML页面组成
##示例

```html
<!DOCTYPE html>
<html>    
    <head>
        <meta charset="UTF-8">
        <title>我的第一个html</title>
    </head>
    <body>
        <h1>我的第一个标题</h1>
        <p>我的第一个段落。</p>
    </body>
</html>    
```

## HTML网页声明
\<!DOCTYPE\>声明位于HTML页面最开始位置，有助于浏览器中正确显示网页\
此标签可告知浏览器文档使用哪种HTML或XHTML规范\
\<!DOCTYPE html\>即表示声明该文档为HTML5文档，是HTML5标准网页声明,全称为Document Type HyperText Mark-up Language,是一条标示语言\
支持HTML5标准的主流浏览器都认识这个声明, 表示网页采用HTML5\
doctype声明是不区分大小写的, 以下方式均可：
```html
<!DOCTYPE html>
<!DOCTYPE HTML>
<!doctype html>
<!Doctype Html>
```

- HTML5
```html
<!DOCTYPE html>
```

- HTML 4.01
```html
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
```
在HTML 4.01 中, <!DOCTYPE> 声明需引用DTD(文档类型声明), 因为 HTML 4.01 是基于SGML(Standard Generalized Markup Language 标准通用标记语言)\
HTML 4.01 规定了三种不同的 <!DOCTYPE> 声明, 分别是：Strict、Transitional 和 Frameset\
HTML5不是基于SGML, 因此不要求引用 DTD

- XHTML 1.0
```html
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
```

## 元素

### html元素
HTML页面的根元素，是页面中最大的标签

### head元素
定义了文档的头部, 包含了文档的元(meta)数据，如 <meta charset="UTF-8"> 定义网页编码格式为UTF-8
对于中文网页需要使用 <meta charset="UTF-8"> 声明编码, 否则会出现乱码
有些浏览器(如360浏览器)会设置GBK为默认编码，则需要设置为 <meta charset="gbk">
在head标签中我们必须要设置title标签

### title元素
定义文档的标题, 让页面拥有一个属于自己的网页标题

### body元素
定义文档的主体, 包含文档的所有内容，如可见的页面内容\
页面内容基本都是放到body里面的, 即只有 \<body\>包含的部分才会在浏览器中显示

### 基本元素
每个网页都会有一个基本的结构标签(骨架标签), 页面内容会在这些基本标签上书写
基本结构标签即为上述的以下标签：
- \<html\>标签
- \<head\>标签
- \<title\>标签
- \<body\>标签

以下为html文档的最最基本的格式, 缺一不可
```html
<html>    
    <head>
        <title></title>
    </head>
    <body>
    </body>
</html>   
```


## HTML标签
HTML标记标签通常被称为HTML标签(HTML tag)\
HTML标签是由尖括号包围的关键词, 比如 \<html\>\
HTML标签通常是成对出现的, 比如 \<b\> 和 \</b\>\
标签对中的第一个标签是开始标签, 第二个标签是结束标签\
开始和结束标签也被称为开放标签和闭合标签\
<标签>内容</标签>

## HTML元素
HTML元素, 通常也叫HTML标签\
严格来讲, 一个 HTML元素包含了开始标签与结束标签, 如:
```html
<p>这是一个段落。</p>
```

# 关于Web浏览器
Web浏览器是用于读取HTML文件, 并将其作为网页显示\
浏览器并不是直接显示的HTML标签, 但可以使用标签来决定如何展现HTML页面的内容给用户

# 注意
## 编码
关于UTF-8的书写规范，"UTF-8"是标准的写法, 即大写字母 + 横杠"-", 应一律使用该种格式

## 后缀名
HTML文档可以有以下后缀名，它们没有任何区别
- XXXX.html(推荐使用)
- XXXX.htm(因最初的window操作系统只支持后缀名为三个字母导致)

## 空白字符
HTML中不支持以下符号, 它们都会被解析成一个空白字符
- 空格
- 回车
- 制表符

