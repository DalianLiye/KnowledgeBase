[目录](../目录.md)


# 关于消息内容
消息内容(content)可以理解为发送给模型的数据 “载荷”
消息的content属性是松散类型的，既支持字符串，也支持无类型对象列表（如字典）
这让LangChain对话模型可以直接支持服务商原生的结构，比如多模态内容和其他数据

同时，LangChain为文本、推理过程、引用、多模态数据、服务端工具调用等消息内容提供了专用的内容类型（Content Blocks）

LangChain对话模型通过content属性接受消息内容，可能包含以下三种形式：
- 字符串
- 服务商原生格式的内容块列表
- LangChain 标准内容块列表


```python
from langchain.messages import HumanMessage

# String content
human_message = HumanMessage("Hello, how are you?")

# Provider-native format (e.g., OpenAI)
human_message = HumanMessage(content=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
])

# List of standard content blocks
human_message = HumanMessage(content_blocks=[
    {"type": "text", "text": "Hello, how are you?"},
    {"type": "image", "url": "https://example.com/image.jpg"},
])
```

在初始化消息时指定content_blocks，依然会填充消息的content字段，同时提供了一种类型安全的接口


# 标准内容块
Standard content blocks\
LangChain提供了一套跨模型提供商通用的消息内容标准表示\
消息对象实现了content_blocks属性，它会惰性地将content属性解析为一套标准的、类型安全的表示

例如，ChatAnthropic或ChatOpenAI生成的消息，其thinking或reasoning块格式是各自服务商独有的\
但可以被惰性地解析为统一的 ReasoningContentBlock表示

示例：Anthropic
```python
from langchain.messages import AIMessage

message = AIMessage(
    content=[
        {"type": "thinking", "thinking": "...", "signature": "WaUjzkyp..."},
        {"type": "text", "text": "..."},
    ],
    response_metadata={"model_provider": "anthropic"}
)
message.content_blocks
```

示例：openAI
```python
from langchain.messages import AIMessage

message = AIMessage(
    content=[
        {
            "type": "reasoning",
            "id": "rs_abc123",
            "summary": [
                {"type": "summary_text", "text": "summary 1"},
                {"type": "summary_text", "text": "summary 2"},
            ],
        },
        {"type": "text", "text": "...", "id": "msg_abc123"},
    ],
    response_metadata={"model_provider": "openai"}
)
message.content_blocks
```

输出结构示例:
```json
[{'type': 'reasoning',
  'reasoning': '...',
  'extras': {'signature': 'WaUjzkyp...'}},
 {'type': 'text', 'text': '...'}]
```

**序列化标准内容**\
如果LangChain之外的应用程序需要访问标准内容块的表示，可以选择将内容块直接存储在消息的content字段中\
为此，可以将环境变量LC_OUTPUT_VERSION设置为v1，或者在初始化任何聊天模型时指定 output_version="v1"

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5-nano", output_version="v1")
```


# 多模态
多模态指的是处理不同形式数据的能力，比如文本、音频、图片和视频\
LangChain为这些数据提供了跨模型提供商通用的标准类型\
对话模型既可以接受多模态数据作为输入，也可以生成多模态数据作为输出

额外的参数可以直接写在内容块的顶层，也可以嵌套在"extras": {"key": value} 中\
例如，OpenAI 和 AWS Bedrock Converse 在处理 PDF 时需要提供文件名。具体细节请参考你所选择模型的提供商文档


示例：image input
```python
# From URL
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this image."},
        {"type": "image", "url": "https://example.com/path/to/image.jpg"},
    ]
}

# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this image."},
        {
            "type": "image",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "image/jpeg",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this image."},
        {"type": "image", "file_id": "file-abc123"},
    ]
}
```


示例：PDF input
```python
# From URL
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this document."},
        {"type": "file", "url": "https://example.com/path/to/document.pdf"},
    ]
}

# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this document."},
        {
            "type": "file",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "application/pdf",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this document."},
        {"type": "file", "file_id": "file-abc123"},
    ]
}
```

示例：audio input
```python
# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this audio."},
        {
            "type": "audio",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "audio/wav",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this audio."},
        {"type": "audio", "file_id": "file-abc123"},
    ]
}
```

示例：video input
```python
# From base64 data
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this video."},
        {
            "type": "video",
            "base64": "AAAAIGZ0eXBtcDQyAAAAAGlzb21tcDQyAAACAGlzb2...",
            "mime_type": "video/mp4",
        },
    ]
}

# From provider-managed File ID
message = {
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe the content of this video."},
        {"type": "video", "file_id": "file-abc123"},
    ]
}
```

注：并非所有模型都支持所有文件类型，具体需要参考各个模型供应商的文档


# 内容块参考
Content block reference\
内容块（无论是创建消息时，还是访问 content_blocks 属性时）都表示为类型化字典的列表

以下列表中的每个项都必须符合以下块类型之一

- Core
  - TextContentBlock
    Purpose: Standard text output
    - type: string required, 固定值"text"
    - text：string required，The text content
    - annotations object[]，List of annotations for the text
    - extras object，Additional provider-specific data
    - 示例：
      ```json
      {
          "type": "text",
          "text": "Hello world",
          "annotations": []
      }
      ```
  - ReasoningContentBlock
    Purpose: Model reasoning steps
    - type:string required, Always "reasoning"
    - reasoning: string The reasoning content
    - extras: object, Additional provider-specific data
    - 示例：
      ```json
      {
          "type": "reasoning",
          "reasoning": "The user is asking about...",
          "extras": {"signature": "abc123"},
      }
      ```
    其他属性参照：
    https://docs.langchain.com/oss/python/langchain/messages

content_blocks是LangChain v1中新增的消息属性，目的是在保持与现有代码向后兼容的同时，实现跨模型提供商的内容格式标准化\
content_blocks并不是content属性的替代品，而是一个新的属性，用于以标准化格式访问消息内容

