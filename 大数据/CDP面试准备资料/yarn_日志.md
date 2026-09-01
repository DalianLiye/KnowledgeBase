# 日志聚合
YARN 日志聚合，是应用结束后，各个 NodeManager 把本机该应用所有 container 日志上传到 HDFS 集中存储，随后删除本地日志。
开启之后，使用yarn logs -applicationId即可统一查看全部容器日志，不用登录各个物理节点。
关键点：只有任务结束才会聚合；运行中任务日志还在 NM 本地，拿不到聚合日志。
核心开关yarn.log‑aggregation‑enable；可以配置 HDFS 上日志自动过期清理。
长驻不退出的应用不会触发聚合，日志堆积在 NodeManager 本地磁盘。