# 关于State
在 LangChain中，state（状态）通常指在 agent、chain 或 middleware 执行过程中用于保存、传递和访问上下文信息的数据结构\
它的作用是让不同步骤、组件或调用之间能够共享信息，从而支持更复杂的对话、多步决策和可观察性\
State包含以下两种类型：
- Message State\
  Langchain默认自带的state，agent通过message state自动维护会话历史
- Custom State\
  Custom state需要用户自己定义, agent通过配置custom state，在会话期间来记忆额外的信息

在state里存储信息可被认为是short-term memory（短期记忆）


# Custom State
custom state必须集成AgentState类，类型必须是TypedDict

定义custom state有以下两种方式：
- 通过middleware（推荐）
- 通过create_agent函数的state_schema

通过middleware扩展custom state，可以在概念上将custom state限定到与之相关的middleware和tool上\
这样就可以更清晰、更模块化地管理state的作用域与生命周期

示例: 通过middleware（推荐）\
当需要某些middleware hooks以及与该middleware关联的tool访问特定的custom state时，应该通过middleware来定义这个custom state
```python
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from typing import Any


class CustomState(AgentState):
    user_preferences: dict

class CustomMiddleware(AgentMiddleware):
    state_schema = CustomState
    tools = [tool1, tool2]

    def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
        ...

agent = create_agent(
    model,
    tools=tools,
    middleware=[CustomMiddleware()]
)

# The agent can now track additional state beyond messages
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})
```

示例2: 通过create_agent函数的state_schema\
如果custom state只用于tool，而不是middleware的各生命周期钩子，可以直接使用 create_agent的state_schema 参数声明custom state
```python
from langchain.agents import AgentState


class CustomState(AgentState):
    user_preferences: dict

agent = create_agent(
    model,
    tools=[tool1, tool2],
    state_schema=CustomState
)
# The agent can now track additional state beyond messages
result = agent.invoke({
    "messages": [{"role": "user", "content": "I prefer technical explanations"}],
    "user_preferences": {"style": "technical", "verbosity": "detailed"},
})
```
把状态扩展放到中间件里，可以把这些扩展在，从而