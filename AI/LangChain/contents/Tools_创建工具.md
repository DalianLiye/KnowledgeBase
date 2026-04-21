[目录](../目录.md)


# 基础工具定义
创建工具最简单的方式是使用@tool装饰器\
默认情况下，函数的文档字符串会成为工具的描述，帮助模型理解何时使用该工具

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"
```

类型注解是必需的，因为它们定义了工具的输入模式（schema）\
文档字符串应信息丰富且简洁，以帮助模型理解工具的用途

服务端工具使用：部分聊天模型内置了工具（如网络搜索、代码解释器），这些工具在服务端执行

工具名称推荐使用snake_case格式（例如，使用web_search而非Web Search）\
部分模型提供商会对包含空格或特殊字符的名称报错或拒绝使用\
仅使用字母数字、下划线和连字符有助于提升在不同模型提供商间的兼容性


# 自定义工具属性
默认情况下，工具的名称取自函数名\
当需要更具描述性的名称时，可以覆盖它

**自定义工具名**
```python
@tool("web_search")  # Custom name
def search(query: str) -> str:
    """Search the web for information."""
    return f"Results for: {query}"

print(search.name)  # web_search
```

**自定义工具描述**\
覆盖自动生成的工具描述，以便为模型提供更清晰的使用指引
```python
@tool("calculator", description="Performs arithmetic calculations. Use this for any math problems.")
def calc(expression: str) -> str:
    """Evaluate mathematical expressions."""
    return str(eval(expression))
```

# 高级 Schema 定义
使用Pydantic模型或JSON Schema来定义复杂的输入参数

示例：Pydantic model
```python
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
    """Input for weather queries."""
    location: str = Field(description="City name or coordinates")
    units: Literal["celsius", "fahrenheit"] = Field(
        default="celsius",
        description="Temperature unit preference"
    )
    include_forecast: bool = Field(
        default=False,
        description="Include 5-day forecast"
    )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

示例：JSON Schema
```python
weather_schema = {
    "type": "object",
    "properties": {
        "location": {"type": "string"},
        "units": {"type": "string"},
        "include_forecast": {"type": "boolean"}
    },
    "required": ["location", "units", "include_forecast"]
}

@tool(args_schema=weather_schema)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
    """Get current weather and optional forecast."""
    temp = 22 if units == "celsius" else 72
    result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
    if include_forecast:
        result += "\nNext 5 days: Sunny"
    return result
```

# 保留参数名
以下参数名称是系统保留的，不能用作工具的自定义参数\
使用这些名称会导致运行时错误

保留参数：
- **config**\
  保留用于在内部向工具传递RunnableConfig
- **runtime**\
  保留用于ToolRuntime参数（用于访问状态、上下文、存储）

如果需要访问运行时信息，请直接使用ToolRuntime参数，而不要将自定义参数命名为config或runtime