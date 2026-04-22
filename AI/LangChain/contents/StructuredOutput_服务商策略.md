[目录](../目录.md)



# 服务商策略
部分模型服务商（如 OpenAI、xAI (Grok)、Gemini、Anthropic (Claude)）的 API 原生支持结构化输出。在可用的情况下，这是最可靠的方法

要使用此策略，请配置 ProviderStrategy：
```python
class ProviderStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    strict: bool | None = None
```

提示：strict 参数需要 langchain>=1.2

schema (必填参数)
用于定义结构化输出格式的 Schema，支持以下几种类型：
- Pydantic 模型：继承自 BaseModel 的子类，自带字段校验，返回经过验证的 Pydantic 实例。
- 数据类 (Dataclasses)：带类型注解的 Python 数据类，返回字典。
- TypedDict：类型化字典类，返回字典。
- JSON Schema：符合 JSON Schema 规范的字典，返回字典。

strict (可选参数)
用于开启 “严格模式” 的布尔参数，部分服务商支持（如 OpenAI 和 xAI），默认值为 None（即关闭）。开启后，模型会被强制严格遵守 Schema，不允许额外字段或格式错误

当你直接将一个 Schema 类型传给 create_agent.response_format，并且模型支持原生结构化输出时，LangChain 会自动使用 ProviderStrategy

Pydantic Model
```python
from pydantic import BaseModel, Field
from langchain.agents import create_agent


class ContactInfo(BaseModel):
    """Contact information for a person."""
    name: str = Field(description="The name of the person")
    email: str = Field(description="The email address of the person")
    phone: str = Field(description="The phone number of the person")

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

print(result["structured_response"])
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')
```

Dataclass
```python
from dataclasses import dataclass
from langchain.agents import create_agent


@dataclass
class ContactInfo:
    """Contact information for a person."""
    name: str # The name of the person
    email: str # The email address of the person
    phone: str # The phone number of the person

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```


TypedDict
```python
from typing_extensions import TypedDict
from langchain.agents import create_agent


class ContactInfo(TypedDict):
    """Contact information for a person."""
    name: str # The name of the person
    email: str # The email address of the person
    phone: str # The phone number of the person

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ContactInfo  # Auto-selects ProviderStrategy
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```

JSON Schema
```python
from langchain.agents import create_agent


contact_info_schema = {
    "type": "object",
    "description": "Contact information for a person.",
    "properties": {
        "name": {"type": "string", "description": "The name of the person"},
        "email": {"type": "string", "description": "The email address of the person"},
        "phone": {"type": "string", "description": "The phone number of the person"}
    },
    "required": ["name", "email", "phone"]
}

agent = create_agent(
    model="gpt-5",
    tools=tools,
    response_format=ProviderStrategy(contact_info_schema)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# {'name': 'John Doe', 'email': 'john@example.com', 'phone': '(555) 123-4567'}
```

服务商原生结构化输出提供了高可靠性和严格验证，因为模型服务商本身会强制遵循 Schema。在可用的情况下，应优先使用它。

如果你的模型选择支持服务商原生结构化输出，那么直接写 response_format=ProductReview 和写 response_format=ProviderStrategy(ProductReview) 在功能上是等效的。
无论哪种方式，如果结构化输出不被支持，agent 都会自动降级为工具调用策略

