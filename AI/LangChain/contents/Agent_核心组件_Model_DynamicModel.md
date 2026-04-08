Dynamic model就是agent可以根据运行时，当前状态，以及上下文自动选择model\
Dynamic model可以实现复杂的路由逻辑和节省成本

实现Dynamic model，需要通过middleware的内部逻辑实现\
该middleware要配置@wrap_model_call装饰器

示例:
```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse


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

agent = create_agent(
    model=basic_model,  # Default model
    tools=tools,
    middleware=[dynamic_model_selection]
)
```

- pre-bound model\
  一个model在定义时，如果预先绑定了tool，就是pre-bound model
  ```python
  llm = ChatOpenAI(...)
  llm_with_tools = llm.bind_tools([tool1, tool2])
  ```

- structured output\
  一个model定义时，也可以绑定structured output，这样model返回结果时，就会按照指定格式返回结果
  ```python
  from typing import TypedDict

  class UserInfo(TypedDict):
      name: str
      age: int

  structured_llm = llm.with_structured_output(UserInfo)
  result: UserInfo = structured_llm.invoke("请提取名字和年龄：张三，27岁")
  ```

Pre-bound models是不被支持使用structure output功能的\
因为，Tool和structure output都会对输出格式做约束和解析，这样就冲突了，所以干脆禁止两个机制同时存在\
因此，在dynamic model做动态选择model时，如果所选择的model同时pre-bound和structure output的定义，就会报错