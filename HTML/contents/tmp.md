表单中的单选按钮可以设置以下几个属性：value、name、checked

 value：提交数据到服务器的值（后台程序PHP使用）
 name：为控件命名，以备后台程序 ASP、PHP 使用
 checked：当设置 checked="checked" 时，该选项被默认选中
<form>
<p>你生活在哪个国家？</p>
<input type="radio" name="country" value="China" checked="checked">中国<br />
<input type="radio" name="country" value="the USA">美国
</form>
注意：同一组的单选按钮，name 取值一定要一致，比如上面例子为同一个名称“country”，这样同一组的单选按钮才可以起到单选的作用。

Elvirangel
   Elvirangel

  zha***r601@163.com

5年前 (2018-03-10)
   JIang

  154***894@qq.com

109
如何使用隐藏在下拉列表中的默认空白值实现SELECT标记

只需使用禁用和/或隐藏属性：

<form>
  <select>
    <option selected disabled hidden style="display: none" value=""></option>
    <option value="volvo">Volvo</option>
    <option value="saab">Saab</option>
    <option value="fiat">Fiat</option>
    <option value="audi">Audi</option>
 </select>
</form>
selected：使此选项成为默认选项。
disabled：使此选项无法点击。
style="display:none"：使此选项不在旧版浏览器中显示。 
hidden：使此选项不显示在下拉列表中。