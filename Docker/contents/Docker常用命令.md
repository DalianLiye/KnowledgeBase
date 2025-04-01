# 启动类命令

## systemctl start
```bash
systemctl start docker
```
**说明：** 启动docker

<br>

## systemctl stop
```bash 
systemctl stop docker 
```
**说明：** 停止docker
	
<br>

## systemctl restart
```bash
systemctl restart docker 
```	
**说明：** 重启docker

<br>

## systemctl status
```bash
systemctl status docker 
```	
**说明：** 查看docker状态

<br>

## systemctl enable
```bash
systemctl enable docker 
```	
**说明：** 设置开机启动

<br>

# 帮助类命令

## docker info
```bash
docker info #查看docker概要信息
```	

<br>

## docker --help
```bash
docker --help  #查看docker总体帮助文档
docker <command> --help  #查看docker命令帮助文档
```	

<br>

# 镜像命令

## docker image 
```bash
docker image -a  #列出全部镜像，a代表all
docker image -q  #只列出全部镜像的image id这一列
```
**说明：** 
列出本地主机上的镜像
- repository： 表示镜像的仓库源
- tag： 经i选哪个的标签版本号
- image id: 镜像ID
- created： 镜像创建时间
- size： 镜像大小
		
同一仓库源可以有多个tag版本，代表这个仓库源的不同个版本\
通过使用repository:tag来定义不同的镜像\
如果不指定一个镜像的版本标签，比如只使用tomcat，docker将默认使用tomcat:latest镜像

<br>
		
## docker search
```bash
docker search <image_name>

docker search --limit 5 redis  #limit: 只列出N个镜像，默认是25个
```	
**说明：** 检索镜像

<br>

## docker pull
```bash
docker pull <image_name>
```
**说明：** 拉取镜像到本地

<br>

## docker system
```bash
docker system df
```
**说明：** 查看<镜像/容器/数据卷>所占的空间

<br>

## docker rmi
```bash
docker rmi <image_id/image_name>   #通过指定镜像id或镜像名，删除某一个镜像
docker rmi -f image_name1：tag image_name2：tag ...  #删除多个镜像
docker rmi -f $(docker images -qa)  #删除全部镜像
docker rmi -f  <image_id>/<image_name>  #强制删除某一个镜像
```
**说明：** rmi代表remove image, rm代表remove容器



# 容器命令

## docker run
```bash
docker run [options] image [command][arg...]
```
**说明：** 新建+启动容器

**option:**
- \--name="<container name>" 为容器指定一个名称
- \-d: 后台运行容器并返回容器ID,也即启动守护式容器(后台运行)
- \-i: 以交互模式运行容器，通常与-t同时使用
- \-t： 为容器重新分配一个伪输入终端，通常与-t同时使用-i同时使用, 也即启动交互式容器(前台有伪终端，等待交互)

```bash
docker run -it ubuntu  /bin/bash #表示启动一个ubuntu的容器，同时返回一个终端可以跟该容器交互，交互命令的接口是shell,即/bin/bash，容器的名字系统会随机分配
docker run -it --name=myu1 ubuntu  /bin/bash  #效果同上，只是启动的实例叫myu1
```
-P: 随机端口映射，大写P
-p： 指定端口映射，小写p

```bash		   
docker run -d <container>  #启动守护式容器(后台服务器)，与-it 交互式容器相对应
```
**注：** 命令执行后马上退出，这是docker机制的问题

<br>

## docker ps
```bash
docker ps [options]
```

```bash
docker ps     #列出正在运行的实例
docker ps -a  #列出所有正在运行的以及历史上运行过的容器
docker ps -l  #显示最近创建的容器
docker ps -n  #显示最近n个创建的容器
docker ps -q  #静默模式，只显示容器编号
```
**说明：** 列出当前所有正在运行的容器
**注：** 启动容器后建议执行docker ps查看下容器是否启动成功


## 退出容器
两种方式： 
- **exit：** 
run进去容器，容器停止
- **ctrl + p + q：**
run进去容器，ctrl + p + q退出，容器不停止

<br>

## docker start
```bash
docker start <container_id>/<container_name>
```
**说明：** 启动已经停止运行的容器

<br>
	
## docker restart
```bash
docker restart <container_id>/<container_name>
```
**说明：** 重启容器

<br>

## docker stop
```bash
docker stop <container_id>/<container_name>
```
**说明：** 停止容器

<br>
	
## docker kill
```bash
docker kill <container_id>/<container_name>
```
**说明：** 强制停止容器

<br>

## docker rm
```bash
docker rm <container_id>/<container_name>

# 一次性删除多个容器实例
docker rm -f$(docker ps -a -q)
docker ps -a -q | xargs docker rm
```
**说明：** 删除一个或多个停止状态的Docker容器
	                   
<br>

## docker logs
```bash
docker logs <container_id>
```
**说明：** 查看容器日志

<br>

## docker top	
```bash
docker top <container_id> 
```
**说明：** 查看容器内的进程
**注：** 每一个容器其实也是一个简易版的linux环境，因此是可以内部进程
	
<br>

## docker inspect
```bash
docker inspect <container_id>
```
**说明：** 查看容器内部细节

<br>
	
## docker exec
```bash
docker exec -it <container_id> bashshell
```
**说明：** 进入正在运行的容器并以命令行交互

<br>
	
## docker attach
```bash
docker attach <container_id>
```
**说明：** 进入容器

<br>

## docker attach和docker exec区别
- **attach：**
直接进入容器启动命令的终端，不会启动新的进程，用exit退出，会导致容器的停止

- **exec：**
在容器中打开新的终端，并且可以启动新的进程，用exit退出，不会导致容器的停止

- **注：**
推荐使用docker exec命令，因为退出容器终端，不会导致容器的停止
	
<br>

## docker cp
```bash
docker exec -it <container_id> /bin/bash
docker cp <container_id>：<path_in_container> <target_host_path>

#例
docker cp my_container:/usr/src/app/file.txt .  # 从容器中复制位于/usr/src/app/file.txt的文件到宿主机的当前目录（.）
docker cp my_container:/usr/src/app/data /home/user/data # 从容器中复制/usr/src/app/data到宿主机的目标目录/home/user/data
```	
**说明：** 在Docker容器和宿主机之间复制文件或目录

<br>
	
## docker export
```bash
docker export <container_id> > <file_name>.tar  #导出容器的内容到一个tar归档文件
```
**说明：** 导出容器到tar文件

<br>
	
## docker import
```bash
docker import [OPTIONS] FILE|URL|- [REPOSITORY[:TAG]]
```
- **FILE|URL|-：** 
要导入的tar文件，可以是本地文件路径、URL，或者使用-表示从标准输入（stdin）读取。
- **[REPOSITORY[:TAG]]：** 
指定要创建的镜像名称和标签（tag），格式为\<image account\>/\<image name\>:\<image version\>

```bash
docker export <container_id> > <file_name>.tar #导出image到tar文件

#根据tar包中的内容创建一个新的文件系统再导入为镜像
cat <file_name>.tar | docker import - <image_account>/<image_name>：<image_version>  #通过管道方式
docker import <file_name>.tar <image_account>/<image_name>:<image_version>   #直接指定文件路径

# 例
docker import myimage.tar myrepo/myimage:latest
cat myimage.tar | docker import - myrepo/myimage:latest
```	
**说明：** 将.tar文件作为Docker镜像导入容器
	
	
	
	
	

	
