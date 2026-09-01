# Driver
Driver作用
- 执行main()方法
- 解析用户代码
- 生成DAG
- 划分Stage
- 生成Task

# Driver运行模式
- yarn‑client
  Driver跑在提交任务的客户端机器
- yarn‑cluster
  Driver运行在AM容器里面


# main()方法
执行main()方法包括
- 初始化SparkContext/SparkSession
- 解析代码，构建逻辑计划、DAG，划分Job，切分Stage，生成一批Task
- 向YARN申请Executor，把Task分发到Executor去运行 


# DAG
DAG就是整个作业的计算流程图
DAG不是物理执行，只是逻辑流程图
直到Action（count/show/save）才真正触发解析DAG
DAG只在Driver内存中构建，Executor看不到DAG，Driver按照DAG分配任务给executor


# Stage
DAG是整张完整的RDD依赖流程图
遇到宽依赖（Shuffle）就切开，切出来的每一块连续窄依赖片段，就是一个Stage


# 宽依赖和窄依赖
- 窄依赖
上游1个RDD分区的数据，只供给下游最多1个RDD分区（一对一），数据不拆包
- 宽依赖
上游1个RDD分区的数据，拆分开流向下游2个及以上RDD分区（一对多），触发Shuffle


# Job‑Stage‑Task 之间的对应关系
1 次Action → 生成 1 个 Job
Job根据宽窄依赖切割成多个 Stage
1 个 Stage 按照 RDD 分区数生成对应数量 Task

触发：1个Action算子产生 1个Job（count、collect、saveAsTextFile、write 等）
一个 Application 可以有多个 Job，代码写多少Action就有多少Job
Job内部包含一整套DAG，DAGScheduler把Job切分成若干Stage
转换算子(map/filter/reduceByKey)不会生成Job