[目录](../目录.md)


# 关于State

LangChain中的State是执行过程中存储、传递上下文的数据结构，用于组件间信息共享，支持多轮对话与复杂决策
State分为两类：
- **Message State**\
  内置默认state，用于自动维护会话消息历史
- **Custom State**\
  用户自定义state，用于存储消息外的额外信息

状态存储内容等价于Agent的短期记忆（short-term memory）


# Custom State

LangChain 1.0+强制要求：自定义State必须继承AgentState，且必须为TypedDict类型，Pydantic模型和dataclasses不再支持
定义方式有两种：
- 通过Middleware（推荐）
  将State与对应中间件、工具绑定，作用域更内聚、模块化更强，适合复杂项目
- 通过create_agent (state_schema=...)
  仅适用于State只给工具使用、不涉及中间件钩子的简单场景，为兼容旧版保留，不推荐新项目使用

优先通过middleware定义自定义State，便于隔离作用域、清晰管理生命周期\
state_schema仅作向后兼容，不建议使用


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
通过中间件（middleware）定义自定义state，优于在create_agent上通过state_schema定义\
因为这种方式可以让state的扩展，在逻辑上只作用于相关的中间件和工具，更内聚、更清晰\
为了向后兼容，create_agent上的state_schema仍然被支持，但不推荐使用