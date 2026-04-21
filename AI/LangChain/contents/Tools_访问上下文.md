[目录](../目录.md)


# 关于访问上下文
当工具能够访问对话历史、用户数据和持久化存储等运行时信息时，它们的能力将达到最强\

工具可以通过ToolRuntime参数访问运行时信息，该参数提供以下能力:
- **State**\
  短期记忆 - 仅在当前对话中存在的可变数据（消息、计数器、自定义字段）\	
  访问对话历史、跟踪工具调用次数
- **Context**\
  调用时传入的不可变配置（用户 ID、会话信息）\
  根据用户身份个性化响应
- **Store**\
  长期记忆 - 跨对话持久化的数据\
  保存用户偏好、维护知识库
- **Stream Writer**\
  工具执行过程中发送实时更新\	
  展示长时间运行操作的进度
- **Execution Info**\
  当前执行的身份与重试信息（线程 ID、运行 ID、尝试次数\	
  访问线程 / 运行 ID、根据重试状态调整行为
- **Server Info**\
  在LangGraph Server上运行时的服务端元数据（助手 ID、图 ID、已认证用户）\	
  访问助手 ID、图 ID或已认证用户信息
- **Config**\
  本次执行的 RunnableConfig\
  访问回调、标签和元数据
- **Tool Call ID**\
  当前工具调用的唯一标识符\
  关联日志和模型调用中的工具调用


# 短期记忆（State）
State代表仅在单次对话期间存在的短期记忆，它包含消息历史记录，以及你在图状态中定义的任何自定义字段

在工具的函数签名中添加runtime: ToolRuntime参数，即可访问state
该参数会被自动注入，并且对大模型是隐藏的 —— 它不会出现在工具的schema中

**访问状态**\
工具可以通过runtime.state访问当前对话状态
```python
from langchain.tools import tool, ToolRuntime
from langchain.messages import HumanMessage

@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    """Get the most recent message from the user."""
    messages = runtime.state["messages"]

    # Find the last human message
    for message in reversed(messages):
        if isinstance(message, HumanMessage):
            return message.content

    return "No user messages found"

# Access custom state fields
@tool
def get_user_preference(
    pref_name: str,
    runtime: ToolRuntime
) -> str:
    """Get a user preference value."""
    preferences = runtime.state.get("user_preferences", {})
    return preferences.get(pref_name, "Not set")
```
runtime参数对模型是隐藏的
在上面的例子中，模型在工具schema中只能看到pref_name这一个参数


**更新状态**\
使用Command来更新Agent的状态
这对于需要更新自定义状态字段的工具非常有用
在更新中包含一个ToolMessage，以便模型可以看到工具调用的结果

```python
from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


class CustomState(AgentState):
    user_name: str


@tool
def set_user_name(new_name: str, runtime: ToolRuntime[None, CustomState]) -> Command:
    """Set the user's name in the conversation state."""
    return Command(
        update={
            "user_name": new_name,
            "messages": [
                ToolMessage(
                    content=f"User name set to {new_name}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```
当工具更新状态变量时，建议为这些字段定义一个reducer（归约器）
由于大模型可以并行调用多个工具，reducer用于解决同一状态字段被并发工具调用更新时的冲突


# 上下文
Context提供在调用时传入的不可变配置数据
它适用于用户ID、会话详情或在对话过程中不应更改的应用特定设置

通过runtime.context访问上下文
```python
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime


USER_DATABASE = {
    "user123": {
        "name": "Alice Johnson",
        "account_type": "Premium",
        "balance": 5000,
        "email": "alice@example.com"
    },
    "user456": {
        "name": "Bob Smith",
        "account_type": "Standard",
        "balance": 1200,
        "email": "bob@example.com"
    }
}

@dataclass
class UserContext:
    user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
    """Get the current user's account information."""
    user_id = runtime.context.user_id

    if user_id in USER_DATABASE:
        user = USER_DATABASE[user_id]
        return f"Account holder: {user['name']}\nType: {user['account_type']}\nBalance: ${user['balance']}"
    return "User not found"

model = ChatOpenAI(model="gpt-5.4")
agent = create_agent(
    model,
    tools=[get_account_info],
    context_schema=UserContext,
    system_prompt="You are a financial assistant."
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's my current balance?"}]},
    context=UserContext(user_id="user123")
)
```


# 长期记忆（Store）
BaseStore提供跨对话持久化的存储\
与State（短期记忆）不同，保存在Store中的数据在未来会话中依然可用

通过runtime.store访问Store\
Store使用namespace/key模式来组织数据

在生产环境部署时，请使用PostgresStore等持久化存储实现，而非InMemoryStore

```python
from typing import Any
from langgraph.store.memory import InMemoryStore
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime
from langchain_openai import ChatOpenAI

# Access memory
@tool
def get_user_info(user_id: str, runtime: ToolRuntime) -> str:
    """Look up user info."""
    store = runtime.store
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"

# Update memory
@tool
def save_user_info(user_id: str, user_info: dict[str, Any], runtime: ToolRuntime) -> str:
    """Save user info."""
    store = runtime.store
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."

model = ChatOpenAI(model="gpt-5.4")

store = InMemoryStore()
agent = create_agent(
    model,
    tools=[get_user_info, save_user_info],
    store=store
)

# First session: save user info
agent.invoke({
    "messages": [{"role": "user", "content": "Save the following user: userid: abc123, name: Foo, age: 25, email: foo@langchain.dev"}]
})

# Second session: get user info
agent.invoke({
    "messages": [{"role": "user", "content": "Get user info for user with id 'abc123'"}]
})
# Here is the user info for user with ID "abc123":
# - Name: Foo
# - Age: 25
# - Email: foo@langchain.dev
```


# Stream writer
在工具执行过程中发送实时更新\
这对于在长时间运行的操作中向用户提供进度反馈非常有用\
使用runtime.stream_writer发送自定义更新

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_weather(city: str, runtime: ToolRuntime) -> str:
    """Get weather for a given city."""
    writer = runtime.stream_writer

    # Stream custom updates as the tool executes
    writer(f"Looking up data for city: {city}")
    writer(f"Acquired data for city: {city}")

    return f"It's always sunny in {city}!"
```

如果在工具中使用runtime.stream_writer，该工具必须在LangGraph的执行上下文中被调用


# Execution info
在工具中通过runtime.execution_info访问线程ID、运行ID和重试状态

```python
from langchain.tools import tool, ToolRuntime

@tool
def log_execution_context(runtime: ToolRuntime) -> str:
    """Log execution identity information."""
    info = runtime.execution_info
    print(f"Thread: {info.thread_id}, Run: {info.run_id}")
    print(f"Attempt: {info.node_attempt}")
    return "done"
```
该功能需要 deepagents>=0.5.0 或 langgraph>=1.1.5 以上版本才能使用


# Server info
当工具在LangGraph Server上运行时，可以通过runtime.server_info访问助手ID、图ID和已认证用户信息

```python
from langchain.tools import tool, ToolRuntime

@tool
def get_assistant_scoped_data(runtime: ToolRuntime) -> str:
    """Fetch data scoped to the current assistant."""
    server = runtime.server_info
    if server is not None:
        print(f"Assistant: {server.assistant_id}, Graph: {server.graph_id}")
        if server.user is not None:
            print(f"User: {server.user.identity}")
    return "done"
```

当工具未在LangGraph Server上运行时（例如在本地开发或测试中），server_info为None
注意：需要 deepagents>=0.5.0（或 langgraph>=1.1.5）版本