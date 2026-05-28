[目录](../目录.md)


# 关于Networking组API资源
Networking组API资源主要包括：
- Ingress


# Ingress
Ingress主要用于处理k8s外部网络请求，实现k8s内部服务暴露外网访问

**示例**\
k8s集群下有三个Node，配置如下：

- **Node1**\
  部署了Product Pod提供product-svc服务

- **Node2**\
  部署了Order Pod提供order-svc服务

- **Node3**\
  作为网关节点接受外部请求，部署了Ingress Controller\
  外部用户访问Node3的Ingress，Ingress将请求转发到集群内部的Pod中

**注：**\
Node1和Node2用来提供应用服务，Node3作为网关节点接受外部请求，并根据请求内容将流量转发至Node1和Node2\
<img src="./img/资源_API_Networking_001.png" alt="ingress1" width="500">\
<img src="./img/资源_API_Networking_002.svg"" alt="ingress2" width="500">