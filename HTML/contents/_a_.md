[目录](../目录.md)

# 定义
该标签用于定义网页中的链接，作用是从一个页面链接到另一个页面\
a代表单词anchor，意为锚

# 使用
在所有浏览器中，链接的默认外观如下
- 未被访问的链接带有下划线而且是蓝色的
- 已被访问的链接带有下划线而且是紫色的
- 活动链接带有下划线而且是红色的

**注:**
- 如果没有使用href属性, 则不能使用hreflang, media, rel, target以及type属性
- 通常在当前浏览器窗口中显示被链接页面, 除非规定了其他 target
- 请使用CSS来改变链接的样式

# 属性

## download属性
**定义:**\
指定下载链接\
**值:**\
要下载文件的路径
```html
<a href="/images/logo1.png" download="/images/logo2.png">
```
**注:**
- 因为下载肯定要有一个URL, 因此href属性必须在\<a\>标签中指定
- download属性同样可以指定下载文件的名称\
例如: \href="/images/logo1.png"是文件在服务器上的路径, download也可以指定为"/images/cat.png","/images/dog.png"(文件名前必须要有/images/), download指定的文件名是下载后重命名后的文件名
- 文件名称没有限定值, 浏览器会自动在文件名称末尾添加该下载文件的后缀 (.img, .pdf, .txt, .html, 等)\
例如: download="/images/logo2.png"可以写成download="/images/logo2", 下载时会自动根据href属性指定文件的后缀名自动追加".png"
- 该属性需要下载资源是同源的, 即该下载资源不能是其他网站的，只能是本站的

## href属性
**定义:**\
指定链接的地址\
href代表单词hyper reference，意为超链接\
它是\<a\>元素最重要的属性\
**值:**
```html
<a href="https://www.baidu.com">这是一个baidu链接</a>
```

### 链接分类
#### 外部链接
访问网站外部的URL
```html
<a href="www.baidu.com">百度</a>
<a href="www.sina.com">新浪</a>
<a href="www.souhu.com">搜狐</a>
```
#### 内部链接
访问网站内部的URL
```html
<a href="previous.html">上一页</a>
```
#### 空链接
当链接的URL还没有确定时，可以选择空链接，即href属性设置为"#"
```html
<a href="#"></a>
<!-- 尚不知道链接URL时，可暂时用#代替-->
```
#### 下载链接
如果href里面地址是一个文件或者压缩包，会下载这个文件
```html
<a href="file.zip">点击此处，会下载file.zip文件</a>
```
#### 网页元素链接
网页中的各种网页元素，如文本，图像，表格，音频，视频等都可以添加超链接
```html
<a href="wwww.baidu.com"><img src="logo.jpg"/></a>
<!-- 点击logo图标，页面会跳转至百度页面-->
```
#### 锚点链接
锚点链接用于快速定位到页面中的某个位置\
在链接文本的href属性中，设置属性值为 "#目标位置标签id" 
```html
<a href="#标题id">点击此处，页面快速定位到标题处</a>
...
...
<h3 id="标题id">标题</h3>
```

## target属性
**定义:**\
用于指定链接页面的打开方式，其中_self为默认值\
**值:**\
属性有以下固定值：
- _self：在当前页面打开
- _blank：在新的页面打开

## 全局属性
\<a\>标签支持所有HTML的全局属性

## 事件属性
\<a\>标签支持所有HTML的事件属性

