[目录](../目录.md)


# 关于Autoscaling资源
Autoscaling资源，主要包括:
- Horizontal Pod Autoscaler(HPA)


# Horizontal Pod Autoscaler(HPA)
用于实现Pod水平自动扩缩容，可依据CPU使用率或自定义指标，动态调整Deployment/StatefulSet等控制器的副本数
- 默认每30秒查询一次指标数据，轮询间隔可通过 kube-controller-manager的参数--horizontal-pod-autoscaler-sync-period修改
- 支持三类指标类型：
  - 内置指标（如 Pod CPU / 内存），按资源利用率计算；
  - 自定义 Pod 指标，按原始数值计算；
  - 自定义对象指标（如其他资源的状态指标）。
- 指标获取方式
  - Heapster: 早期方式，不推荐
  - Metrics Server: 主流, 提供基础指标
  - 自定义REST API: 获取扩展指标
- 支持配置多组指标联合判断扩缩容策略