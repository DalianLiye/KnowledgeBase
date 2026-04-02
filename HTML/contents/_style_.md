[目录](../目录.md)

# 定义
\<style\>标签定义HTML文档的样式信息\
通过\<style\>标签, 可以规定在浏览器中如何呈现HTML文档

# 使用
在\<style\>元素中可直接添加样式来渲染HTML文档
每个HTML文档能包含多个\<style\>标签

**注：**
- 如需链接外部样式表，请使用\<link\>标签
- 如果没有使用"scoped"属性，则每一个\<style\>标签必须位于head头部区域
- 理论上, \<style\>标签可以放在其他任何位置, 如\<body\>标签内，但一般都是放到\<head\>标签中, 通过此种方式, 可以方便控制当前整个页面中的元素样式设置

# 属性
## media属性
为样式表规定不同的媒体类型,如"media_query"

## scoped属性
如果使用该属性, 则样式仅仅应用到style元素的父元素及其子元素, 如"scoped"

## type属性
规定样式表的 MIME 类型, 如"text/css"
```html
<head>
    <style type="text/css">
        body {background-color:yellow}
        p {color:blue}
    </style>
</head>
```

## 全局属性
\<style\>标签支持HTML的全局属性

## 事件属性
\<style\>标签支持HTML的事件属性

