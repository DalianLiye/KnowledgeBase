# Spark连接及初始化

## Spark建立连接(scala)
使用Scala开发Spark应用，必须使用兼容的Scala版本
比如，Spark3.5.3默认编译适配Scala2.12

如果不兼容，可以重新编译Spark，以适配Scala版本，但生产一般直接用官方预编译包

开发Spark应用需要引入Spark的Maven依赖，Maven中央库坐标如下：
```text
groupId = org.apache.spark
artifactId = spark‑core_2.12
version = 3.5.3
```
注：
- artifactId末尾`_2.12`代表适配Scala2.12版本
- spark‑core_2.12表示Scala版本必须2.12.x，不能用2.13，版本不匹配直接报类找不到

如果Spark要访问HDFS集群，需要引入和集群HDFS版本匹配的hadoop‑client依赖
```text
groupId = org.apache.hadoop
artifactId = hadoop‑client
version = <your‑hdfs‑version>
```
注:
- `<your‑hdfs‑version>`替换成实际的Hadoop版本
- 如果只需要访问HDFS，引入hdfs-client即可
- 如果用`spark‑submit`提交到集群，Spark的集群环境已经带hadoop依赖(每台机器的spark/jars目录下)
  因此，项目里可以不用打包hadoop‑client,运行时直接加载环境中的jar
  如果Maven中设置scope为provided，表示它只在编译阶段使用该依赖，运行时会使用集群环境提供的依赖jar，不会打进最终Jar包
  如果强行打入，很容易产生版本冲突

最后在代码中导入Spark核心类
```scala
import org.apache.spark.SparkContext
import org.apache.spark.SparkConf
```
- **SparkConf**
  设置Spark配置
- **SparkContext**
  Spark入口上下文，用于创建RDD


## 初始化Spark
创建Spark程序需依次执行以下：
1) 构建SparkConf对象
   该对象存放应用的配置信息，承载配置，应用名、master、各类调优参数
2) 通过SparkConf对象，创建SparkContext对象
   Spark核心入口上下文，连接集群，创建RDD，调度Job

示例:
```scala
val conf = new SparkConf().setAppName(appName).setMaster(master)
new SparkContext(conf)
```
appName: 应用名称，会展示在Spark集群WebUI界面
master: Spark/Mesos/YARN集群地址，特殊值local代表本地模式运行

一个JVM进程内，同一时刻只能有一个活跃的SparkContext
创建新SparkContext前，必须调用stop()关闭正在运行的SparkContext，否则会报错
示例:
```scala
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

val conf1 = new SparkConf().setAppName("demo1").setMaster("local[*]")
val sc1 = new SparkContext(conf1)

// 没有 stop，直接再创建第二个 SparkContext，报错
val conf2 = new SparkConf().setAppName("demo2").setMaster("local[*]")
val sc2 = new SparkContext(conf2)

// 有 stop，再创建第二个 SparkContext，成功
sc1.stop()  // 关闭旧的上下文
val conf2 = new SparkConf().setAppName("demo2").setMaster("local[*]")
val sc2 = new SparkContext(conf2)
```

实际生产环境，不要在代码里硬编码master地址，要通过spark‑submit提交命令传入master参数
仅本地调试、单元测试的时候，可以写local，让Spark在本进程内部运行
这样，就可以不修改代码，通过给spark submit提交命令里为master参数设置不同的值，既可以实现本地local测试，也可以提交YARN集群运行