# ResourceManager
- yarn.resourcemanager.scheduler.class 指定调度器
- yarn.resourcemanager.am.max-attempts AM 最大重试次数

# NodeManager（机器资源配置重中之重）
- yarn.nodemanager.resource.memory-mb：单节点 YARN 总可用内存
- yarn.nodemanager.resource.cpu-vcores：单节点 YARN 总可用 CPU 核数
⚠️ 注意：不能把机器全部内存 CPU 给 YARN，要预留系统、HDFS、Hive、操作系统资源

# Container 容器限制
- yarn.scheduler.minimum-allocation-mb 最小容器内存
- yarn.scheduler.maximum-allocation-mb 最大容器内存
- yarn.scheduler.minimum-allocation-vcores 最小 CPU
- yarn.scheduler.maximum-allocation-vcores 最大 CPU
坑：Spark 任务 OOM 很多时候就是 Container 最大内存设置太小。

- yarn.nodemanager.vmem-pmem-ratio
虚拟内存比率，经常出现虚拟内存超限杀掉 container，排错高频
默认是2.1，jvm经常使用虚拟内存，一旦超标，会杀死container，但其实物理内存没有满
解决方法：酌情提高虚拟内存比率，比如到4，还有就是关闭虚拟内存检查