Static tool就是创建Agent时指定tool后，tool在agent整个生命周期内都不会改变\
Static tool是最普遍，最直接的一种指定tool的方式\
创建agent时，指定一个Tool函数列表[Tool1, Tool2,...], 如果列表为空，以为这agent仅仅是绑定了LLM，没有tool calling能力

Tool既可以是普通的python函数，也可以是python coroutines
```python
from langchain.tools import tool
from langchain.agents import create_agent


@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])
```

当用@Tool装饰一个函数时，不只是简单地把它标记为“工具”，还可以在装饰器里顺带配置这个工具的名字、描述、参数结构等信息，方便 LLM 更好地理解、选择、和调用这个工具
```python
from typing import TypedDict
from langchain.tools import tool

class WeatherInput(TypedDict):
    city: str
    unit: str

@tool(name="weather_lookup", args_schema=WeatherInput, description="查询指定城市的当前天气信息")
def weather_tool(city: str, unit: str = "celsius") -> str:
    # city, unit 的定义来自 args_schema
    return f"{city} 当前天气：26°C，单位为 {unit}"
```

@tool装饰器这些属性字段是装饰器里预置的
- name\
  函数名叫 get_weather，但对 LLM 暴露的工具名是 "weather_lookup"，也就是说，模型在“tool calls”协议里，会看到 weather_lookup 这个名字，而不是 get_weather

- description\
  提供了一句中文描述：查询指定城市的当前天气信息\
  LLM 会根据描述，决定何时调用这个工具（这对工具路由很重要）

- args_schema
  参数 schema 按定义的 TypedDict 来，可以精确控制传入参数的字段名、类型等



这些描述信息也可以加载system prompt里，但写在装饰器里会有强约束力，更加稳定，因为它是langchain框架支持的\
而写在system prompt里，其实是用来LLM的分析理解能力，约束力不强，不会特别稳定