# Spark Shell
Spark Shell是一个交互式Scala终端，用来调试、测试代码
底层实现上, spark‑shell本质就是调用通用的spark‑submit脚本

在Spark shell交互环境中，系统已经预先创建好了一个适配解释器的SparkContext，变量名固定为sc
因此，进入Spark Shell后，可以直接使用变量sc，不要再new SparkConf + new SparkContext手动新建，会报错
单JVM只能有一个活跃SparkContext，shell已经占了一个


# 参数
- **master**
  指定该上下文要连接的集群master地址
- **jars**
  指定逗号分隔的jar包列表，把第三方jar加入运行时类路径
- **packages**
  指定逗号分隔的Maven坐标列表，为shell会话添加依赖（例如Spark Packages组件）
- **repositories**
  指定存放额外依赖的仓库仓库地址，例如Sonatype仓库

# 示例
- 示例1:使用 4 个 CPU 核心运行 spark‑shell
```bash
./bin/spark‑shell --master local[4]
```

- 示例2：同时把 code.jar 加入类路径
```bash
./bin/spark‑shell --master local[4] --jars code.jar
```

- 示例3：通过 Maven 坐标引入外部依赖
```bash
./bin/spark‑shell --master local[4] --packages "org.example:example:0.1"
```

- 示例4：查看帮助信息
```bash
spark‑shell --help
```