[目录](../目录.md)

# href属性
href是Hypertext Reference的缩写, 表示超文本引用, 是引用\
用来建立当前元素和文档之间的链接, 常用的有：link、a
```html
<link href="reset.css" rel=”stylesheet“/>
```
浏览器会识别该文档为css文档, 并行下载该文档, 并且不会停止对当前文档的渲染处理\
这也是建议使用link, 而不采用 @import 加载css的原因

# src属性
src是source的缩写, src的内容是页面必不可少的一部分, 是引入
src指向的内容会嵌入到文档中当前标签所在的位置
常用的有：img、script、iframe

```html
<script src="script.js"></script>
```
当浏览器解析到该元素时, 会暂停浏览器的渲染, 直到该资源加载完毕\
这也是将js脚本放在底部而不是头部得原因

# 总结
src用于替换当前元素, 即src指定的资源是要显示到页面中的, 是页面必不可少的一部分, 是引入
href用于在当前文档和引用资源之间建立联系，即建立与该页面的关联，是引用