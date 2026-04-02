当调用agent的invoke方法获得最终回答时，有时agent需要执行多个步骤导致整个过程可能会比较耗时\
为了在这个过程中看到进度或中间结果，可以在agent执行每一步时把产生的消息“流式”返回（stream）\
即实时把中间响应发送给调用方，而不是等到所有步骤完成后才一次性返回最终结果

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