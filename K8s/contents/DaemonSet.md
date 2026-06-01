[目录](../目录.md)


# 关于DaemonSet
DaemonSet通过节点选择器（selector）筛选节点，在每个匹配节点上运行一个Pod(守护程序)
常用于部署集群日志、监控、网络、存储等节点级系统组件


# 典型场景
- **日志收集**\
  fluentd，logstash等

- **节点监控**\
  Prometheus Node Exporter，collectd等监控组件

- **集群基础程序**\
  kube-proxy、glusterd、Ceph 客户端等



# 创建DaemonSet
通过以下配置创建DaemonSet，文件名：fluentd-demo.yaml
```yaml
apiVersion: apps/v1
kind: DaemonSet  # 创建DaemonSet资源
metadata:
  name: fluentd  # DaemonSet名字
spec:
  selector:
    matchlabels:
      app: logging  # 此处的标签值要与.spec.template.metadata.labels[0].app的值一一对应
  template:
    metadata:
      labels:
        app: logging
        id: fluentd
      name: fluentd
    spec:
      containers:
      - name: fluentd-es
        image: agilestacks/fluentd-elasticsearch:v1.3.0
        env:  # 环境变量配置
        - name: FLUENTD_ARGS
          value: -qq
        volumeMounts:  # 加载数据卷，避免数据丢失
        - name: containers
          mountPath: /var/lib/docker/containers
        - name: varlog
          mountPath: /var/log
      volumes: # 定义数据卷
         - hostPath:  #数据卷类型，主机路径的模式，即与Node共享目录
             path: /var/lib/docker/containers  # 将Node中的该目录共享
           name: containers  # 定义的数据卷的名称
          - hostPath:
             path: /var/log
           name: varlog
```
创建后，发现fluentd pod被发布在了所有非master 的node上，如果selector没有匹配的node，它会默认将pod发布在所有非master 节点

将其中一个node打上标签
```shell
kubectl label no k8s-node1 type=microservices
```

同时给daemonset添加Nodeselector,
```yaml
apiVersion: apps/v1
kind: DaemonSet  # 创建DaemonSet资源
metadata:
  name: fluentd  # DaemonSet名字
spec:
  selector:
    matchlabels:
      app: logging  # 此处的标签值要与.spec.template.metadata.labels[0].app的值一一对应
  template:
    metadata:
      labels:
        app: logging
        id: fluentd
      name: fluentd
    spec:
      nodeSelector:
        type: microservices 
      containers:
      - name: fluentd-es
        image: agilestacks/fluentd-elasticsearch:v1.3.0
        env:  # 环境变量配置
        - name: FLUENTD_ARGS
          value: -qq
        volumeMounts:  # 加载数据卷，避免数据丢失
        - name: containers
          mountPath: /var/lib/docker/containers
        - name: varlog
          mountPath: /varlog
       volumes: # 定义数据卷
         - hostPath:  #数据卷类型，主机路径的模式，即与Node共享目录
             path: /var/lib/docker/containers  # 将Node中的该目录共享
           name: containers  # 定义的数据卷的名称
         - hostPath:
             path: /var/log
           name: varlog
```
修改后，发现fluentd pod只在Node1上运行\
此时如果同样的方式给node2打同样的标签，会发现fluentd pod也会在node2上运行

DaemonSet配置文件中，spec.selector.matchlabels的标签值要跟spec.template.metadata.labels的值一一对应\
只有一一对应，DaemonSet才知道它要将这个yaml文件里的pod发布到指定的node上


# 指定Node节点
DaemonSet是一种特殊的控制器，用于确保集群中每个（或符合条件的）节点上都运行一个 Pod 副本\
它会忽略Node的unschedulable状态，即使节点被标记为 unschedulable，DaemonSet仍然会在该节点上创建 Pod

DaemonSet在指定的Node节点运行Pod主要通过以下方式：
- **nodeSelector**\
  只调度到匹配指定Label的Node上

- **nodeAffinity**\
  功能更丰富的Node选择器，比如支持集合操作

- **podAffinity**\
  调度到满足条件的Pod所在的Node上


# DaemonSet更新
当修改DaemonSet的 spec.template （例如更新容器镜像、环境变量、资源限制等）\
默认情况下，控制器会逐个节点滚动更新其管理的DaemonSet Pod，替换旧的Pod为新的Pod

DaemonSet支持多种更新策略，主要通过spec.updateStrategy属性控制，包含以下几种方式：
- **RollingUpdate**\
  不推荐，会逐个节点滚动更新DaemonSet Pod，按策略逐步替换旧Pod，会造成频繁更新

- **OnDelete**\
  推荐，仅当对应的DaemonSet Pod被手动删除时，控制器才会根据新的模板创建新的Pod（不会自动替换现有 Pod\
  即需要哪个节点更新DaemonSet Pod就删掉哪个节点的Pod，然后更新那个节点Pod，避免频繁更新

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: example-ds
spec:
  updateStrategy:  # 控制DaemonSet更新策略
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 1
  selector:
    matchLabels:
      app: my-daemon
  template:
    metadata:
      labels:
        app: my-daemon
    spec:
      containers:
        - name: my-daemon
          image: myimage:v2
```