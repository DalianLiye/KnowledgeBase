[目录](../目录.md)


# 关于System Prompt
通过system prompt，可以塑造agent如何执行task\
如果没有指定system prompt，Agent仅通过user prompt推理任务


通过 create_agent 的system_prompt参数指定提示词，值可以是字符串或SystemMessage对象

示例：指定字符串
```python
agent = create_agent(
    model,
    tools,
    system_prompt="You are a helpful assistant. Be concise and accurate."
)
```

示例：指定SystemMessage对象\
使用SystemMessage对象可以更细粒度控制Prompt结构\
不同模型提供商（provider）支持的属性不同\
例如 Anthropic支持cache_control实现内容块缓存，减少重复请求的延迟与成本

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


# Dynamic System Prompt
可以通过middleware，动态指定system prompt, 使用@dynamic_prompt装饰器实现

@dynamic_prompt是专门用于动态生成system prompt的钩子，并非请求拦截式中间件，因此只需返回字符串作为提示词，无需调用handler\
框架会在模型调用前自动执行该钩子，并将返回内容作为system prompt使用


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