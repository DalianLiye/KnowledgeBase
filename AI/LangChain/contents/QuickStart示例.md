[目录](../目录.md)

# 示例
```python
from dataclasses import dataclass

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.structured_output import ToolStrategy
from dotenv import load_dotenv
load_dotenv()
import os


# Define system prompt
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location

If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""

# Define context schema
@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

# Define tools
@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"

# ========================
# DeepSeek 模型
# ========================
model = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com/v1",
    temperature=0
)

# Define response format
@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    punny_response: str
    weather_conditions: str | None = None

# Set up memory
checkpointer = InMemorySaver()

# Create agent
agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)

# Run agent
config = {"configurable": {"thread_id": "1"}}

response = agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather outside?"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])

# Continue conversation
response = agent.invoke(
    {"messages": [{"role": "user", "content": "thank you!"}]},
    config=config,
    context=Context(user_id="1")
)

print(response['structured_response'])
```

# 说明
代码里无需显式指定integration，后台会在指定model时自定分析匹配\
过程大致如下：
1) 框架内部有一个“模型路由/注册表”（registry）
2) 根据create_agent传入的model字符串名称参数，去匹配是哪个provider\
   比如，如果是gpt-5，则是OpenAI，如果是claude-sonnet-4-6，则是Anthropic\
   由于该例是直接传入的ChatOpenAI对象，因此后台自动匹配OpenAI
3) 内部会调用对应Provider的Integration包


示例涉及以下Agent核心部分：
- **System Prompt**\
  用来定义agent的角色和行为\
  它的描述一定要具体且可执行，比如针对Tool函数的相关描述


- **Tool**\
  Tool就是自定义的函数，可以让模型跟外部系统交互\
  在System prompt要对Tool函数进行详细描述，包括函数名，参数，以及何时调用，这样模型就可以更好的调用Tool函数了

  在Tool函数加装饰器@Tool后, 函数就可以接收参数 "runtime: ToolRuntime[自定义类型]"\
  函数体内，通过ToolRuntime[自定义类型]类型参数，获取一些meta和上下文信息，用于函数体内的逻辑实现\
  该示例中，自定义了一个类型Context，那么参数就可以写成runtime: ToolRuntime[Context]，然后runtime.context的返回值就是自定义类型Context的一个实例

  Tool函数的参数既可以是自定义的，也可以是使用ToolRuntime[Context]，也可以混合使用(ToolRuntime类型参数必须是第一个位置)\
  它们的区别在于，自定义参数的值，是模型分析了用户发送的提示词后得到的，然后传给函数的（经过模型）\
  ToolRuntime[自定义类型]类型参数无需经由LLM分析，是由LangChain运行时注入（没经过模型）

  函数体内，也可以跟agent Memory进行交互


- **Model**\
  通过Model设置模型参数\
  不同厂商的模型的配置参数也各不相同\
  示例使用ChatOpenAI创建DeepSeek模型，LangChain会通过OpenAI协议适配器调用模型\
  DeepSeek官方直接兼容OpenAI的API格式，所以不用装额外插件，直接用ChatOpenAI就能调用


- **Response Format**\
  可以对模型的返回值定义严格的format\
  比如format可以是一个字典对象，包含一些自定义的字段，然后让模型将输出按照这种事先定义好的format返回给agent


- **Memory**\
  可以在Model里为agent指定一个memory对象，用于记录和维护每次与模型对话的状态信息\
  InMemorySaver会在程序结束后被清除，不是Agent执行结束\
  生产环境，建议设置为持久存储，比如DB