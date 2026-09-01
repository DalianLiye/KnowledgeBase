- Container 被 kill，退出码 143
最常见：内存超限，物理内存超出 container 分配内存，NM 杀掉容器

- Container 退出码 137
Linux OOM Killer，机器物理内存耗尽，操作系统直接杀进程

- 虚拟内存超限 killed（虚拟内存比率）

- AM 启动失败，作业提交卡住
RM、NM 通讯问题；资源不足；队列权限；磁盘满；日志目录权限

- 集群资源充足，但是任务拿不到资源
排查：队列最大容量、用户资源上限、Container 最小 / 最大规格不匹配、调度器队列配置错误

- NodeManager 掉线，状态 Lost
NM 和 RM 心跳超时，GC 卡顿、网络、磁盘满、内存溢出

- RM HA 高可用
RM 主备切换，zookeeper 存储状态，active/standby；故障切换现象；如何手动切换 RM


- 小任务很多，大量小container，集群卡顿怎么优化？
减少 task 数量，把很多小分片合并成大 task
Executor 复用（最关键，避免频繁启停 container）
不要一个 task 对应一个 container！ 一个 executor (container) 可以并行跑多个 task，由 spark.executor.cores 控制，核越多，单个 container 内并发 task 越多，减少 container 总数
上游源头减少小任务、小文件，合并成大任务、大文件

- YARN 的资源隔离怎么做？（CGroups，CPU 内存隔离）
YARN 两种隔离：内存隔离、CPU 隔离。
内存隔离：不需要 CGroups，NM 定期采样进程内存，超标直接 kill 容器。
CPU 软隔离（无 cgroups）：vcore 只是记账，YARN 做调度记账，进程可以抢占全部 CPU，隔离无效。
CPU 硬隔离（开启 CGroups）：操作系统层面限制 CPU 使用上限，container 不能超分配的 vcore，真正隔离。

- YARN 内存参数怎么规划，为什么不能机器全部内存给 yarn？
YARN 通过yarn.nodemanager.resource.memory‑mb定义节点所有 container 可使用内存总和。
不能把机器全部内存分配给 YARN。第一操作系统需要内存，尤其 HDFS 依赖 PageCache；第二 NodeManager、DataNode 这类守护进程不属于 YARN 容器，不受该参数管控，需要预留内存；如果整机内存耗尽，操作系统 OOM Killer 会随机杀死进程，可能造成 DN 挂掉引发 HDFS 数据风险。
规划时总内存减去 OS、守护进程预留，剩下的才赋值给 nodemanager.resource.memory‑mb。同时还要配置 container 单实例最大最小内存。


- NodeManager 经常掉线，排查步骤？
先用yarn node -list -all确认状态，区分 LOST 和 UNHEALTHY；
登录故障节点检查 NodeManager 进程是否存活；
查看 nodemanager.log，排查 OOM、FullGC、网络报错；
检查系统 messages 日志，确认是否被 OOM‑killer 杀掉；
排查机器 CPU、磁盘 IO、磁盘空间；
排查 NM 到 RM 网络、DNS、Kerberos；
检查 NodeManager JVM 堆内存配置，节点 container 多的时候堆内存不能过小。
最常见原因是 NodeManager 发生长时间 Full GC，心跳 STW 卡住，出现假掉线。


- NM掉线，正在运行的 container 会怎么样？
NM 被标记 LOST 之后，RM 会把该节点上所有 Application 里面的 container 标记失败
Spark 任务会重试失败 task
yarn‑cluster 模式下，如果 AM 刚好在这个节点，会触发 AM 重试，任务整体重启。


- 日志聚合作用
开启后，容器运行日志上传HDFS，任务结束后可以用yarn logs查看
如果不开启，日志只存在各个NM本地，任务结束后很难排查


- 有大量小文件的常见原因以及对策
常见原因：
分区表写入，分区数据量很小；
数据倾斜，reduce输出很多小part 文件；
原始数据源本身就是海量小文件

对策：
读取小文件时候，通过以下参数，逻辑上合并小文件，减少task数量
spark：CombineFileInputFormat，
hive：CombineHiveInputFormat

写小文件时候，可以调整任务并行度
Hive 参数（insert overwrite 写 hive 表）