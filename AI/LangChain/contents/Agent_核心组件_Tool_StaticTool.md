[目录](../目录.md)


# 关于Static Tool
Static tool指Agent创建时指定工具列表，生命周期内固定不变，是最常用的工具配置方式\
传入工具列表为空时，Agent仅绑定LLM，不具备工具调用能力\
Tool支持普通Python函数与协程（coroutines）

# 示例

示例1：绑定工具
示例1：
```python
from langchain.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv  
load_dotenv()  

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent("openai:gpt-5", tools=[search, get_weather])
```

示例2：添加工具元数据
当用@Tool装饰一个函数时，不只是简单地把它标记为“工具”，还可以在装饰器里顺带配置这个工具的名字、描述、参数结构等信息，方便model更好地理解、选择、和调用这个工具
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
- **name**\
  函数名叫get_weather，但对model暴露的工具名是"weather_lookup"\
  即模型在“tool calls”协议里，会看到weather_lookup这个名字，而不是 get_weather

- **description**\
  提供了一句中文描述：查询指定城市的当前天气信息\
  model会根据描述，决定何时调用这个工具（这对工具路由很重要）

- **args_schema**\
  参数 schema 按定义的\
  args_schema 用于定义工具的输入参数结构，支持Pydantic model或TypedDict\
  脚本里是TypedDict，可以精确控制传入参数的字段名、类型等

注：\
这些属性信息也可以加载system prompt里，但写在装饰器里会有强约束力，更加稳定，因为它是langchain框架支持的\
而写在system prompt里，其实是用来model的分析理解能力，约束力不强，不会特别稳定