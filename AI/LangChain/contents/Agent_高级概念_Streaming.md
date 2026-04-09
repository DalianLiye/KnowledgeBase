[目录](../目录.md)


# 关于Streaming

调用agent的invoke方法获取最终结果时，由于agent可能需要执行多步推理，整体过程会比较耗时\
为了实时查看执行进度与中间结果，可通过流式返回（stream）在每一步执行时实时返回消息，而非等待所有步骤完成后才一次性返回最终结果

示例:
```python
from langchain.messages import AIMessage, HumanMessage

for chunk in agent.stream({
    "messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]
}, stream_mode="values"):
    # Each chunk contains the full state at that point
    latest_message = chunk["messages"][-1]
    if latest_message.content:
        if isinstance(latest_message, HumanMessage):
            print(f"User: {latest_message.content}")
        elif isinstance(latest_message, AIMessage):
            print(f"Agent: {latest_message.content}")
    elif latest_message.tool_calls:
        print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
```