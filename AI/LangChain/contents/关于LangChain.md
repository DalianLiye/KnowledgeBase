[目录](../目录.md)

LangChain是一个开源的框架，内置了构建Agent的能力和体系，并且可以和很多模型或工具集成\
LangChain可以通过少量的代码，构建自定义agent和application\
LangChain可以和很多模型交互，涵盖了当前主流的模型，比如OpenAI, Anthropic, Google\
LangChain也提供了很多已经封装好的相关provider的Integration，这些Integration提供了很多额外的能力，比如访问外部资源的能力，包括google search, 各种数据库连接，SaaS集成等等


LangChain核心优势：
- 提供统一标准的模型交互接口，可无缝切换不同模型
- 使用简单、高度灵活，快速搭建简单 Agent，也支持复杂定制
- 新版Agent基于LangGraph构建，因此它可以利用LangGraph的一些优势, 天然具备持久执行、流式输出、人工介入、状态持久等生产级能力
- 配合LangSmith实现可视化调试、追踪与评估


LangChain生态组件：

- **LangChain Core**\
  LangChain Core是LangChain底层接口与抽象（内核）\
  整个生态的最小内核、标准接口层，只定义规范、基类、协议，不含具体实现、不含第三方集成、不含高级链 / Agent

- **LangChain**\
  用于创建自定义Agent, 是基于LangChain Core封装的高层应用框架（业务层）\
  提供简洁API，底层依赖LangGraph运行时\
  快速构建Agent，无需关心底层编排

- **LangGraph**\
  agent底层工作流编排与运行时框架\
  提供状态管理、持久化、可控流程、多Agent等高级能力\
  适用于有固定流程，且需要高度自定义的场景

- **LangSmith**\
  调试、监控、追踪、评估工具

- **Deep Agent（非官方核心组件）**\
  基于LangChain的增强型Agent实现\
  内置长对话压缩、虚拟文件系统、子Agent等高级特性

注：LangChain Core，LangChain和LangGraph的依赖关系如下： 
- LangGraph → 依赖 → LangChain Core
- LangChain → 依赖 → LangChain Core + LangGraph

以下是一个简单的示例
```python
# pip install -qU langchain "langchain[anthropic]"
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```