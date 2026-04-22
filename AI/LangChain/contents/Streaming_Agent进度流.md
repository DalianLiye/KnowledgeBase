[目录](../目录.md)


# 关于Agent进度流
要流式输出agent的执行进度，使用stream或astream方法，并指定stream_mode="updates"
它会在agent的每一步执行完成后，发出一个事件

例如，一个调用一次工具的agent，会按顺序产生以下更新：
- LLM 节点：生成包含工具调用请求的 AIMessage
- 工具节点：执行工具并返回 ToolMessage
- LLM 节点：生成最终的 AI 响应


```python
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"

agent = create_agent(
    model="gpt-5-nano",
    tools=[get_weather],
)
for chunk in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        for step, data in chunk["data"].items():
            print(f"step: {step}")
            print(f"content: {data['messages'][-1].content_blocks}")
```

```json
step: model
content: [{'type': 'tool_call', 'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_OW2NYNsNSKhRZpjW0wm2Aszd'}]

step: tools
content: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]

step: model
content: [{'type': 'text', 'text': 'It's always sunny in San Francisco!'}]
```