[目录](../目录.md)


# 关于Agent进度流
如需流式获取Agent执行进度，调用stream或astream方法，并指定流式模式为stream_mode="updates"即可
该模式会在Agent每一个执行步骤结束后，主动推送状态事件

以单次工具调用的Agent为例，事件推送顺序如下：
- LLM节点：生成包含工具调用请求的 AIMessage
- 工具节点：执行对应工具，返回工具执行结果消息
- LLM节点：整合结果，生成最终AI回答


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