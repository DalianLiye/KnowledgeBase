[目录](../目录.md)

通过HTML DOM, JavaScript能够访问并修改HTML文档中的每个元素

 
# 修改元素文本内容
```html
document.getElementById("p1").innerHTML="新文本!";  //更新了id是p1元素的文本节点内容
```

# 修改元素样式
```html
document.getElementById("p2").style.color="blue";
document.getElementById("p2").style.fontFamily="Arial";
document.getElementById("p2").style.fontSize="larger";
```

# 通过响应事件进行上述修改
HTML DOM允许事件发生时执行相应代码,包括以下事件：
- 在元素上点击, 如响应onclick事件
- 加载页面, 如直接在<scripts></scripts>中写
- 改变输入字段, 如响应onblur事件
```html
<script>
    function OnClickEnvent()
    {
        document.body.style.backgroundColor="lavender"; //改变body颜色
        document.getElementById("p1").innerHTML="Hello World!"; //更新id是p1元素的文本内容
    }
</script>

<p id="p1">Hello!</p>
<input type="button" onclick="OnClickEnvent()" value="点击事件" />
```
 