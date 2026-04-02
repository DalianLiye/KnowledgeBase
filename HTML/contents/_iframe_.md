[目录](../目录.md)

# 定义
标记一个内联框架\
一个内联框架被用来在当前HTML文档中嵌入另一个HTML文档\
iframe代表单词Inline frame, 意为内联框架

# 使用
可把需要的文本放置在\<iframe\>和\</iframe\>之间, 这样就可以应对不支持\<iframe\>的浏览器\
请使用CSS为\<iframe\>(包括滚动条)定义样式

# 属性
## height属性
**定义：**\
规定 <iframe> 的高度\
**值：**\
任意数字，单位是px

## width属性
**定义：**\
规定 <iframe> 的宽度\
**值：**\
任意数字，单位是px

# name属性
**定义：**\
规定<iframe>的名称\
**值：**\
任意自定义名称

# sandbox属性
**定义：**\
对<iframe>的内容定义一系列额外的限制\
**值：**
-  ""
- allow-forms
- allow-same-origin
- allow-scripts
- allow-top-navigation

# seamless属性
**定义：**\
规定<iframe>看起来像是父文档中的一部分(没有边框和滚动条)\
seamless属性是一个布尔属性\
**值：**\
没有具体值，直接在写属性名"seamless"
```html
<iframe src="demo_iframe.htm" width="200" height="200" seamless></iframe>
```
**注：**\
只有Chrome和Safari 6支持\<iframe\> 标签的seamless属性

## src属性
**定义：**\
规定在\<iframe\>中显示的HTML文档的URL\
**值：**\
HTML文档的URL地址

## srcdoc属性
**定义：**\
规定页面中的HTML内容显示在\<iframe\>中\
**值：**\
一些HTML代码

## 全局属性
\<iframe\>标签支持HTML的全局属性

## 事件属性
\<iframe\>标签支持HTML的事件属性

# 示例
```html
<iframe src="http://www.iframe.com"></iframe>
```