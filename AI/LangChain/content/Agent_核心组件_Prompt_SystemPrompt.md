# 关于System prompt
通过system prompt，可以塑造agent如何执行task\
如果没有指定system prompt，那么agent就只通过user prompt来推理task


通过create_agent的system_prompt参数指定prompt，值可以是字符串，或SystemMessage对象\
示例：指定字符串
```python
agent = create_agent(
    model,
    tools,
    system_prompt="You are a helpful assistant. Be concise and accurate."
)
```

示例：指定SystemMessage对象\
指定SystemMessage对象，可以更细粒度的控制Prompt的结构\
不同的provider，SystemMessage对象里的属性也会不同\
比如，cache_control属性可以让Anthropic缓存content block，以此减少重复请求的延迟和成本
```python
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage

literary_agent = create_agent(
    model="anthropic:claude-sonnet-4-5",
    system_prompt=SystemMessage(
        content=[
            {
                "type": "text",
                "text": "You are an AI assistant tasked with analyzing literary works.",
            },
            {
                "type": "text",
                "text": "<the entire contents of 'Pride and Prejudice'>",
                "cache_control": {"type": "ephemeral"}
            }
        ]
    )
)

result = literary_agent.invoke(
    {"messages": [HumanMessage("Analyze the major themes in 'Pride and Prejudice'.")]}
)
```

# Dynamic system prompt
可以通过middleware，动态指定system prompt\
middleware使用@dynamic_prompt 装饰器

使用@dynamic_prompt 装饰器的middleware不需要return handler(request)\
因为它不是“拦截-再放行”的 handler 风格 middleware，而是 LangChain 里一种“动态生成 prompt 的中间件/钩子”\
即框架会在发起模型请求前调用它，把它的返回字符串当作（或注入为）system prompt 的一部分/全部

示例：
```python
from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest


class Context(TypedDict):
    user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
    """Generate system prompt based on user role."""
    user_role = request.runtime.context.get("user_role", "user")
    base_prompt = "You are a helpful assistant."

    if user_role == "expert":
        return f"{base_prompt} Provide detailed technical responses."
    elif user_role == "beginner":
        return f"{base_prompt} Explain concepts simply and avoid jargon."

    return base_prompt

agent = create_agent(
    model="gpt-4.1",
    tools=[web_search],
    middleware=[user_role_prompt],
    context_schema=Context
)

# The system prompt will be set dynamically based on context
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Explain machine learning"}]},
    context={"user_role": "expert"}
)
```