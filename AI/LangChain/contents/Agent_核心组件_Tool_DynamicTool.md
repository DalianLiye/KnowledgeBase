[目录](../目录.md)


# 关于Dynamic Tool
Dynamic tool是指Agent可以在运行时，动态选择并执行合适的工具

Dynamic Tool有两种实现方式：
- Filtering pre-registered tools（预先注册所有工具，运行时动态筛选）
- Runtime tool registration（运行时动态注册新工具）


## Filter Pre-Registered Tools
Agent创建时预先注册全部工具，运行时根据状态、权限、配置动态筛选可用工具

适用场景：
- 所有工具预先可知
- 根据条件动态启用/禁用工具
- 工具本身固定，但可用性动态变化

示例1：根据state动态选择Tool
```python
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def state_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on conversation State."""
    # Read from State: check if user has authenticated
    state = request.state
    is_authenticated = state.get("authenticated", False)
    message_count = len(state["messages"])

    # Only enable sensitive tools after authentication
    if not is_authenticated:
        tools = [t for t in request.tools if t.name.startswith("public_")]
        request = request.override(tools=tools)
    elif message_count < 5:
        # Limit tools early in conversation
        tools = [t for t in request.tools if t.name != "advanced_search"]
        request = request.override(tools=tools)

    return handler(request)

agent = create_agent(
    model="gpt-4.1",
    tools=[public_search, private_search, advanced_search],
    middleware=[state_based_tools]
)

# 假设有 chat_history 和 user_is_authenticated
response = agent.invoke(
    input="帮我查一下内部数据",
    state={
        "messages": chat_history,
        "authenticated": user_is_authenticated,
    },
)
```


示例2：根据存储里的信息，动态选择Tool
```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable
from langgraph.store.memory import InMemoryStore

@dataclass
class Context:
    user_id: str

@wrap_model_call
def store_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Store preferences."""
    user_id = request.runtime.context.user_id

    # Read from Store: get user's enabled features
    store = request.runtime.store
    feature_flags = store.get(("features",), user_id)

    if feature_flags:
        enabled_features = feature_flags.value.get("enabled_tools", [])
        # Only include tools that are enabled for this user
        tools = [t for t in request.tools if t.name in enabled_features]
        request = request.override(tools=tools)

    return handler(request)

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, analysis_tool, export_tool],
    middleware=[store_based_tools],
    context_schema=Context,
    store=InMemoryStore()
)
```

示例3：根据运行时上下文，动态选择Tool
```python
from dataclasses import dataclass
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@dataclass
class Context:
    user_role: str

@wrap_model_call
def context_based_tools(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
    """Filter tools based on Runtime Context permissions."""
    # Read from Runtime Context: get user role
    if request.runtime is None or request.runtime.context is None:
        # If no context provided, default to viewer (most restrictive)
        user_role = "viewer"
    else:
        user_role = request.runtime.context.user_role

    if user_role == "admin":
        # Admins get all tools
        pass
    elif user_role == "editor":
        # Editors can't delete
        tools = [t for t in request.tools if t.name != "delete_data"]
        request = request.override(tools=tools)
    else:
        # Viewers get read-only tools
        tools = [t for t in request.tools if t.name.startswith("read_")]
        request = request.override(tools=tools)

    return handler(request)

agent = create_agent(
    model="gpt-4.1",
    tools=[read_data, write_data, delete_data],
    middleware=[context_based_tools],
    context_schema=Context
)
```


## Runtime tool registration
在Agent运行过程中动态注册、加载、执行工具

需要通过两个hook实现：
- wrap_model_call：将动态工具加入请求，即将Dynamic Tool注册到请求里
- wrap_tool_call：指定动态工具的执行函数，即指定Dynamic Tool由具体哪一个函数执行
注：wrap_tool_call是必需的，因为Agent需要知道工具对应的具体执行函数，否则无法运行工具是

适用场景：
1) 工具从MCP服务器等外部服务动态发现
2) 工具根据用户配置动态生成
3) 统一工具注册中心，多团队共享管理
   例如，一个公司很多team都有自己的agent，如果没有这个Tool目录/注册表中心，那么需要每一个team的agent都要有自己的注册的Tool以及对应的函数实现，不便于管理\
   有了这个外部的统一的Tool目录/注册中心，它提供统一管理的Tool列表以及具体实现 (endpoint)\
   那么各个team就可以从这个中心获取获取Tool ，然后注册给自己的agent(通过wrap_model_call hook), 再将具体的实现函数(通过wrap_tool_call hook)\
   关于具体的实现函数，如果中心提供了各个tool的endpoint，可以指定endpoint，否则必须在自己的agent上有自己的函数定义

示例：
```python
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, ModelRequest, ToolCallRequest

# A tool that will be added dynamically at runtime
@tool
def calculate_tip(bill_amount: float, tip_percentage: float = 20.0) -> str:
    """Calculate the tip amount for a bill."""
    tip = bill_amount * (tip_percentage / 100)
    return f"Tip: ${tip:.2f}, Total: ${bill_amount + tip:.2f}"

class DynamicToolMiddleware(AgentMiddleware):
    """Middleware that registers and handles dynamic tools."""

    def wrap_model_call(self, request: ModelRequest, handler):
        # Add dynamic tool to the request
        # This could be loaded from an MCP server, database, etc.
        updated = request.override(tools=[*request.tools, calculate_tip])
        return handler(updated)

    def wrap_tool_call(self, request: ToolCallRequest, handler):
        # Handle execution of the dynamic tool
        if request.tool_call["name"] == "calculate_tip":
            return handler(request.override(tool=calculate_tip))
        return handler(request)

agent = create_agent(
    model="gpt-4o",
    tools=[get_weather],  # Only static tools registered here
    middleware=[DynamicToolMiddleware()],
)

# The agent can now use both get_weather AND calculate_tip
result = agent.invoke({
    "messages": [{"role": "user", "content": "Calculate a 20% tip on $85"}]
})
```