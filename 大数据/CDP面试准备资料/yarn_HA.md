ResourceManager HA，双RM，ZK做故障转移
状态存储在ZK，避免单点故障
standby RM不处理业务，发生故障自动切换active