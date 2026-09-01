# 算子
算子就是RDD上面提供的一个个方法/函数，用来做数据处理操作。
Spark 把数据计算的操作封装成方法，这些方法就叫算子。

# 算子类型
- 转换算子 (Transformation)：只记账，不干活，懒加载；返回新 RDD
- 行动算子 (Action)：真正干活，触发 Job；不返回 RDD


# 转换算子(Transformation)
调用后不执行计算，Driver仅记录RDD依赖，构建 DAG
返回一个新RDD
遇到Action才会真正执行

常见窄依赖转换算子（无 shuffle）
map、filter、flatMap、mapPartitions、union、sample、distinct(会shuffle)
常见宽依赖转换算子（会产生 Shuffle！）
reduceByKey、groupByKey、join、cogroup、repartition、coalesce、sortByKey
reduceByKey、groupByKey 这些是转换算子！不是 Action！只是内部会触发 shuffle 切割 Stage


reduceByKey和groupByKey 
shuffle前是否做map端局部聚合，是最大差别，reduceByKey会做map端局部聚合，groupByKey不会做map端局部聚合。


特殊转换算子
cache() / persist()：仅给 RDD 打缓存标记，属于转换，不会立刻缓存数据，等 Action 才生效。

# 行动算子 Action（触发 Job）
触发 Job，DAGScheduler 切割 Stage，生成 Task，Executor 执行计算。
不返回 RDD，返回本地结果，或者输出到外部存储
每执行一次 Action，就生成一个新 Job

常见 Action 算子
- 返回结果到 Driver：
count()、collect()、first()、take(n)、reduce()、foreach()

- 输出到外部存储 (HDFS 等)：
saveAsTextFile()、saveAsObjectFile()













- 转换算子 Transformation
  map、filter、flatMap、reduceByKey、join、cache()
  调用这些方法，不会读数据、不会跑 Task、不会启动 Executor 计算。
Driver 端仅仅记录 RDD 的依赖关系（DAG 逻辑图）。
- 行动算子 Action（触发计算）
  count、collect、saveAsTextFile、write、take
  遇到 Action，才真正提交 Job，切割 Stage，生成 Task，Executor 开始读数据做计算。



  # 关于懒加载(惰性求值)
转换算子只记录逻辑，不真正计算数据，直到行动算子 (Action)，才触发真实的计算

**两类算子**
转换算子Transformation（懒）
行动算子Action（触发计算）

cache () 也是懒加载
cache() 只是给 RDD 打上 “需要缓存” 标记。
必须第一次 Action 跑完之后，才会把数据存入 Executor 内存 / 磁盘。
没有 Action，cache 完全不生效


为什么 Spark 设计懒加载
减少 IO 开销：Spark 可以把一整套算子合并，一次性计算，而不是算一步输出一步。
DAG 优化：Driver 拿到完整算子链条后，才切割 Stage、识别 shuffle、做优化。
如果每一步都立即计算，中间结果要落地磁盘，性能极差


运维视角看到的现象（非常重要）
任务提交后，代码飞快跑完一大段，Spark UI 看不到 Job、Stage、Task；直到执行到写表 /count，瞬间大量 Task 启动。这就是懒加载。
如果循环里面写 Action，每循环一次触发一次 Job，会生成大量 Job，资源浪费。
用户误以为cache已经缓存数据，但是没有执行 Action，Storage 页面看不到任何缓存数据。


易错点
❌转换算子执行的时候，Executor 运行 map/filter 函数
✅转换算子这行代码跑在 Driver；算子内部的 lambda 函数，序列化后打包进 Task，Action 之后才在 Executor 执行。


Spark 懒加载即惰性求值
转换算子只在 Driver 记录 RDD 依赖逻辑，不触发实际计算
只有行动算子 Action 才会触发 Job，提交 Stage 与 Task，Executor 真正执行计算
cache/persist 也是懒标记，需要 Action 才真正缓存数据

**总结**
转换算子记账，Action才干活