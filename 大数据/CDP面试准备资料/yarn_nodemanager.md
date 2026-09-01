# 故障状态

LOST：RM 收不到 NM 的心跳（通信层面问题），NM 进程可能挂了、卡死
UNHEALTHY：NM 进程活着，能正常发心跳；但是 NM 本地自检失败（磁盘 / 目录 / 自定义健康脚本异常）


# Lost
参数：yarn.resourcemanager.nm.liveness‑monitor.expiry‑interval‑ms，默认 60 秒。
RM 超过这个时间收不到 NM 上报的心跳，就标记节点 LOST

触发原因
NodeManager 进程直接崩溃、被 OOM‑killer 杀死；
NM 发生长时间 Full GC，JVM STW 停顿，心跳线程卡住，进程还在但是发不出心跳；
NM 与 RM 网络抖动、断连、DNS 异常、Kerberos 问题；
服务器宕机、重启。

行为表现
RM 不再给该节点分配新 container；
RM 判定该节点上所有 container 全部失败；
如果 AM 正好跑在这台机器，触发 AM 重试，yarn‑cluster 任务整体重跑；
如果RM将新的AM指定给其他节点，AM会从该节点移除，任务会重新分配；
如果AM在该节点，任务会继续运行，直到完成；
如果后面 NM 恢复、重新向 RM 注册，节点变回 RUNNING
关键点：RM 不知道 NM 内部发生了什么，只是收不到心跳，通信超时判定失联。



# UNHEALTHY（节点不健康）
NodeManager 进程存活，可以正常给 RM 发送心跳，心跳包里面主动告诉 RM：我本机硬件 / 目录有问题，我不健康
NM 内部磁盘健康检查线程（默认 2 分钟执行一次）检查：
yarn.nodemanager.local‑dirs 容器本地数据目录
yarn.nodemanager.log‑dirs 容器日志目录
检查项：磁盘使用率、磁盘是否只读、目录权限、inode 耗尽。
当故障磁盘比例超过阈值，NM 上报状态 UNHEALTHY。
也可以配置自定义 shell 健康检测脚本，脚本返回异常，节点也会变成 UNHEALTHY。

触发原因
local‑dirs/log‑dirs 磁盘使用率超过阈值（默认 90%）；
目录权限错误、磁盘损坏、只读；
inode 耗尽；
自定义健康检测脚本执行失败。

行为表现
RM不再往这个节点分配新的 container；
已经正在运行的 container 还会继续跑，不会直接杀掉；
磁盘问题修复之后，下一轮健康检查通过，节点自动恢复 RUNNING；
不会因为 UNHEALTHY 触发 AM 重试