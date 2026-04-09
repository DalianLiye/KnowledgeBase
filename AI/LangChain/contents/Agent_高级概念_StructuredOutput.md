[目录](../目录.md)


# 关于Structured Output
LangChain支持通过response_format参数，强制模型按指定格式返回结构化数据

提供两种策略：
- ToolStrategy
- ProviderStrategy


# ToolStrategy
通过模拟工具调用（tool call）实现结构化输出\
模型并非真实调用工具，而是遵循工具调用协议输出规范格式\
所有支持tool calling的模型均可使用，适合厂商原生结构化输出不可用或不稳定的场景

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
直接使用模型厂商原生结构化输出能力，格式更标准、稳定性更高，但仅当提供商原生支持时可用

**自动降级规则（LangChain 1.0+）**\
response_format直接传入schema时，默认使用ProviderStrategy\
若厂商不支持原生结构化输出，框架自动降级为ToolStrategy

示例：
```python
from langchain.agents.structured_output import ProviderStrategy

agent = create_agent(
    model="gpt-4.1",
    response_format=ProviderStrategy(ContactInfo)
)
```