Middleware可以为agent在不同的执行阶段提供强大的自定义扩展能力

例如，Middleware可以实现以下场景：
- 调用model之前处理state
- 修改或验证model返回值
- 自定义tool执行报错时的处理逻辑
- 基于state和context实现动态model选择
- 添加自定义日志，监控以及分析

Middleware可以无缝嵌入到 agent 的执行流程里，在不修改agent核心逻辑的情况下，在关键节点拦截并修改数据流