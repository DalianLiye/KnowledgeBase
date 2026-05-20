[目录](../目录.md)


# 自定义agent记忆
默认情况下，Agent使用AgentState管理短期记忆，通过messages字段维护完整对话历史\
可以继承AgentState，自由添加自定义字段，扩展记忆能力\
扩展后的自定义状态Schema，通过state_schema参数传入create_agent即可生效


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