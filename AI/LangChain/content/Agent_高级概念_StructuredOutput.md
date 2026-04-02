# 关于Structured output
LangChain提供了一个策略，可以让model按照指定格式返回内容\
通过response_format参数实现

structure output有以下两种方式：
- ToolStrategy
- ProviderStrategy


# ToolStrategy
ToolStrategy是一种通过“模拟调用工具”的方式来让model生成结构化输出的方法\
它把model的输出组织成调用某个预定义工具（或工具接口）的形式，从而得到可解析的、结构化的数据（比如 JSON 或特定字段的映射）\
任何支持tool calling的model都可以使用ToolStrategy的方式\
当model provider原生支持结构化输出不可用或不可靠时，就应该使用ToolStrategy

示例：
```python
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy


class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-4.1-mini",
    tools=[search_tool],
    response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```


# ProviderStrategy
ProviderStragety 使用model provider原生的结构化输出能力\
它更可靠，但只有provider支持原生结构化输出时才可用

示例：
```python
from langchain.agents.structured_output import ProviderStrategy

agent = create_agent(
    model="gpt-4.1",
    response_format=ProviderStrategy(ContactInfo)
)
```

从langchain 1.0开始，如果 response_format直接设置为schema，则默认使用ProviderStrategy的方式\
如果provider原生不支持，则会按照ToolStrategy的方式