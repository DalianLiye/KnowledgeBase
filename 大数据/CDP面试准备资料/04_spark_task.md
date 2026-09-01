# Task 
Task是Spark最小的执行单元，真正发给Executor线程去跑的任务

Task才是真正干活的实体，由Executor执行
Executor只认识Task，不知道DAG、不知道Stage，只执行收到的Task

一个Stage有多少个RDD分区，就会生成多少个Task
1个Task处理1个Stage的RDD分区

**Task类型**
- ShuffleMapTask
  属于ShuffleMapStage
  执行完计算，输出shuffle数据写入Executor本地磁盘，给后面Stage读取
- ResultTask
  属于ResultStage
  执行计算后，把结果直接返回Driver，不写shuffle文件
  一个ResultStage里面全部是ResultTask

**Task执行规则**
同一个Stage内部的多个Task可以并行跑，分配到不同Executor
必须当前Stage所有Task全部执行完成，Driver才会提交下一个Stage的Task
Task失败，Driver会重新调度该Task重试


Task 类型不看它读不读 shuffle，看本阶段是否输出 shuffle。
中间 Stage 即使读取上游 shuffle 做 reduce 逻辑，只要还要输出 shuffle 给下一个阶段，task 就是 ShuffleMapTask；只有最后 Stage 才是 ResultTask。

