[目录](../目录.md)


# 关于Dynamic Model
Dynamic model是agent可根据运行时状态、上下文自动选择模型，实现智能路由与成本优化
实现Dynamic model必须使用middleware，并通过@wrap_model_call装饰器完成模型路由逻辑


# 示例

示例:
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

# 关于pre-bound和structured output的冲突

- **pre-bound model**\
  pre-bound model指预先通过bind_tools()绑定了工具的模型\
  示例：
  ```python
  llm = ChatOpenAI(...)
  llm_with_tools = llm.bind_tools([tool1, tool2])
  ```

- **structured output**\
  structured output指通过 with_structured_output()让模型按指定格式返回结果\
  示例：
  ```python
  from typing import TypedDict

  class UserInfo(TypedDict):
      name: str
      age: int

  structured_llm = llm.with_structured_output(UserInfo)
  result: UserInfo = structured_llm.invoke("请提取名字和年龄：张三，27岁")
  ```

Pre-bound models是不被支持使用structure output功能的\
Tool和structure output都会对输出格式做约束和解析，会导致冲突，所以干脆禁止两个机制同时存在\
因此，在dynamic model做动态选择model时，如果所选择的model同时指定了pre-bound和structure output的定义，就会报错
