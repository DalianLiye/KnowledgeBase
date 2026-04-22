[目录](../目录.md)


# Streaming thinking /reasoning tokens

部分模型在生成最终答案前会进行内部推理
你可以通过筛选 type 为 "reasoning" 的标准内容块，来流式输出这些思考 / 推理 Token

重要提示：推理输出必须在模型端开启

要从 agent 中流式输出思考 Token，使用 stream_mode="messages" 并筛选推理内容块

```python
from langchain.agents import create_agent
from langchain.messages import AIMessageChunk
from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import Runnable


def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"


model = ChatAnthropic(
    model_name="claude-sonnet-4-6",
    timeout=None,
    stop=None,
    thinking={"type": "enabled", "budget_tokens": 5000},
)
agent: Runnable = create_agent(
    model=model,
    tools=[get_weather],
)

for token, metadata in agent.stream(
    {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
    stream_mode="messages",
):
    if not isinstance(token, AIMessageChunk):
        continue
    reasoning = [b for b in token.content_blocks if b["type"] == "reasoning"]
    text = [b for b in token.content_blocks if b["type"] == "text"]
    if reasoning:
        print(f"[thinking] {reasoning[0]['reasoning']}", end="")
    if text:
        print(text[0]["text"], end="")
```

```text
[thinking] The user is asking about the weather in San Francisco. I have a tool
[thinking]  available to get this information. Let me call the get_weather tool
[thinking]  with "San Francisco" as the city parameter.
The weather in San Francisco is: It's always sunny in San Francisco!
```
无论使用哪个模型服务商，其工作方式都是一致的：LangChain 会通过 content_blocks 属性，将不同服务商的特定格式（如 Anthropic 的 thinking 块、OpenAI 的 reasoning summaries 等）标准化为统一的 "reasoning" 内容块类型


# 流式输出工具调用（Streaming tool calls）
你可能希望同时流式输出以下两种信息：
- 工具调用生成过程中的部分 JSON（Partial JSON）
- 执行完成、已解析的工具调用结果
设置 stream_mode="messages" 会流式输出 agent 中所有 LLM 调用生成的增量消息块
要获取包含已解析工具调用的完整消息：
- 如果这些消息被记录在 state 中（如 create_agent 的模型节点），使用 stream_mode=["messages", "updates"]，通过状态更新来访问完整消息（下方会演示）。
- 如果这些消息未被记录在 state 中，使用自定义更新，或在流式循环中手动聚合块内容（下一节介绍）。

提示：如果你的 agent 包含多个 LLM，请参阅下方关于子代理流式输出的章节

```python
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


agent = create_agent("openai:gpt-5.2", tools=[get_weather])


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)
    # N.B. all content is available through token.content_blocks


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):  # `source` captures node name
                _render_completed_message(update["messages"][-1])
```

```text
[{'name': 'get_weather', 'args': '', 'id': 'call_D3Orjr89KgsLTZ9hTzYv7Hpf', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_D3Orjr89KgsLTZ9hTzYv7Hpf', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
The| weather| in| Boston| is| **|sun|ny|**|.|
```

**Accessing completed messages（访问已完成消息）**\
 重要提示：如果已完成消息被记录在 agent 的 state 中，你可以使用 stream_mode=["messages", "updates"]（如流式工具调用部分所示），从而在流式过程中访问已完成消息。

在某些情况下，已完成的消息不会体现在 state 更新中。如果你能访问 agent 内部逻辑，可以使用 自定义更新（custom updates） 来在流式过程中访问这些消息；否则，你可以在流式循环中聚合消息块（见下文）。

思考以下示例：我们在一个简化的 guardrail middleware（防护中间件） 中集成了流写入器（stream writer）。该中间件通过工具调用来生成结构化的 “安全 / 不安全（safe/unsafe）” 评估结果（你也可以使用结构化输出（structured outputs）来实现这一点）
```python
from typing import Any, Literal

from langchain.agents.middleware import after_agent, AgentState
from langgraph.runtime import Runtime
from langchain.messages import AIMessage
from langchain.chat_models import init_chat_model
from langgraph.config import get_stream_writer  
from pydantic import BaseModel


class ResponseSafety(BaseModel):
    """Evaluate a response as safe or unsafe."""
    evaluation: Literal["safe", "unsafe"]


safety_model = init_chat_model("openai:gpt-5.2")

@after_agent(can_jump_to=["end"])
def safety_guardrail(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Model-based guardrail: Use an LLM to evaluate response safety."""
    stream_writer = get_stream_writer()
    # Get the model response
    if not state["messages"]:
        return None

    last_message = state["messages"][-1]
    if not isinstance(last_message, AIMessage):
        return None

    # Use another model to evaluate safety
    model_with_tools = safety_model.bind_tools([ResponseSafety], tool_choice="any")
    result = model_with_tools.invoke(
        [
            {
                "role": "system",
                "content": "Evaluate this AI response as generally safe or unsafe."
            },
            {
                "role": "user",
                "content": f"AI response: {last_message.text}"
            }
        ]
    )
    stream_writer(result)

    tool_call = result.tool_calls[0]
    if tool_call["args"]["evaluation"] == "unsafe":
        last_message.content = "I cannot provide that response. Please rephrase your request."

    return None
```


接下来，我们可以将这个中间件集成到 agent 中，并包含它的自定义流事件：
```python
from typing import Any

from langchain.agents import create_agent
from langchain.messages import AIMessageChunk, AIMessage, AnyMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


agent = create_agent(
    model="openai:gpt-5.2",
    tools=[get_weather],
    middleware=[safety_guardrail],
)

def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates", "custom"],
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
    elif chunk["type"] == "custom":
        # access completed message in stream
        print(f"Tool calls: {chunk['data'].tool_calls}")
```

```text
[{'name': 'get_weather', 'args': '', 'id': 'call_je6LWgxYzuZ84mmoDalTYMJC', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_je6LWgxYzuZ84mmoDalTYMJC', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
The| weather| in| **|Boston|**| is| **|sun|ny|**|.|[{'name': 'ResponseSafety', 'args': '', 'id': 'call_O8VJIbOG4Q9nQF0T8ltVi58O', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'evaluation', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'safe', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'ResponseSafety', 'args': {'evaluation': 'safe'}, 'id': 'call_O8VJIbOG4Q9nQF0T8ltVi58O', 'type': 'tool_call'}]
```


或者，如果你无法向流中添加自定义事件，可以在流式循环中聚合消息块：

```python
input_message = {"role": "user", "content": "What is the weather in Boston?"}
full_message = None
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
            full_message = token if full_message is None else full_message + token  
            if token.chunk_position == "last":
                if full_message.tool_calls:
                    print(f"Tool calls: {full_message.tool_calls}")
                full_message = None
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source == "tools":
                _render_completed_message(update["messages"][-1])
```

# Streaming with human-in-the-loop（带人工干预的流式输出）
要处理人工干预中断，我们基于上述示例进行扩展：
- 为 agent 配置人工干预中间件和检查点（checkpointer）
- 收集在 updates 流模式下生成的中断事件
- 使用 command 响应这些中断

```python
from typing import Any

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.messages import AIMessage, AIMessageChunk, AnyMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command, Interrupt


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


checkpointer = InMemorySaver()

agent = create_agent(
    "openai:gpt-5.2",
    tools=[get_weather],
    middleware=[
        HumanInTheLoopMiddleware(interrupt_on={"get_weather": True}),
    ],
    checkpointer=checkpointer,
)


def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


def _render_interrupt(interrupt: Interrupt) -> None:
    interrupts = interrupt.value  
    for request in interrupts["action_requests"]:
        print(request["description"])


input_message = {
    "role": "user",
    "content": (
        "Can you look up the weather in Boston and San Francisco?"
    ),
}
config = {"configurable": {"thread_id": "some_id"}}
interrupts = []
for chunk in agent.stream(
    {"messages": [input_message]},
    config=config,
    stream_mode=["messages", "updates"],
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            if source == "__interrupt__":
                interrupts.extend(update)
                _render_interrupt(update[0])
```

```text
[{'name': 'get_weather', 'args': '', 'id': 'call_GOwNaQHeqMixay2qy80padfE', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"ci', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ty": ', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"Bosto', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'n"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': 'get_weather', 'args': '', 'id': 'call_Ndb4jvWm2uMA0JDQXu37wDH6', 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"ci', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ty": ', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"San F', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'ranc', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'isco"', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '}', 'id': None, 'index': 1, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_GOwNaQHeqMixay2qy80padfE', 'type': 'tool_call'}, {'name': 'get_weather', 'args': {'city': 'San Francisco'}, 'id': 'call_Ndb4jvWm2uMA0JDQXu37wDH6', 'type': 'tool_call'}]
Tool execution requires approval

Tool: get_weather
Args: {'city': 'Boston'}
Tool execution requires approval

Tool: get_weather
Args: {'city': 'San Francisco'}
```

接下来，我们为每个中断收集一个决策。重要的是，决策的顺序必须与我们收集到的动作顺序相匹配。
为了说明，我们将编辑一个工具调用，并接受另一个：

```python
def _get_interrupt_decisions(interrupt: Interrupt) -> list[dict]:
    return [
        {
            "type": "edit",
            "edited_action": {
                "name": "get_weather",
                "args": {"city": "Boston, U.K."},
            },
        }
        if "boston" in request["description"].lower()
        else {"type": "approve"}
        for request in interrupt.value["action_requests"]
    ]

decisions = {}
for interrupt in interrupts:
    decisions[interrupt.id] = {
        "decisions": _get_interrupt_decisions(interrupt)
    }

decisions
```

```text
{
    'a96c40474e429d661b5b32a8d86f0f3e': {
        'decisions': [
            {
                'type': 'edit',
                 'edited_action': {
                     'name': 'get_weather',
                     'args': {'city': 'Boston, U.K.'}
                 }
            },
            {'type': 'approve'},
        ]
    }
}
```

接下来，我们可以通过向同一个流式循环传入 command 来恢复执行：
```python
interrupts = []
for chunk in agent.stream(
    Command(resume=decisions),
    config=config,
    stream_mode=["messages", "updates"],
    version="v2",
):
    # Streaming loop is unchanged
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if isinstance(token, AIMessageChunk):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
            if source == "__interrupt__":
                interrupts.extend(update)
                _render_interrupt(update[0])
```

```text
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston, U.K.!"}]
Tool response: [{'type': 'text', 'text': "It's always sunny in San Francisco!"}]
-| **|Boston|**|:| It|'s| always| sunny| in| Boston|,| U|.K|.|
|-| **|San| Francisco|**|:| It|'s| always| sunny| in| San| Francisco|!|
```


# 子代理流式输出（Streaming from sub-agents）
当 agent 中的任意环节存在多个 LLM 时，通常需要区分生成消息的来源

为此，创建每个 agent 时传入 name 参数。在 messages 模式下流式输出时，可通过元数据中的 lc_agent_name 键获取该名称

下面，我们更新「流式工具调用」示例：
- 将工具替换为内部调用 agent 的 call_weather_agent 工具
- 为每个 agent 添加 name
- 创建流时指定 subgraphs=True
- 流处理逻辑与之前相同，但新增了利用 create_agent 的 name 参数追踪当前活跃 agent 的逻辑

提示：为 agent 设置 name 后，该名称也会附加到该 agent 生成的所有 AIMessage 上。
接下来，我们先构建 agent：



First we construct the agent:
```python
from typing import Any

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain.messages import AIMessage, AnyMessage


def get_weather(city: str) -> str:
    """Get weather for a given city."""

    return f"It's always sunny in {city}!"


weather_model = init_chat_model("openai:gpt-5.2")
weather_agent = create_agent(
    model=weather_model,
    tools=[get_weather],
    name="weather_agent",
)


def call_weather_agent(query: str) -> str:
    """Query the weather agent."""
    result = weather_agent.invoke({
        "messages": [{"role": "user", "content": query}]
    })
    return result["messages"][-1].text


supervisor_model = init_chat_model("openai:gpt-5.2")
agent = create_agent(
    model=supervisor_model,
    tools=[call_weather_agent],
    name="supervisor",
)
```

Next, we add logic to the streaming loop to report which agent is emitting tokens:
```python
def _render_message_chunk(token: AIMessageChunk) -> None:
    if token.text:
        print(token.text, end="|")
    if token.tool_call_chunks:
        print(token.tool_call_chunks)


def _render_completed_message(message: AnyMessage) -> None:
    if isinstance(message, AIMessage) and message.tool_calls:
        print(f"Tool calls: {message.tool_calls}")
    if isinstance(message, ToolMessage):
        print(f"Tool response: {message.content_blocks}")


input_message = {"role": "user", "content": "What is the weather in Boston?"}
current_agent = None
for chunk in agent.stream(
    {"messages": [input_message]},
    stream_mode=["messages", "updates"],
    subgraphs=True,
    version="v2",
):
    if chunk["type"] == "messages":
        token, metadata = chunk["data"]
        if agent_name := metadata.get("lc_agent_name"):
            if agent_name != current_agent:
                print(f"🤖 {agent_name}: ")
                current_agent = agent_name  
        if isinstance(token, AIMessage):
            _render_message_chunk(token)
    elif chunk["type"] == "updates":
        for source, update in chunk["data"].items():
            if source in ("model", "tools"):
                _render_completed_message(update["messages"][-1])
```

```text
🤖 supervisor:
[{'name': 'call_weather_agent', 'args': '', 'id': 'call_asorzUf0mB6sb7MiKfgojp7I', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'query', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' weather', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' right', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' now', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' and', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': " today's", 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': ' forecast', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'call_weather_agent', 'args': {'query': "Boston weather right now and today's forecast"}, 'id': 'call_asorzUf0mB6sb7MiKfgojp7I', 'type': 'tool_call'}]
🤖 weather_agent:
[{'name': 'get_weather', 'args': '', 'id': 'call_LZ89lT8fW6w8vqck5pZeaDIx', 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '{"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'city', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '":"', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': 'Boston', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
[{'name': None, 'args': '"}', 'id': None, 'index': 0, 'type': 'tool_call_chunk'}]
Tool calls: [{'name': 'get_weather', 'args': {'city': 'Boston'}, 'id': 'call_LZ89lT8fW6w8vqck5pZeaDIx', 'type': 'tool_call'}]
Tool response: [{'type': 'text', 'text': "It's always sunny in Boston!"}]
Boston| weather| right| now|:| **|Sunny|**|.

|Today|'s| forecast| for| Boston|:| **|Sunny| all| day|**|.|Tool response: [{'type': 'text', 'text': 'Boston weather right now: **Sunny**.\n\nToday's forecast for Boston: **Sunny all day**.'}]
🤖 supervisor:
Boston| weather| right| now|:| **|Sunny|**|.

|Today|'s| forecast| for| Boston|:| **|Sunny| all| day|**|.|
```