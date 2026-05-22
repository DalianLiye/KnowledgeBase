[目录](../目录.md)


# 关于动态选择工具
Agent运行时，可以动态选择执行合适的工具

实现方式：
- 动态筛选预注册工具（预先注册所有工具，运行时动态筛选）
- 运行时动态注册新工具


# 动态筛选预注册工具
创建Agent时预先注册全部工具，运行时根据状态、权限、配置等信息动态筛选可用工具

适用场景：
- 所有工具预先可知
- 根据条件动态启用/禁用工具
- 工具本身固定，但可用性动态变化


## 示例
- 示例1：根据请求状态动态选择工具
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
  说明:agent调用invoke函数时，传递的state参数里，messages和authenticated字段完全是自定义的，这里定义了什么字段，state_based_tools函数l里request.state就能获取什么字段


- 示例2：根据存储信息，动态选择工具
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

- 示例3：根据运行时上下文，动态选择工具
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


# 运行时动态注册新工具
Agent运行过程中动态注册、加载、执行工具

通过以下钩子函数实现：
- **wrap_model_call**\
  将动态工具加入请求，即将动态工具注册到请求里\
  wrap_model_call触发时机：Agent让大模型思考之前，即:Agent收到用户问题 → 先跑wrap_model_call → 再把请求发给大模型
- **wrap_tool_call**\
  指定动态工具的执行函数，即指定动态工具由某一具体函数执行\
  wrap_tool_call触发时机：模型决定调用某个工具之后、真正执行之前，即：模型要调用search_tool → 先跑wrap_tool_call → 再真正执行函数\
  wrap_tool_call是必需的，因为Agent需要知道工具对应的具体执行函数，否则工具无法运行

适用场景：
- 工具从MCP服务器等外部服务动态发现\
  无需本地预定义全部工具，Agent运行时主动连接MCP服务，实时拉取服务端托管的工具清单、调用规则，按需加载使用
- 工具根据用户配置动态生成\
  Agent创建时工具不注册，而是在运行时动态注册的
- 统一工具注册中心，支持多团队共享管理\
  企业内各团队均有独立agent，若无统一注册表，各团队需单独开发、注册工具，运维管理繁琐\
  搭建外部统一工具中心，集中维护工具清单与接口地址，各团队可从中取用工具，借助钩子函数挂载至自身代理使用\
  工具执行优先调用中心接口地址，无接口时则本地实现对应函数逻辑


## 示例
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


# 两种方式比较

| 项目           | 动态筛选预注册工具   | 运行时动态注册新工具             |
|:---------------:|:---------------------:|:---------------------------------:|
| 工具来源       | 本地预先全部注册     | 运行时从外部 / 配置添加          |
| 启动时状态     | 全量加载             | 极少 / 无                        |
| 运行时动作     | 过滤、隐藏           | 新增、注册、绑定                 |
| 必须钩子       | wrap_model_call      | wrap_model_call + wrap_tool_call |
| 能否用远程工具 | 不能                 | 能（MCP/API）                    |
| 内存占用       | 高                   | 低（按需加载）                   |
| 复杂度         | 低                   | 中                               |
| 企业规模       | 小 / 中              | 中 / 大                          |

