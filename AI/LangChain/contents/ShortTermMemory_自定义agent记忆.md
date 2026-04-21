[目录](../目录.md)


# 自定义agent记忆

默认情况下，agent使用AgentState来管理短期记忆，具体来说，是通过messages字段来维护对话历史
可以继承AgentState来添加额外字段
自定义状态schema通过state_schema参数传递给create_agent

```python
from langchain.agents import create_agent, AgentState
from langgraph.checkpoint.memory import InMemorySaver


class CustomAgentState(AgentState):
    user_id: str
    preferences: dict

agent = create_agent(
    "gpt-5",
    tools=[get_user_info],
    state_schema=CustomAgentState,
    checkpointer=InMemorySaver(),
)

# Custom state can be passed in invoke
result = agent.invoke(
    {
        "messages": [{"role": "user", "content": "Hello"}],
        "user_id": "user_123",
        "preferences": {"theme": "dark"}
    },
    {"configurable": {"thread_id": "1"}})
```