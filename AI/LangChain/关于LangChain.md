LangChina是一个开源的框架，预置了搭建agent的框架，并且可以和很多LLM或工具集成
LangChain可以通过少量的代码，构建自定义agent和application
LangChain可以和很多LLM交互，这些LLM涵盖了当前主流的LLM，比如OpenAI, Anthropic, Google
LangChain也提供了很多已经封装好的相关provider的Integration，这些Integration提供了很多额外的能力，比如访问外部资源的能力，包括google search, 各种数据库连接，SaaS集成等等


LangChain有以下优势：
- 有统一标准的LLM交互接口，可以在不同的LLM之间切换
- 使用简单，高度灵活，既可以快速搭建简单的Agent，又可以制定高度灵活复杂的Agent
- LangChain的agent是基于LangGraph构建的，因此它可以利用LangGraph的一些优势
- LangChain可以通过LangSmith的Debug功能，可视化复杂的内部流程


LangChain生态包含以下几个组件：
- LangChain
  用于创建自定义Agent
  LangChain是基于LangGraph构建的

- LangGraph
  agent 工作流的编排系统
  适用于有固定流程，且需要高度自定义的场景

- Deep Agent
  Deep Agent是以LangChain为基础的一个具体实现
  它额外增加了一些功能，比如long conversations compression, virtual filesystem, subagent-spawning
  如果不需要这些额外的功能，或者想从头到尾创建一个自定义agent，可以选择LangChain

- LangSmith
  用于追踪请求，debug，评估输出结果等

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