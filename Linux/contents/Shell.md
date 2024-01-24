[目录](../目录.md)
# 脚本第一行 #
```bash
#!/bin/bash  #路径为解释器路径
```

# 命令分隔符 #
(**;**)分号 和 (**\n**)换行符


# 注释 # 
使用\#符号给代码注释


# 调试脚本 #
```bash
bash -x  <script_name>.sh #运行带有-x标志的脚本能打印出所执行的每一行命令以及当前状态

sh -x  <script_name>.sh #会将脚本中执行的每一行都输出到stdout

set -x #在执行时显示参数和命令
        #代码中set -x和set +x之间的代码显示调试信息

set +x #禁止调试

set -v #当命令进行读取时显示输入

set +v #禁止打印输入

_DEBUG=on   ./<script_name>.sh #通过传递_DEBUG环境变量来建立自定义的调试风格
```
脚本开头的第一行改为 #!/bin/bash -xv，就可以启动调试功能了


# Shell执行 #
**方法1: sh命令行参数**
```bash
sh  <script_name>.sh   #脚本位于当前路径下
sh  /dir1/dir2/.../<script_name>.sh  #使用脚本完整路径
```
注：当使用该方法时，脚本第一行的#!/bin/bash没有作用

**方法2: 独立运行脚本**
```bash
./<script_name>.sh  #脚本位于当前路径下.表示当前路径
/dir1/dir2/.../<script_name>.sh  #使用脚本完整路径
```
注：使用该方法，则脚本第一行的#!/bin/bash起作用，当读取该行，会以以下方式运行脚本,
```bash
/bin/bash <script_name>.sh
```
但需要给脚本赋予可执行权限
```bash
chmod  a+x  <script_name>.sh
```
