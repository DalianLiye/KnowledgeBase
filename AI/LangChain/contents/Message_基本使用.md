[目录](../目录.md)


# 基本使用
使用消息的最简单方式，就是创建消息对象，并在调用模型时将它们传入
```python
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("gpt-5-nano")

system_msg = SystemMessage("You are a helpful assistant.")
human_msg = HumanMessage("Hello, how are you?")

# Use with chat models
messages = [system_msg, human_msg]
response = model.invoke(messages)  # Returns AIMessage
```

## 文本提示词
文本提示词（text prompts）就是普通字符串，非常适合不需要保留对话历史的简单生成任务

```python
response = model.invoke("Write a haiku about spring")
```

**使用场景：**
- 单次、独立的请求
- 不需要对话历史
- 希望代码复杂度最低


## 消息提示词
也可以通过传入消息对象列表(message prompts)的方式，给模型发送多条消息

它通过专门的消息对象（SystemMessage、HumanMessage、AIMessage）来构建对话上下文，而不是简单的字符串\
这种方式能清晰区分不同角色的消息，让模型理解对话结构


```python
from langchain.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage("You are a poetry expert"),
    HumanMessage("Write a haiku about spring"),
    AIMessage("Cherry blossoms bloom...")
]
response = model.invoke(messages)
```

**使用场景：**
- 管理多轮对话
- 处理多模态内容（图片、音频、文件）
- 必须包含系统指令
- 需要记录完整对话历史


## 字典格式
也可以直接使用OpenAI风格的字典格式 来定义消息，LangChain会自动解析
```python
messages = [
    {"role": "system", "content": "You are a poetry expert"},
    {"role": "user", "content": "Write a haiku about spring"},
    {"role": "assistant", "content": "Cherry blossoms bloom..."}
]
response = model.invoke(messages)
```