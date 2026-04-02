[目录](../目录.md)

# 关于URL
URL, 也叫统一资源定位器(Uniform Resource Locators)\
URL 是一个网页地址\
URL可以由字母组成, 如"baidu.com", 或互联网协议(IP)地址： 192.68.20.50\
一般使用网站域名来访问,因为名字比数字更容易记住

Web浏览器通过URL从Web服务器请求页面\
点击HTML页面中的某个链接时, 对应的\<a\>标签指向万维网上的一个地址
一个统一资源定位器(URL)用于定位万维网上的文档

**语法规则:**\
scheme://host.domain:port/path/filename\
例如：http://www.baidu.com/html/html01.html

**说明:**
- **scheme**\
定义因特网服务的类型, 以下为最常见类型：
    - http(超文本传输协议, 以 http:// 开头的普通网页, 不加密)
    - https(超文本传输协议,安全网页, 加密所有信息交换),
    - ftp(文件传输协议, 用于将文件下载或上传至网站)
    - file(计算机上的文件)
- **host**\
定义域主机（http 的默认主机是 www）
- **domain**\
定义因特网域名，比如 runoob.com
- **:port**\
定义主机上的端口号（http 的默认端口号是 80）
- **path**\
定义服务器上的路径（如果省略，则文档必须位于网站的根目录中）
- **filename**\
定义文档/资源的名称

# URL字符编码
URL只能使用 ASCII 字符集来通过因特网进行发送\
由于URL常常会包含ASCII集合之外的字符, URL 必须转换为有效的ASCII格式\
URL编码使用"%"其后跟随两位的十六进制数来替换非 ASCII 字符\
URL不能包含空格, URL编码通常使用 + 来替换空格

完整的URL编码请参考\
https://www.runoob.com/tags/html-urlencode.html