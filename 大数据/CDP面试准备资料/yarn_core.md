# RM ResourceManager 资源管理器
全局老大，整个集群资源总调度
两个核心组件：
Scheduler 调度器：分配资源，不监控任务状态
ApplicationManager：接收作业，启动 AM，处理 Application 失败

# NM NodeManager 节点管理器
每个 DataNode 一台，本节点资源管理者
管理 Container，监控节点资源，上报 RM，启停容器

# AM ApplicationMaster 应用管理器
每个作业一个 AM，向 RM 申请资源，跟 NM 通信启动 Container，管理本作业所有 task
AM 本身也是一个 Container

# Container 容器
YARN资源抽象单元，封装 CPU、内存，任务全部跑在 Container 里

# 作业完整提交流程
作业完整提交流程：客户端提交 → RM 接收 → RM 分配 Container 启动 AM → AM 向 RM 申请资源 → NM 启动各个 Task Container → 作业运行完成