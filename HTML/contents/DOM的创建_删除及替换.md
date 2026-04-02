[目录](../目录.md)

# 创建HTML元素

- document.appendChild()\
将新元素作为父元素的最后一个子元素进行添加\
如需向HTML DOM添加新元素, 首先必须创建该元素, 然后把它追加到已有的元素上
```html
var newElement = document.createElement("p")   //创建新元素p
var newTextNode = document.createTextNode("文本节点")   //创建新文本节点
newElement.appendChild(newTextNode)  //向 <p> 元素追加文本节点

var element = document.getElementById("div_id")
element.appendChild(newElement)  
```

- document.insertBefore()\
该方法可以在指定位置创建新元素
```javascript
var newElement=document.createElement("p");
var newTextNode=document.createTextNode("文本节点");
newElement.appendChild(newTextNode);

var element=document.getElementById("div_id");
var child=document.getElementById("p1");
element.insertBefore(newElement,child); //将newElement插入到child节点前
```
 

# 删除HTML元素

- document.removeChild()
```javascript
var parent=document.getElementById("div1");
var child=document.getElementById("p1");
parent.removeChild(child);     

/*
要想删除一个元素必须要通过父元素调用removeChild()方法实现
如果确定删除的元素但不确定父元素，可通过以下方式实现
即通过parentNode属性获取父元素，然后再调用removeChild()方法实现

var child=document.getElementById("p1");
child.parentNode.removeChild(child);
*/
```
 

# 替换HTML元素

- document.replaceChild()
```javascript
var parent=document.getElementById("div1");
var child=document.getElementById("p1");
var para=document.createElement("p");
var node=document.createTextNode("这是一个新的段落。");
para.appendChild(node);
parent.replaceChild(para,child);
```