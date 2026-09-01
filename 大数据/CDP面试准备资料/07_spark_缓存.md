# 缓存cache/persist
把RDD 计算后的中间结果保存下来（内存 / 磁盘），避免重复重新计算前面一整套 RDD 依赖链（重新跑 Stage、重新 shuffle），提升重复使用RDD的性能
cache()=persist()的简化版本