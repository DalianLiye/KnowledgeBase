# 发生数据倾斜，如何排查处理

1) 先定位倾斜（排查第一步，不要上来就改代码）
1. Spark UI 看对应 Stage，看各个 Task 的数据读取大小，看到个别 task 数据量远超其他。
2. 看 Shuffle 读写字节数，确认是 shuffle 阶段产生倾斜。
3. SQL 执行计划 explain，找到发生 shuffle 的算子（group by /join）。
4. 找出热点 key：把倾斜 key 打印出来，看是哪几个 key 流量爆炸。

2) Spark3 AQE 自动优化
3) Join 场景倾斜
   BroadcastJoin（广播 join）

4) 大表 join 大表，少数 key 热点（AQE 搞不定的重度倾斜）
  加盐打散方案（最经典，面试必问）