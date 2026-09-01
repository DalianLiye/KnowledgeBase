# yarn常用命令

查看yarn集群状态
```bash
yarn node -list
```

查看所有application
```bash
yarn application -list
```

kill任务
```bash
yarn application -kill application_xxxx
```

查看队列信息（Capacity调度器）
```bash
yarn queue -status root.default
```
任务提交一直PENDING
执行这条命令看：Applications pending、Pending Resources，如果有数值，说明队列资源耗尽，任务在排队。
核对队列配置是否生效
对比输出里的 Capacity、Maximum Capacity，确认 yarn‑site.xml 修改的队列配置是否刷新生效。


查看日志
```bash
yarn logs -applicationId application_xxxx
```

统计容器状态，用于查看资源使用情况
```bash
yarn top
```