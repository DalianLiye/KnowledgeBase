通过更新state，就可以调用agent\
每一个agent都包含了一连串message\
如果要调用agent，那就发送一个新的message

示例：
```python
result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in San Francisco?"}]}
)
```