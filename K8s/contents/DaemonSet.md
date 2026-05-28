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