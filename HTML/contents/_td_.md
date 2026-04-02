[目录](../目录.md)

# 定义
标签用于定义表格中的单元格\
td代表单词table data cell, 意为表格中的一个单元格

# 使用
必须嵌套在\<tr\>标签中\
可以做合并单元格操作, 包括跨行合并和跨列合并

# 示例
```html
<table>
    <tr>
        <th>...</th>  
    </tr>
    <tr>
        <td>...</td>  
    </tr>
    ...
</table>
```

# 属性
## rowspan属性
**定义：**\
用于跨行合并\
**值：**\
列数, 正整数
```html
<td rowspan="合并单元格的个数">...</td>
```

## colspan属性
**定义：**\
用于跨列合并\
**值：**\
列数，正整数
```html
<td colspan="合并单元格的个数">...</td>
```

# 合并单元格
## 跨行合并
rowspan="合并单元格的个数"

## 跨列合并
colspan="合并单元格的个数"

## 目标单元格
**跨行合并：**\
最上侧单元格为目标单元格，写合并代码\
**跨列合并：**\
最左侧单元格为目标单元格，写合并代码

## 合并单元格三部曲
1) 先确定是跨行还是跨列合并\
2) 找到目标单元格，写上合并方式=合并的单元格数量\
3) 删除多余的单元格

## 示例
```html
<table border="1" align="center" cellpadding="0" cellspacing="0" width="1000" height="500">
    <tr>
        <td></td>
        <td colspan="2"></td>
    </tr>
    <tr>
        <td rowspan="2"></td>
        <td></td>
        <td></td>
    </tr>
    <tr>
        <td></td>
        <td></td>
    </tr>
</table>
```