当前学习link:
https://www.bilibili.com/video/BV1gr4y1U7CY?p=34&vd_source=c3e313c1c635c648f9abbb17350d9043


Docker是一个CS结构的系统，后端是一个松耦合架构，众多模块各司其职
Docker守护进程运行在主机上，通过Socket连接从客户端访问
守护进程从客户端接受命令并管理运行在主机上的容器
容器，是一个运行时环境(鲸鱼上的集装箱)

Docker运行的基本流程：

安装
https://docs.docker.com/engine/install/centos/



常用命令
帮助启动类命令
	启动docker： systemctl start docker
	停止docker： systemctl stop docker 
	重启docker： systemctl restart docker 
	查看docker状态： systemctl status docker 
	开机启动： systemctl enable docker 
	查看docker概要信息： docker info
	查看docker总体帮助文档： docker --help 
	查看docker命令帮助文档： docker 具体命令 --help
	
镜像命令：
	docker image ： 列出本地主机上的镜像
		repository： 表示镜像的仓库源
		tag： 经i选哪个的标签版本号
		image id: 镜像ID
		created： 镜像创建时间
		size： 镜像大小
		
		同一仓库源可以有多个tag版本，代表这个仓库源的不同个版本
		通过使用repository:tag来定义不同的镜像
		如果不指定一个镜像的版本标签，比如只使用tomcat，docker将默认使用tomcat:latest镜像
		
		docker image -a 列出全部的镜像，a代表all
		docker image -q 只列出全部镜像的image id这一列
		
		
		
	docker search 某个XXX镜像名字
		--limit: 只列出N个镜像，默认是25个
		docker search --limit 5 redis
	docker pull 某个XXX镜像名字
	
	docker system df  查看镜像/容器/数据卷所占的空间
	
	docker rmi 某一个镜像id/镜像名称   删除某一个镜像
	docker rmi -f 镜像名1：tag 镜像名2：tag ......  删除多个镜像
	docker rmi -f $(docker images -qa) 删除全部镜像
	docker rmi -f 某一个镜像id/镜像名称  强制删除某一个镜像
	注意： rmi代表remove image, rm代表remove 容器

什么是虚悬镜像
仓库名，标签都是<none>的镜像，俗称虚镜像 dangling image 
一般建议删除，原因可能是docker在创建镜像时出现了一些问题



容器命令
新建+启动容器
	docker run [options] image [command][arg...]
	option: 有些是一个减号，有些是两个减号
		    --name="容器新名字" 为容器指定一个名称
	        -d: 后台运行容器并返回容器ID,也即启动守护式容器(后台运行)
			-i: 以交互模式运行容器，通常与-t同时使用
			-t：为容器重新分配一个伪输入终端，通常与-t同时使用-i同时使用
			也即启动交互式容器(前台有伪终端，等待交互)
			
			docker run -it ubuntu  /bin/bash 表示启动一个ubuntu的容器，同时返回一个终端可以跟该容器交互，交互命令的接口是shell,即/bin/bash，容器的名字系统会随机分配
			docker run -it --name=myu1 ubuntu  /bin/bash 效果同上，只是启动的实例叫myu1
			-P: 随机端口映射，大写P
			-p：指定端口映射，小写p

列出当前所有正在运行的容器
	docker ps [options]
	docker ps  罗列出正在运行的实例
	docker ps -a 罗列出所有正在运行的以及历史上运行过的容器
	docker ps -l 显示最近创建的容器
	docker ps -n 显示最近n个创建的容器
	docker ps -q 静默模式，只显示容器编号
	
	启动容器后建议执行docker ps查看下容器是否启动成功

退出容器
	两种退出方式： 
		exit： run进去容器，容器停止
		ctrl + p + q： run进去容器，ctrl + p + q退出，容器不停止

启动已经停止运行的容器
	docker start 容器ID或者容器名
	
重启容器
	docker restart 容器ID或者容器名
	
停止容器
	docker stop 容器ID或者容器名
	
强制停止容器
	docker kill 容器ID或者容器名

删除已停止的容器
	docker rm 容器ID或者容器名
	
	一次性删除多个容器实例： docker rm -f$(docker ps -a -q)
	                   docker ps -a -q | xargs docker rm

启动给守护式容器(后台服务器)			   
	docker run -d 容器名 启动守护式容器，与-it 交互式容器相对应
	命令执行后马上退出，这是docker机制的问题

查看容器日志
	docker logs 容器ID
	
查看容器内的进程
	每一个容器其实也是一个简易版的linux环境，因此是可以内部进程
	docker top 容器ID 
	
查看容器内部细节
	docker inspect 容器ID
	
进入正在运行的容器并以命令行交互
	docker exec -it 容器ID bashshell
	
重新进入 docker attach 容器ID
	attach和exec之间的区别
		attach直接进入容器启动命令的终端，不会启动新的进程，用exit退出，会导致容器的停止
		exec是在容器中打开新的终端，并且可以启动新的进程，用exit退出，不会导致容器的停止
	推荐使用docker exec命令，因为退出容器终端，不会导致容器的停止
	
	
从容器内拷贝文件到主机 
	docker exec -it 容器ID /bin/bash
	docker cp 容器ID：容器内路径 目的主机路径
	
导入和导出容器
	export 导出容器的内容作为一个tar归档文件(对应import命令)
	import从tar包中的内容跟创建一个新的文件系统再导入为镜像(对应export)
	
	docker export 容器ID > 文件名.tar
	cat 文件名.tar | docker import -镜像用户/镜像名：镜像版本号
	
	
	
	
	
	
镜像的分层
	
