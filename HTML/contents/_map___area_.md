[目录](../目录.md)

# 定义
\<map\>标签用于客户端图像映射\
图像映射指带有可点击区域的一幅图像

# 使用
HTML4.01与HTML5之间的差异\
在 HTML5 中, 如果id属性在\<map\>标签中指定, 则你必须同样指定name属性


# 属性
## usemap属性
\<img\>中的usemap属性可引用\<map\>中的id或name属性(取决于浏览器), 所以应同时向\<map\>添加id和name属性

## name属性
必需, 为image-map规定的名称, 它规定了图像映射的名称\
name属性与<img>标签的usemap属性相关联, 以创建图像与映射之间的关系\
所有主流浏览器都支持 name 属性
```html
<map name="mapname"> ...
...
<img usemap="#mapname"> ... <!-- mapname前要加上"#"号 -->
```

## 全局属性
\<map\>标签支持全局属性，查看完整属性表HTML全局属性

## 事件属性
\<map\>标签支持所有HTML事件属性

# area元素
area元素永远嵌套在map元素内部\
area元素可定义图像映射中的区域
```html
<img src="图片URL" width="200" height="200" alt="替换文本" usemap="#mapname">

<map name="mapname">
　　<area shape="rect" coords="0,0,82,126" href="sun.htm" alt="Sun">
　　<area shape="circle" coords="90,58,3" href="mercur.htm" alt="Mercury">
　　<area shape="circle" coords="124,58,8" href="venus.htm" alt="Venus">
</map>
```




