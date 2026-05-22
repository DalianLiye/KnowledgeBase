[目录](../目录.md)


# 关于静态工具
创建Agent时指定全部工具列表，工具列表在整个生命周期内不变\
静态工具是最常用的工具配置方式\
当不指定工具列表或工具列表设置为空(Tools=[])时，意味着Agent仅绑定了模型，不具备工具调用能力


# 示例

- 示例1：绑定工具
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

- 示例2：添加工具元数据
  当用@Tool装饰一个函数时，Agent会做以下操作：
  - 将该函数标记为“工具”
  - 装饰器里可以顺带配置该工具的名字、描述、参数结构等信息，方便模型更好地理解、选择、和调用这个工具
    
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

  说明:
  - @tool装饰器以下字段是预置的
    - **name**\
      虽然函数名叫weather_tool，但其实暴露给模型的工具名是"weather_lookup"\
      即模型在“tool calls”协议里，会看到weather_lookup这个名字，而不是weather_tool

    - **description**\
      提供了一句中文描述：查询指定城市的当前天气信息\
      模型会根据描述，决定何时调用这个工具（这对工具路由很重要）

    - **args_schema**\
      args_schema用于定义工具的输入参数结构，支持Pydantic model或TypedDict\
      示例里是TypedDict，可以精确控制传入参数的字段名、类型等

  - 这些属性信息也可以定义在提示词里，但定义在装饰器里约束力更强，更稳定，因为它是langchain框架支持的\
    写在提示词里，靠的是模型的分析理解能力，约束力不强也，不会特别稳定