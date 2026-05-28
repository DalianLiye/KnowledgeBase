[目录](../目录.md)


# 关于Batch组API资源
Batch组API资源主要包括：
- job
- cronjob


# job
用于运行一次性任务，任务执行完成后Pod自动销毁，不会重新启动新容器


# cronjob
在Job之上增加定时调度功能，可按照预设周期重复执行任务