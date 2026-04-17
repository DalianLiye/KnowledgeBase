[目录](../目录.md)


# 关于可配置模型

可配置模型(Configurable models)是LangChain提供的一种运行时动态切换模型的能力\
初始化时可以不固定model和model_provider，而是在每次调用invoke() 时通过config参数动态指定\
这样就可以用同一个模型实例，根据场景选择不同的底层模型

示例：
```python
from langchain.chat_models import init_chat_model

configurable_model = init_chat_model(temperature=0)

configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "gpt-5-nano"}},  # Run with GPT-5-Nano
)
configurable_model.invoke(
    "what's your name",
    config={"configurable": {"model": "claude-sonnet-4-6"}},  # Run with Claude
)
```

**典型应用场景：**
- **多模型路由**\
  根据用户请求类型、成本预算、性能需求，动态选择不同模型
- **A/B测试**\
  在不修改代码的情况下，对比不同模型的效果。
- **复杂业务流**\
  根据上下文自动切换成本高 / 低、能力强 / 弱的模型


**关于configurable_fields参数**\
configurable_fields表示哪些模型参数，允许在调用的时候动态修改

如果初始化时不指定configurable_fields，模型实例一旦创建，参数就固定不可修改
```python
model = init_chat_model(model="gpt-4o", temperature=0.5)
```

如果初始化时指定configurable_fields，指定的参数可在运行时动态配置\
示例：
```python
model = init_chat_model(
    model="gpt-4o",
    temperature=0.5,
    configurable_fields=["temperature"]  # 我指定这个字段可以运行时修改！
)

model.invoke("你好", config={"configurable": {"temperature": 1}})
model.invoke("你好", config={"configurable": {"temperature": 0}})
```

如果初始化时不指定model和model_provider，LangChain会自动将这两个参数加入configurable_fields\
示例：
```python
configurable_model = init_chat_model(temperature=0)

# 等价于
configurable_model = init_chat_model(
    temperature=0
    configurable_fields=["model","model_provider"]
)
```


# 示例

- **带默认值的可配置模型**
  可以创建带默认值的可配置模型，指定可配置参数，并为可配置参数添加前缀（避免多模型冲突）
  ```python
  first_model = init_chat_model(
          model="gpt-4.1-mini",
          temperature=0,
          configurable_fields=("model", "model_provider", "temperature", "max_tokens"),
          config_prefix="first",  # Useful when you have a chain with multiple models
  )

  first_model.invoke("what's your name")

  first_model.invoke(
      "what's your name",
      config={
          "configurable": {
              "first_model": "claude-sonnet-4-6",
              "first_temperature": 0.5,
              "first_max_tokens": 100,
          }
      },
  )
  ```

  config_prefix用于给可配置参数添加自定义前缀，当一条链中存在多个可配置模型时，避免参数名称冲突，确保每个模型能正确获取自己的运行配置
  ```python
  from langchain.chat_models import init_chat_model

  # ======================
  # 模型1：前缀 = first
  # ======================
  model1 = init_chat_model(
      model="gpt-4.1-mini",        # 默认模型
      temperature=0,               # 默认温度
      configurable_fields=["model", "temperature"],
      config_prefix="first"        # 给参数加前缀：first_
  )

  # ======================
  # 模型2：前缀 = second
  # ======================
  model2 = init_chat_model(
      model="claude-haiku-4-5",    # 默认模型
      temperature=0,               # 默认温度
      configurable_fields=["model", "temperature"],
      config_prefix="second"       # 给参数加前缀：second_
  )

  # ======================
  # 关键：同时给两个模型传不同配置
  # 不会冲突！因为前缀不同
  # ======================
  config = {
      "configurable": {
          # 给 model1 的参数（带 first_）
          "first_model": "gpt-4.1",
          "first_temperature": 0.8,

          # 给 model2 的参数（带 second_）
          "second_model": "claude-sonnet-4-6",
          "second_temperature": 0.1
      }
  }

  # 各自调用，各自拿到自己的配置，互不干扰
  resp1 = model1.invoke("Hello", config=config)
  resp2 = model2.invoke("Hello", config=config)

  print("model1 使用的模型:", resp1.response_metadata['model_name'])
  print("model2 使用的模型:", resp2.response_metadata['model_name'])
  ```
  结果：
  ```python
  model1 使用的模型: gpt-4.1
  model2 使用的模型: claude-sonnet-4-6
  ```

- **声明式地使用可配置模型**\
  可以在可配置模型上调用bind_tools、with_structured_output、with_configurable等声明式操作\
  并像使用普通聊天模型一样，对可配置模型进行链式调用
  ```python
  from pydantic import BaseModel, Field


  class GetWeather(BaseModel):
      """Get the current weather in a given location"""

          location: str = Field(description="The city and state, e.g. San Francisco, CA")


  class GetPopulation(BaseModel):
      """Get the current population in a given location"""

          location: str = Field(description="The city and state, e.g. San Francisco, CA")


  model = init_chat_model(temperature=0)
  model_with_tools = model.bind_tools([GetWeather, GetPopulation])

  model_with_tools.invoke(
      "what's bigger in 2024 LA or NYC", config={"configurable": {"model": "gpt-4.1-mini"}}
  ).tool_calls
  ```
  
  返回结果
  ```json
  [
      {
          'name': 'GetPopulation',
          'args': {'location': 'Los Angeles, CA'},
          'id': 'call_Ga9m8FAArIyEjItHmztPYA22',
          'type': 'tool_call'
      },
      {
          'name': 'GetPopulation',
          'args': {'location': 'New York, NY'},
          'id': 'call_jh2dEvBaAHRaw5JUDthOs7rt',
          'type': 'tool_call'
      }
  ]
  ```
  
  切换模型再次调用
  ```python
  model_with_tools.invoke(
      "what's bigger in 2024 LA or NYC",
      config={"configurable": {"model": "claude-sonnet-4-6"}},
  ).tool_calls
  ```

  返回结果
  ```json
  [
      {
          'name': 'GetPopulation',
          'args': {'location': 'Los Angeles, CA'},
          'id': 'toolu_01JMufPf4F4t2zLj7miFeqXp',
          'type': 'tool_call'
      },
      {
          'name': 'GetPopulation',
          'args': {'location': 'New York City, NY'},
          'id': 'toolu_01RQBHcE8kEEbYTuuS8WqY1u',
          'type': 'tool_call'
      }
  ]
  ```