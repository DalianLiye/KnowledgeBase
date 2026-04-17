[目录](../目录.md)


# 关于调用配置

在调用模型时，可以通过config参数传入一个RunnableConfig字典，实现对运行时行为、回调函数和元数据跟踪的动态控制

**关于RunnableConfig**\
它是LangChain提供的标准运行配置字典，用来在每次调用 invoke() / stream() / batch() 时动态传入额外控制参数\
相当于：每次调用模型时的 “运行时参数”

常用配置选项包括
```python
response = model.invoke(
    "Tell me a joke",
    config={
        "run_name": "joke_generation",   # 本次运行的自定义名称
        "tags": ["humor", "demo"],       # 分类标签
        "metadata": {"user_id": "123"},   # 自定义元数据
        "callbacks": [my_callback_handler]  # 回调处理器
    }
)
```

核心应用场景：
- 使用LangSmith追踪进行调试
- 实现自定义日志或监控
- 在生产环境控制资源使用


# RunnableConfig关键属性

- **run_name**\
  string，用于在日志和追踪中标识本次调用，不会被子调用继承
- **tags**\
  string[]，标签列表，用于在调试工具中过滤和分类，会被所有子调用继承
- **metadata**\
  object，自定义键值对，用于附加业务上下文，会被所有子调用继承
- **max_concurrency**\
  number，控制 batch() / batch_as_completed() 调用时的最大并发数
- **callbacks**\
  array，回调处理器列表，用于监控和响应执行过程中的事件
- **recursion_limit**\
  number，设置链的最大递归深度，防止复杂流水线中出现无限循环