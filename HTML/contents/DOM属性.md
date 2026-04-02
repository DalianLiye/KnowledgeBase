[目录](../目录.md)

# innerHTML属性
获取元素内容的最简单方法是使用innerHTML属性\
innerHTML属性对于获取或替换HTML元素的内容很有用\
innerHTML属性可用于获取或改变任意HTML元素, 包括 \<html\>和\<body\>


# nodeName属性
nodeName属性规定节点的名称, 只读
不同的节点类型调用nodeName属性, 返回的值也不同, 如：
- \<元素节点\>.nodeName, 返回标签名
- \<属性节点\>.nodeName, 返回属性名
- \<文本节点\>.nodeName, 返回#text
- \<文档节点\>.nodeName, 返回#document

**注：**\
nodeName始终包含HTML元素的大写字母标签名


# nodeValue属性
nodeValue属性规定节点的值，不同的节点类型调用nodeValue属性，返回的值也不同，如：
- \<元素节点\>.nodeValue, 返回undefined或null
- \<文本节点\>.nodeValue, 返回文本本身
- \<属性节点\>.nodeValue, 返回属性值


# nodeType属性
nodeType属性返回节点的类型，只读
以下为元素类型和nodeType返回值的对应关系
- \<元素节点\>.nodeType,返回1
- \<属性节点\>.nodeType,返回2
- \<文本节点\>.nodeType,返回3
- \<注释节点\>.nodeType,返回8
- \<文档节点\>.nodeType,返回9