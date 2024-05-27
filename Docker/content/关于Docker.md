当前学习link:
https://www.bilibili.com/video/BV1gr4y1U7CY?p=8&vd_source=c3e313c1c635c648f9abbb17350d9043


# 网站
- docker官网：www.docker.com
- docker hub官网： hub.docker.com   安装镜像的仓库

# 关于Docker
docker并非是一个通用的容器工具，它依赖于已存在并运行的Linux内核环境\
Docker最初是为Linux开发的，因为它直接使用了Linux内核的特性，这使得Docker在Linux上运行效果最佳，并且具有最大的性能和兼容性\
Docker实质上是在已经运行的Linux下制造了一个隔离的文件环境，因此它的执行效率几乎等同于所部署的Linux主机\
因此，Docker必须部署在Linux内核的系统上

非linux内核系统运行docker，可以使用以下方法：
 1) 先安装一个虚拟机，并在安装Linux系统的虚拟机中运行Docker
 2) 使用Docker Desktop
    Desktop并不会直接跟非Linux系统进行交互，因为像windows和MacOS都有内置的虚拟化技术，它会虚拟一个轻量级的linux系统使得Docker Desktop可以在这些虚拟化的linux系统里执行docker
