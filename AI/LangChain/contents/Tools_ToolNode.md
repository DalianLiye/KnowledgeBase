[目录](../目录.md)


# 关于ToolNode
ToolNode是LangGraph工作流中用于执行工具的预构建节点\
它自动处理工具的并行执行、错误处理和状态注入\
如果需要对工具执行模式进行细粒度控制的自定义工作流，请使用ToolNode而非create_agent,它是驱动Agent工具执行的基础构建块


# 基本使用
```python
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

# Create the ToolNode with your tools
tool_node = ToolNode([search, calculator])

# Use in a graph
builder = StateGraph(MessagesState)
builder.add_node("tools", tool_node)
# ... add other nodes and edges
```


# 工具返回值
工具可以返回以下值类型：
- **string（字符串）**\
  用于人类可读的结果
- **object（对象）**\
  用于需要模型解析的结构化结果
- **Command**\
  当需要写入/更新状态时，可附带可选消息


**返回字符串**\
当工具需要提供纯文本，供模型读取并在后续回复中使用时，返回字符串

```python
from langchain.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"It is currently sunny in {city}."
```

Behavior（行为）:
- 返回值会被自动转换为ToolMessage
- 模型会读取这段文本，并决定下一步操作
- 不会修改Agent状态，除非后续由模型或其他工具进行修改

当结果本身就是人类可读的文本时，使用这种方式



**返回对象**\
当工具生成模型需要解析的结构化数据时，返回一个对象（例如字典 dict）

```python
from langchain.tools import tool


@tool
def get_weather_data(city: str) -> dict:
    """Get structured weather data for a city."""
    return {
        "city": city,
        "temperature_c": 22,
        "conditions": "sunny",
    }
```

Behavior（行为）:
- 对象会被序列化，并作为工具输出返回
- 模型可以读取特定字段，并基于这些字段进行推理
- 和字符串返回值一样，不会直接更新图状态

当下游推理更依赖明确的字段而非自由格式文本时，使用这种方式



**返回Command**\
当工具需要更新图状态时（例如设置用户偏好或应用状态），返回 Command\
可以返回包含或不包含ToolMessage的Command\
如果模型需要看到工具执行成功（例如确认偏好更改），请在更新中包含ToolMessage，并使用runtime.tool_call_id作为tool_call_id参数

```python
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command


@tool
def set_language(language: str, runtime: ToolRuntime) -> Command:
    """Set the preferred response language."""
    return Command(
        update={
            "preferred_language": language,
            "messages": [
                ToolMessage(
                    content=f"Language set to {language}.",
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
```

Behavior（行为）:
- Command通过update参数更新状态
- 更新后的状态在本次运行的后续步骤中可用
- 对于可能被并行工具调用更新的字段，需要使用reducer

当工具不只是返回数据，还需要修改Agent状态时，使用这种方式


# 错误处理
配置工具错误的处理方式\
所有选项请参考ToolNode API文档
```python
from langgraph.prebuilt import ToolNode

# Default: catch invocation errors, re-raise execution errors
tool_node = ToolNode(tools)

# Catch all errors and return error message to LLM
tool_node = ToolNode(tools, handle_tool_errors=True)

# Custom error message
tool_node = ToolNode(tools, handle_tool_errors="Something went wrong, please try again.")

# Custom error handler
def handle_error(e: ValueError) -> str:
    return f"Invalid input: {e}"

tool_node = ToolNode(tools, handle_tool_errors=handle_error)

# Only catch specific exception types
tool_node = ToolNode(tools, handle_tool_errors=(ValueError, TypeError))
```

# 使用tools_condition进行路由
使用tools_condition进行条件路由，基于大模型是否发起了工具调用
```python
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END

builder = StateGraph(MessagesState)
builder.add_node("llm", call_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", tools_condition)  # Routes to "tools" or END
builder.add_edge("tools", "llm")

graph = builder.compile()
```



# 状态注入
工具可以通过ToolRuntime访问当前的图状态
```python
from langchain.tools import tool, ToolRuntime
from langgraph.prebuilt import ToolNode

@tool
def get_message_count(runtime: ToolRuntime) -> str:
    """Get the number of messages in the conversation."""
    messages = runtime.state["messages"]
    return f"There are {len(messages)} messages."

tool_node = ToolNode([get_message_count])
```
关于从工具中访问状态、上下文和长期记忆的更多细节，请参考 “Access context” 相关文档