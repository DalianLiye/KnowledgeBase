[目录](../目录.md)


# 关于Agent调用

Agent通过更新state触发调用\
每个Agent维护一组消息序列，调用时只需传入新的用户消息即可执行

示例：
```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
```

Agent的全部数据就是state，而messages是state里最核心的字段\
调用 agent.invoke( { "messages": ... } )就相当于直接向state里写入新的用户消息，完成state更新\
state一更新，Agent就自动运行