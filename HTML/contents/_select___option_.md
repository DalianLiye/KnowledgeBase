[目录](../目录.md)

# 定义
\<select\>标签定义下拉列表表单元素

# 使用
在页面中, 如果有多个选项让用户选择, 并且想要节约页面空间时, 可使用\<select\>标签控件定义下拉列表\
\<select\>标签中至少包含一对\<option\>
在\<option\>标签中定义select="selected"时, 当前项即为默认选中项

# 属性
## selected属性
**定义：**\
用于定义页面初始化时，默认的选中项\
**值：**\
固定值"selected"

# 示例
```html
<select>
    <option>项目1</option>
    <option>项目2</option>
    <option>项目3</option>
    <option selected="selected">项目4</option>  <!--页面初始化时，默认选中该项目-->
    ...
</select>
```