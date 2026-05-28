[目录](../目录.md)


# 关于Autoscaling类资源
Autoscaling类资源，主要包括:
- Horizontal Pod Autoscaler(HPA)


# Horizontal Pod Autoscaler(HPA)
中文全称：水平 Pod 自动扩缩容控制器
HPA是autoscaling API组下的命名空间级资源
HPA依据内置（CPU/内存）或自定义指标，动态调整Deployment、StatefulSet等工作负载控制器的Pod副本数量，实现Pod水平扩缩容

默认每30秒查询一次指标数据，轮询间隔可通过kube-controller-manager的以下参数参数修改
- 参数: horizontal-pod-autoscaler-sync-period

HPA支持以下指标类型：
- 内置指标：按资源利用率计算，如Pod CPU/内存
- 自定义Pod指标：按原始数值计算
- 自定义对象指标：如其他资源的状态指标

HPA指标获取方式
- Heapster: 早期方式，不推荐
- Metrics Server: 主流, 提供基础指标
- 自定义REST API: 获取扩展指标

**注：**\
支持配置多组指标联合判断扩缩容策略