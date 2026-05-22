[目录](../目录.md)


# 关于动态选择模型
动态选择模型是Agent可根据运行时状态、上下文自动选择模型，实现智能路由与成本优化\
实现动态选择模型必须使用中间件，并通过@wrap_model_call装饰器完成模型路由逻辑


# 示例

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from dotenv import load_dotenv  
load_dotenv() 

basic_model = ChatOpenAI(model="gpt-4.1-mini")
advanced_model = ChatOpenAI(model="gpt-4.1")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    """Choose model based on conversation complexity."""
    message_count = len(request.state["messages"])

    if message_count > 10:
        # Use an advanced model for longer conversations
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))

tools=[]

agent = create_agent(
    model=basic_model,  # Default model
    tools=tools,
    middleware=[dynamic_model_selection]
)
```

# 关于预绑定工具的模型和结构化输出的冲突

- **预绑定工具的模型**\
  预绑定工具的模型指预先通过bind_tools()预先绑定了工具的模型实例\
  示例：
  ```python
  llm = ChatOpenAI(...)
  llm_with_tools = llm.bind_tools([tool1, tool2])
  ```

- **结构化输出**\
  结构化输出指通过with_structured_output()让模型按指定格式返回结果\
  示例：
  ```python
  from typing import TypedDict

  class UserInfo(TypedDict):
      name: str
      age: int

  structured_llm = llm.with_structured_output(UserInfo)
  result: UserInfo = structured_llm.invoke("请提取名字和年龄：张三，27岁")
  ```

已经通过bind_tools()预绑定工具的模型，不支持再使用结构化输出功能\
工具调用和结构化输出都会强制约束模型的输出格式与解析逻辑\
底层（尤其是 OpenAI 格式）无法同时兼容两种格式约束，会产生解析冲突\
因此框架会禁止这两个机制同时作用于同一个模型\
动态选择模型时，如果模型同时指定了预绑定工具和结构化输出，框架会直接抛出错误