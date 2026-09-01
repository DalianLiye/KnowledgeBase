# RDD创建
RDD创建来源包括：
- **外部数据集**
  引用外部存储系统中的数据集，例如共享文件系统、HDFS、HBase，或者任意实现了Hadoop InputFormat的数据源
- **并行化集合**
  对Driver程序中已经存在的集合做并行化，即parallelize
  

# 外部数据集
Spark支持读取文本文件、SequenceFile，以及任意其他Hadoop InputFormat数据源
Spark可以从Hadoop支持的任意存储源创建分布式数据集，包括本地文件系统、HDFS、Cassandra、HBase、亚马逊S3等

可以使用SparkContext.textFile()方法创建文本文件RDD

示例1: 
基于HDFS创建的RDD对象rdd，包含的是hdfs文件的元数据信息，包括文件的路径，block信息等，而不是hdfs文件内部的真实数据
```scala
val rdd = sc.textFile("hdfs://log.txt")
```

示例2: 
基于本地文件创建的RDD对象distFile，创建后可以执行数据集算子操作
比如map、reduce算子，把所有行的字符长度累加求和，该方法接收文件URI，把文件读取为行的集合
```scala
val distFile = sc.textFile("data.txt")
distFile.map(s => s.length).reduce((a, b) => a + b)
```
说明:
1) 只要实现Hadoop InputFormat接口，Spark就可以读取，不局限HDFS, 本地磁盘、对象存储S3、HBase、Cassandra都属于这类
   文件URI可以包括：本机本地路径，hdfs://、s3a://这类URI
2) 执行textFile()函数，返回RDD[String]，RDD里面每一条元素对应文件的一行文本
   返回RDD[String]只是生成RDD元数据，不会真正读取文件
   触发Action算子（reduce），Executor才会去读取外部存储真实数据


## Spark读取文件注意事项
- 如果使用本地文件系统路径，仅仅Driver有文件不行，Worker节点也必须能在相同路径访问该文件
  要么把文件拷贝到所有Worker机器，要么使用网络挂载的共享文件系统
  集群环境优先用HDFS，不要读本地磁盘
- Spark所有基于文件的输入方法（包括textFile），支持读取目录、压缩文件(压缩文件直接支持读，不需要手动解压)、通配符
  读取多个文件时，分区的顺序由文件系统返回文件的顺序决定，不一定按照文件路径字典序(分区之间数据顺序无法保证)
  同一个分区内部，数据行保持原文件中的顺序
  示例：
  ```text
  textFile("/my/directory")读取整个目录
  textFile("/my/directory/*.txt")匹配 txt 后缀
  textFile("/my/directory/*.gz")读取gz压缩文件
  ```
- textFile支持可选第二个参数，用来控制分区数量
  默认规则：HDFS中一个Block对应一个分区（HDFS默认块大小128MB）
  可以传入更大数值，增加分区数
  不能设置比Block数量更少的分区，想变少只能后续调用coalesce/repartition
  ```scala
  sc.parallelize(集合, N)  //可以自由指定分区，可大可小
  sc.textFile(path,N)  //N只能大于等于block数量，不能压小
  ```

## 其他数据格式
除文本文件之外，Spark Scala API 还支持其他多种数据格式
- **wholeTextFiles**
  SparkContext.wholeTextFiles读取包含大量小文本文件的目录，返回(文件名, 文件完整内容)键值对
  分区由数据本地性决定，可能会出现分区过少
  该方法第二个可选参数，用来设置最小分区数
- **SequenceFile**
  使用sequenceFile[K, V]读取SequenceFile，K、V为文件的key、value类型
  类型需要实现Hadoop的Writable接口，例如IntWritable、Text
  Spark做了封装，可以直接写原生Scala/Java类型，例如sequenceFile[Int, String]，内部自动映射为IntWritable、Text
- **其他Hadoop InputFormat**
  - hadoopRDD
    old API，适配旧版MapReduce API，传入JobConf、InputFormat 类、key、value 类，配置方式和写Hadoop MR任务一致
  - newAPIHadoopRDD
    现在主流使用，适配新版MapReduce API（org.apache.hadoop.mapreduce包）
    只要是Hadoop InputFormat都可以通过这两个方法接入Spark，即凡是Hadoop能读的数据源，Spark都可以套这两个API读取
- **ObjectFile**
  RDD.saveAsObjectFile/sc.objectFile
  把RDD以Java序列化对象格式保存读取
  缺点: Java序列化存储，只适合Spark内部使用，不能给其他工具读取，序列化开销大，性能不如Avro这类专用列式格式，生产优先Avro、Parquet
  优点: 任意RDD都可以直接存，不需要定义schema
  
**wholeTextFiles和textFile**
- textFile
  返回数据：每行 → 一条记录
  适用场景: 大文件，按行处理日志
- wholeTextFiles
  返回数据：(文件名，整个文件内容) → 一条记录
  适用场景: 一堆大量小文件，需要拿到完整文件内容 + 文件名
注：大量小文件用 wholeTextFiles 容易分区太少，传入第二个参数设置最小分区


# 并行化集合
并行化集合是在Driver程序中，对已有集合（Scala 序列 Seq）调用SparkContext.parallelize()方法创建出来
集合中的元素会被复制，生成一个可以并行运算的分布式数据集
创建出来的RDD，只保存元数据：来源标记、分片策略，不会保存集合内部真实元素数据，原始集合数据仍然存放在Driver进程内存中

示例：创建包含数字1‑5的并行化集合
```scala
val data = Array(1, 2, 3, 4, 5)
val distData = sc.parallelize(data)
```
distData包含的是数组List的元数据信息，包括数组的元素，数组的索引等，不是数组已经分发出去的真实数据
distData创建后，分布式数据集distData就可以执行并行操作
例如调用distData.reduce((a, b) => a + b)对数组元素求和

**并行化集合的分区**
分区数量是并行化集合重要参数，数据集会被切分为若干分区
Spark集群中，每一个分区对应启动一个Task任务
经验配置：集群中每1颗CPU，建议配置2‑4个分区

分区数设置方式
- 自动设置
  Spark会根据集群环境自动设置分区数
  ```scala
  sc.parallelize(data) // 自动设置分区数
  ```
- 手动设置
  parallelize的第二个参数传入
  ```scala
  sc.parallelize(data, 10) // 手动设置分区数为 10
  ```
注:
- slices这个术语和partitions(分区)是同义词，用于兼容旧版本
- parallelize来源于Driver本地集合
  定义RDD阶段只是记录元数据，触发Action算子之后，数据才真正分发到Executor
  元素是从Driver端复制过去，并不是把集合对象直接发送引用