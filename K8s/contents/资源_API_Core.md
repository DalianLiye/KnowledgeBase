[目录](../目录.md)


# 关于Core组API资源
Core组API资源主要包括：
- PersistentVolume(PV)
- PersistentVolumeClaim(PVC)
- ConfigMap
- Secret
- LimitRange
- Pod
- PodTemplate
- Service
- Node
- Namespace


# PersistentVolume(PV)
PV即: 持久化卷\
PV是集群级存储资源，对NFS、云盘、iSCSI等底层存储进行统一抽象\
PV的作用是为整个集群提供可用的持久化存储载体

特点:
- 可由管理员手动创建，也可通过StorageClass动态自动创建
- 生命周期独立于Pod，不受Pod启停、删除影响
- 定义存储容量、访问模式（如 ReadWriteOnce、ReadOnlyMany、ReadWriteMany）、存储类型、回收策略等属性

**注：**\
PV是集群级资源


# PersistentVolume(PVC)
PVC即: 持久化卷声明\
PVC是用户发起的存储资源申请，用于指定所需存储的规格, 类似于“我要一个多大容量、什么访问模式的存储卷”

PVC的作用是解耦使用者与底层存储，简化存储申请流程\
即：用户无需关心底层存储细节，只需声明需求即可使用持久化存储

特点：
- 用户仅声明存储容量、访问模式等需求，无需感知底层存储细节
- 创建后会自动匹配并绑定符合条件的PV，PV与PVC为一对一绑定
- 生命周期不强制和Pod绑定，Pod通过挂载PVC来使用存储

**注：**\
PVC是命名空间级资源


# ConfigMap
用于存储键值（key-value）格式的非敏感配置数据，可被挂载或注入到Pod中，供容器读取使用\
ConfigMap可集中统一管理应用配置，多个Pod/容器可共用同一份配置，避免逐个单独维护，提升配置管理效率

**注：**\
由于ConfigMap采用的是普通明文配置，敏感数据建议使用Secret


# Secret
功能用法与ConfigMap相近，专门用于存储密码、令牌、密钥等敏感数据\
数据会以编码形式存储，避免明文暴露，防止敏感信息泄露\
使用时可挂载或注入到Pod中，无需将敏感数据直接写入镜像或Pod配置清单

**注：**\
Secret仅做Base64 编码（非强加密），生产环境可配合权限策略进一步加固安全

使用方式：
- Volume挂载
- 环境变量注入

Secret类型:
- **Service Account**\
  用于Pod访问K8s API的身份凭证，由集群自动创建，会自动挂载到Pod内路径：/run/secrets/kubernetes.io/serviceaccount

- **Opaque**\
  默认数据以Base64编码存储，常用于存放密码、密钥等敏感数据\
  注：Base64仅为编码方式，并非加密，可逆向解码还原原始数据

- **kubernetes.io/dockerconfigjson**\
  专门存储私有镜像仓库的登录认证信息，用于拉取私有镜像


# LimitRange
作用于命名空间，统一约束该空间内Pod与容器的资源配置，批量设置资源使用规则
通过设置资源默认值、最大值、最小值，规范整体资源使用，避免资源滥用
- **Request**\
  资源预留最小值，调度时保证容器至少可分配到对应资源
- **Limits**\
  资源使用上限，容器运行时不得超出该数值


# Pod
当多个容器存在强依赖、紧耦合关系时，可部署在同一个Pod中，它们会共享Pod内的网络栈与存储卷\
Pod是K8s中最小的可部署、调度单元，本质是一组容器的集合

一个Pod包含：
- 应用容器（单个或多个）
- 存储资源
- 独立唯一的Pod IP
- 容器运行配置
  
Pod代表集群中一个独立的应用运行实例\
K8s不会直接管理容器，所有容器都被封装在Pod中统一调度与管理\
Pod本身属于命名空间级资源


- **Pod和容器**\
  Pod和容器常见组合方式：
  - **one-container-per-pod**\
    一个Pod内仅运行一个容器，生产环境最常用, Pod可看作该容器的运行载体
  - **multi-containers-per-pod**\
    一个Pod内运行多个容器，适用于容器间紧密耦合、需要共享资源、必须协同运行的场景\
    同一Pod内所有容器共享同一个IP地址、端口空间，容器间可通过localhost直接通信

  **注：**\
  常规场景下一个Pod建议只运行主应用容器，多容器仅用于日志收集、监控等辅助侧容器场景


- **Pause容器**\
  K8s会为每个Pod自动创建一个Pause容器（也叫沙箱容器）\
  它是Pod内所有业务容器的基础，负责统一创建并共享网络栈、存储卷、PID命名空间等核心资源\
  因此同一Pod内的不同容器，可直接通过localhost互相访问
  <img src="./img/资源_API_Core_001.png" alt="pod容器1" width="500">\
  <img src="./img/资源_API_Core_002.svg" alt="pod容器2" width="500">

  **注:**\
  - Pause容器功能极简，几乎不占用资源，生命周期贯穿整个Pod，Pod启停本质就是Pause容器启停
  - 所有业务容器都会加入Pause容器的命名空间，实现资源互通
  - 外部访问Pod，实际访问的也是Pause容器暴露的网络端点

- **Pod容器类型**\
  Docker曾是K8s Pod中主流的容器运行时\
  目前K8s遵循CRI标准，同时兼容多种容器引擎


# Pod Template
它是Pod的配置定义，并非独立资源，内嵌在各类控制器对象中，控制器用它来创建Pod
常见使用对象：Deployment、StatefulSet、DaemonSet、ReplicaSet、Job、CronJob
控制器依据该模板统一创建Pod


## Pod副本
副本指基于同一模板复制生成的多个Pod实例
副本仅Pod名称、UID等标识类信息不同，容器配置、运行应用等核心内容完全一致，对外提供相同服务

K8s控制器通过Pod模板和replicas（副本数）定义期望实例数量，并按模板创建对应个数的Pod
当集群内实际Pod数量与期望副本数不匹配时，控制器会自动调度，始终维持副本数量符合设定值

常见管理副本的控制器：
- Deployment
- ReplicaSet
- StatefulSet

**注:**\
- 同组副本Pod一般会调度到不同节点，实现负载均衡与故障容错
- Pod副本属于命名空间级资源


# Service
Service主要用于k8s集群内部的网络通信，比如Node之间，Pod之间的通信(即便Pod处在不同的Node里)\
由于k8s内部是无法直接访问Pod的，因此就通过Service暴露端口的方式接收通信请求，再将请求转发到Pod\
也就是Pod是通过service来暴露自己，进而提供服务的

如果一个应用的背后由一组Pod支撑，那么Service就是这个应用服务的抽象，它定义了Pod逻辑集合和访问这个Pod集合的策略\
Service不代表一个Node，而是代表一组Pod

Service也可以处理外部请求，对外提供一个访问入口，外部请求访问该入口后，通过负载均衡转发到Pod集合中某一个Pod的容器内\
这仅限于某些service类型，比如NodePort，LoadBalancer，但Service主要还是处理k8s内部请求


**东西流量和南北流量**

- **东西流量**\
  横向流量, 通过service实现集群内部各个节点的访问

- **南北流量**\
  纵向流量，通过Ingress实现k8s内部服务暴漏外网访问

<img src="./img/资源_API_Core_003.png" alt="东西南北流量" width="500">



# Node
集群中的工作节点，用于运行Pod\
节点并非由K8s创建，而是由K8s进行管理\
即使通过yaml创建节点对象，K8s也只会做健康检查，检查失败则不会调度Pod到该节点


# Namespace
命名空间本身也是一种资源，它属于集群级资源


# Downward API
Downward API既不用于持久化存储数据，也不承担容器与宿主机的数据交换工作\
其核心作用是让容器获取当前Pod自身的元数据信息，实现Pod信息向容器内注入

Downward API属于core/v1，是Pod内置的元数据注入机制\
将Pod信息注入容器两种方式
- **环境变量**\
  适用于传递单个字段，可把Pod、容器相关信息注入容器环境变量

- **Volume挂载**\
  将Pod信息生成文件，以卷的形式挂载到容器内部