[目录](../目录.md)


# 关于CronJob
基于Job扩展，增加定时调度能力，支持按cron表达式周期重复执行任务\
每次调度都会自动创建Job来完成实际工作



## CronJob
CronJob主要用于在k8s中周期性运行计划任务，它与linux中的crontab相同

**注:**\
CronJob执行的时间是controller-manager的时间，所以一定要确保controller-manager时间是准确的, 即要与现实的时间同步
虽然k8s CronJob跟linux crontab类似，但是它们之间是没有关联的，CronJob并不基于crontab


**cron表达式**\
一共有5位（* * * * *），每位数分别代表不同的时间单位

- n=1: 分钟 (0 - 59)
- n=2: 小时 (0 - 23)
- n=3: 月的某天 (1 - 31)
- n=4: 月份 (1 - 12)
- n=5: 周的某天 (0 - 6), 0-6代表周日(0)到周一(6)

**示例**\
执行kubectl create命令创建如下Cronjob，文件名：cron-job-pd.yaml
整个过程如下：
1) CronJob根据定义的schedule(每分钟一次)触发调度
2) CronJob Controller在触发时间点自动创建一个Job资源
3) 这个Job资源会创建一个或多个 Pod(取决于 Job的配置，默认是一个 Pod)
4) Pod运行定义的容器（ busybox:1.28），并执行命令

```yaml
apiVersion: batch/v1
kind: CronJob  # 资源类型是CronJob
metadata:
  name: cron-job-test   # cronjob的名字
spec:
  concurrencyPolicy: Allow  # 并发调度的策略，Allow：允许并发调度，Forbid: 不允许并发执行，Replace：如果之前的任务还没有执行完，就直接执行新的，放弃上一个任务
  failedJobsHistoryLimit: 1  # 保留多少个失败的任务
  successfulJobsHistoryLimit: 3  # 保留多少个成功的任务
  suspend: false  # 是否挂起任务，若为true，则该任务不会执行
# startingDeadlineSeconds: 30  # 间隔多长时间检测失败的任务并重新执行，时间不能小于10 
  schedule: "* * * * *"  # 调度策略
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: busybox
            image: busybox:1.28
            imagePullPolicy: IfNotPresent
            command:
            - /bin/sh
            - -c
            - date; echo Hello from the k8s cluster
          restartPolicy: OnFailure
```


**Pod和Job的命名**\
Pod名字是由 Job自动生成的，通常格式是： <job-name>-<随机字符串>\
Job 名字又是由 CronJob 名字加上时间戳组成, 即 cron-job-test-<时间戳>-<随机字符串>

Pod会被调度到集群中某个节点上，具体节点由调度器根据资源情况和调度策略决定

查看创建好的cronjob，执行命令：
```shell
kkubectl get cronjob
```