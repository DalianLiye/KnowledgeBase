[目录](../目录.md)


# 服务商策略
部分主流大模型厂商（OpenAI、xAI Grok、Gemini、Anthropic Claude）的接口原生支持结构化输出，该方式稳定性与准确性最优，优先推荐使用

如需启用该策略，直接配置ProviderStrategy即可
```python
class ProviderStrategy(Generic[SchemaT]):
    schema: type[SchemaT]
    strict: bool | None = None
```
注：strict参数需要langchain>=1.2

- **schema(必填参数)**
  定义结构化输出的数据格式规范，支持四种常用写法，返回格式各有区别
  - **Pydantic模型**\
    继承BaseModel定义，自带字段合法性校验，最终返回Pydantic实体对象
  - **数据类 (Dataclasses)**\
    Python原生带类型注解的数据类，最终返回标准字典
  - **TypedDict**\
    轻量化类型约束字典，最终返回标准字典
  - **JSON Schema**\
    遵循JSON规范的字典格式，通用性最强，最终返回标准字典

- **strict(可选参数)**
  布尔类型参数，仅部分厂商模型支持（OpenAI、xAI 等），默认None代表关闭\
  开启严格模式后，模型必须完全遵循定义的Schema，禁止输出多余字段、禁止格式错乱\
  当直接将Schema类型赋值给create_agent的response_format参数，且所用模型支持原生结构化输出时，LangChain会自动匹配启用ProviderStrategy

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

  **策略总结**\
  1) 服务商原生结构化输出由模型接口底层强制约束格式，校验严谨、稳定性高，有条件优先使用\
  2) 模型支持原生结构化输出时，response_format=自定义Schema 与 response_format=ProviderStrategy(Schema) 两种写法功能完全一致\
  3) 若当前模型不支持原生结构化输出，框架会自动降级，切换为工具调用策略完成结构化输出  