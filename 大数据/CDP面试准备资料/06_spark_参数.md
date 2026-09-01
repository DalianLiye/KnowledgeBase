# 参数优先级
默认配置 < spark‑defaults.conf < spark‑submit命令行 < 代码内setConf


# 示例
```bash
spark-submit \
--master yarn \
--deploy-mode cluster \
--num-executors 10 \
--executor-cores 4 \
--executor-memory 8G \
--driver-memory 4G \
--conf spark.sql.shuffle.partitions=200 \
--conf spark.default.parallelism=200 \
--conf spark.executor.memoryOverhead=2G \
--conf spark.driver.memoryOverhead=1G \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--conf spark.shuffle.file.buffer=64k \
--conf spark.reducer.maxSizeInFlight=48m \
--conf spark.yarn.maxAppAttempts=2 \
your_app.jar
```

# 常用参数

**spark-submit命令**
- master 
  集群运行模式，yarn /local [*]

- deploy‑mode
  cluster (集群) /client (客户端)

- num‑executors
  Executor数量

- executor‑cores
  每个Executor的CPU核数

- executor‑memory
  每个Executor堆内存 (‑Xmx)

- driver‑memory
  Driver堆内存

- spark.default.parallelism
  默认RDD并行度，shuffle后RDD默认分区数
  仅对RDD生效，SQL不生效
  默认：YARN模式下=executor数量 × executor‑cores
  如果宽依赖时，没有显式指定分区数，那么就按照这个参数设置分区数，如果显式指定了分区数，那么这个参数就不生效

- spark.sql.shuffle.partitions
  SparkSQL / DataFrame/Dataset 做 shuffle 操作后的默认分区数量
  凡是会触发shuffle的算子：join、groupBy、aggregate、distinct、orderBy，shuffle 输出的 RDD 分区数就由该参数控制，对应task数量
  只作用于 SparkSQL、DataFrame；RDD API 不识别这个参数，RDD 走spark.default.parallelism

- spark.executor.memoryOverhead
  Executor堆外内存，YARN容器总内存 = executor‑memory + memoryOverhead
  默认`max(executorMemory*0.1,384M)`

- spark.driver.memoryOverhead
  Driver堆外内存
  OOM 除了调堆内存，很多时候要加大堆外内存

- spark.shuffle.file.buffer
  shuffle写磁盘的缓冲区，默认32k，调64k/128k，减少磁盘IO

- spark.reducer.maxSizeInFlight
  reduce端拉取shuffle数据的缓冲区，默认48M

- spark.shuffle.io.maxRetries
  shuffle拉取失败重试次数，默认3

- spark.shuffle.io.retryWait
  重试等待时间，默认5s

- spark.shuffle.sort.bypassMergeThreshold
  分区数小于该值不做排序，默认200

- spark.serializer=org.apache.spark.serializer.KryoSerializer
  Kryo序列化，比Java序列化更快、占用更小，生产环境必开

- spark.sql.adaptive.enabled=true
  自适应查询计划，根据数据变化动态调整查询计划，提升查询性能