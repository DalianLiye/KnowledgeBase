[目录](../目录.md)


# V2流式输出格式

要求：LangGraph >= 1.1
在调用 stream() 或 astream() 时传入 version="v2"，即可获得统一的输出格式。无论使用哪种流模式或组合多少种模式，每个数据块都是一个包含 type、ns 和 data 键的 StreamPart 字典

示例:v2 (new)
```python
# Unified format — no more tuple unpacking
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
    version="v2",
):
    print(chunk["type"])  # "updates" or "custom"
    print(chunk["data"])  # payload
```

示例:v1 (current default)
```python
# Must unpack (mode, data) tuples
for mode, chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode=["updates", "custom"],
):
    print(mode)   # "updates" or "custom"
    print(chunk)  # payload
```

V2 格式同时也改进了 invoke() 方法：它会返回一个 GraphOutput 对象，包含 .value 和 .interrupts 属性，将状态数据与中断元数据清晰地分离开来：

```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Hello"}]},
    version="v2",
)
print(result.value)       # state (dict, Pydantic model, or dataclass)
print(result.interrupts)  # tuple of Interrupt objects (empty if none)
```

有关 V2 格式的更多细节，包括类型收窄、Pydantic / 数据类的强制转换以及子图流式处理，请参阅 LangGraph 流式文档