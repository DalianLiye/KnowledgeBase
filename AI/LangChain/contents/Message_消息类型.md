[目录](../目录.md)


# 关于消息类型

- **系统消息(System message)**\
  用于告诉模型如何行为，并为交互提供上下文
- **人类消息(Human message)**\
  代表用户输入以及与模型的交互
- **AI 消息(AI message)**\
  模型生成的响应，包括文本内容、工具调用和元数据
- **工具消息(Tool message)**
  代表工具调用的返回结果


## 系统消息
系统消息(System Message)代表一组用于 “预调” 模型行为的初始指令
可以用系统消息来设定对话语气、定义模型角色，并为回复建立行为准则

示例：Basic instructions
```python
system_msg = SystemMessage("You are a helpful coding assistant.")

messages = [
    system_msg,
    HumanMessage("How do I create a REST API?")
]
response = model.invoke(messages)
```

示例：Detailed persona
```python
from langchain.messages import SystemMessage, HumanMessage

system_msg = SystemMessage("""
You are a senior Python developer with expertise in web frameworks.
Always provide code examples and explain your reasoning.
Be concise but thorough in your explanations.
""")

messages = [
    system_msg,
    HumanMessage("How do I create a REST API?")
]
response = model.invoke(messages)
```


## 人类消息
人类消息(Human Message)代表用户的输入和交互，它可以包含文本、图片、音频、文件以及其他任何形式的多模态内容

**文本内容**\
Message object
```python
response = model.invoke([
  HumanMessage("What is machine learning?")
])
```

String shortcut
```python
# Using a string is a shortcut for a single HumanMessage
response = model.invoke("What is machine learning?")
```

**消息元数据**
```python
human_msg = HumanMessage(
    content="Hello!",
    name="alice",  # Optional: identify different users
    id="msg_123",  # Optional: unique identifier for tracing
)
```


## AI消息
AI消息(AI Message)代表模型调用的输出\
它可以包含多模态数据、工具调用以及后续可以访问的、模型提供商特定的元数据

```python
response = model.invoke("Explain AI")
print(type(response))  # <class 'langchain.messages.AIMessage'>
```

不同模型提供商对消息类型的处理和解读方式不同\
因此有时手动创建一个新的AIMessage对象，并将其插入消息历史（就像它来自模型一样）会很有帮助

```python
from langchain.messages import AIMessage, SystemMessage, HumanMessage

# Create an AI message manually (e.g., for conversation history)
ai_msg = AIMessage("I'd be happy to help you with that question!")

# Add to conversation history
messages = [
    SystemMessage("You are a helpful assistant"),
    HumanMessage("Can you help me?"),
    ai_msg,  # Insert as if it came from the model
    HumanMessage("Great! What's 2+2?")
]

response = model.invoke(messages)
```

**AIMessage核心属性:**
- **text**\
  类型：string\
  说明：消息的文本内容（便捷访问方式）
- **content**\
  类型：string | dict[]\
  说明：消息的原始内容，纯文本时是字符串，多模态 / 结构化时是字典列表
- **content_blocks**\
  类型：ContentBlock[]\
  说明：标准化的消息内容块，LangChain统一的多模态内容格式
- **tool_calls**\
  类型：dict[] | None\
  说明：模型发起的工具调用列表；如果没有调用工具则为空
- **id**\
  类型：string\
  说明：消息的唯一标识符，由LangChain自动生成或由模型服务商返回
- **usage_metadata**\
  类型：dict | None\
  说明：消息的使用元数据，可用时会包含Token消耗等信息
- **response_metadata**\
  类型：ResponseMetadata | None\
  说明：表示该消息的响应元数据

**工具调用**\
当模型发起工具调用时，这些调用会被包含在AIMessage中\
其他结构化数据，例如推理过程或引用信息，也可以出现在消息的content字段中

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano")

def get_weather(location: str) -> str:
    """Get the weather at a location."""
    ...

model_with_tools = model.bind_tools([get_weather])
response = model_with_tools.invoke("What's the weather in Paris?")

for tool_call in response.tool_calls:
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
    print(f"ID: {tool_call['id']}")
```


**Token使用**\
AIMessage可以在它的usage_metadata字段中存储Token计数和其他使用元数据

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano")

response = model.invoke("Hello!")
response.usage_metadata
```

```json
{'input_tokens': 8,
 'output_tokens': 304,
 'total_tokens': 312,
 'input_token_details': {'audio': 0, 'cache_read': 0},
 'output_token_details': {'audio': 0, 'reasoning': 256}}
```


**流式输出与数据块**\
在流式输出过程中，会收到AIMessageChunk对象，这些对象可以合并成一个完整的消息对象

```python
chunks = []
full_message = None
for chunk in model.stream("Hi"):
    chunks.append(chunk)
    print(chunk.text)
    full_message = chunk if full_message is None else full_message + chunk
```


## 工具消息
对于支持工具调用的模型，AI消息中可以包含工具调用请求\
工具消息用于将单次工具执行的结果传回给模型\
工具可以直接生成ToolMessage对象

```python
from langchain.messages import AIMessage
from langchain.messages import ToolMessage

# After a model makes a tool call
# (Here, we demonstrate manually creating the messages for brevity)
ai_message = AIMessage(
    content=[],
    tool_calls=[{
        "name": "get_weather",
        "args": {"location": "San Francisco"},
        "id": "call_123"
    }]
)

# Execute tool and create result message
weather_result = "Sunny, 72°F"
tool_message = ToolMessage(
    content=weather_result,
    tool_call_id="call_123"  # Must match the call ID
)

# Continue conversation
messages = [
    HumanMessage("What's the weather in San Francisco?"),
    ai_message,  # Model's tool call
    tool_message,  # Tool execution result
]
response = model.invoke(messages)  # Model processes the result
```
**ToolMessage 核心属性：**
- **content**\
  类型：string\
  说明：required，工具调用结果的字符串化输出，会直接发送给模型
- **tool_call_id**\
  类型：string\
  说明：required，该消息对应的工具调用 ID，必须与 AIMessage 中工具调用的 ID 完全匹配
- **name**\
  类型：string\
  说明：required，被调用的工具名称
- **artifact**\
  类型：dict\
  说明：可选，不会发送给模型的额外数据，可用于程序内部访问和调试

**artifact字段说明**\
artifact字段用于存储补充数据，这些数据不会发送给模型，但可以通过程序访问\
它适合用来保存原始结果、调试信息，或供后续处理使用的数据，同时又不会污染模型的上下文

例如，一个检索工具可以从文档中提取一段内容供模型参考\
content字段存放模型会引用的文本，而artifact字段可以存放文档标识符或其他元数据，供应用程序后续使用（例如，用来渲染页面）

示例：使用 artifact 存储检索元数据
```python
from langchain.messages import ToolMessage

# Sent to model
message_content = "It was the best of times, it was the worst of times."

# Artifact available downstream
artifact = {"document_id": "doc_123", "page": 0}

tool_message = ToolMessage(
    content=message_content,
    tool_call_id="call_123",
    name="search_books",
    artifact=artifact,
)
```

