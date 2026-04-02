[目录](../目录.md)

# 定义
为页面上的所有的相对链接规定默认URL或默认目标


# 使用
- 在一个文档中，最多能使用一个\<base\>元素
- \<base\>标签必须位于\<head\>元素内部，且最好排在\<head\>元素中第一个元素的位置，这样\<head\>标签内的其他元素使用\<base\>元素中的信息了
- 如果使用了<base>标签，以下属性至少具备一个或两个都具备
    - href
    - target

**注：** 绝对链接是不会使用\<base\>标签的


# 属性
## href属性
**定义:**\
URL，规定页面中所有相对链接的基准URL\
**值:**\
URL


## target属性
**定义:**\
规定页面中所有的超链接和表单在何处打开\
该属性会被每个链接中的target属性覆盖\
HTML5已经不再支持Frames和framesets，因此，iframes通常使用_parent, _top 和framename值\
**值:**
```html
<base target="_blank|_self|_parent|_top|framename">
```
\_blank: 在新窗口中打开被链接文档\
\_self: 默认。在相同的框架中打开被链接文档\
\_parent: 在父框架集中打开被链接文档\
\_top: 在整个窗口中打开被链接文档\
framename: 在指定的框架中打开被链接文档

## 全局属性
<base>标签支持HTML的全局属性

## 事件属性
<base>标签不支持任何的事件属性

# 示例
```html
<head>
　　<base href="www.test.com/" target="_blank">
</head>

<img src="logo1.jpg"> <!-- src的路径最终为www.test.com/logo1.jpg -->
<a href="logo2.jpg"> <!-- href的路径最终为www.test.com/logo2.jpg，属性值为"_blank" -->
<a href="logo3.jpg" target="_self"> <!-- src的路径最终为www.test.com/logo3.jpg，但由于自定义了target属性，因此<base>标签的属性被覆盖，属性值为"_self" -->
```
 
