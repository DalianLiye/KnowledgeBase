[目录](../目录.md)


# 关于服务端工具调用
有些大模型服务商支持在服务端自动完成工具调用循环, 无需经由客户端再发一轮请求

**传统工具调用和服务端工具调用**
- **传统工具调用**\
  客户端发请求 → 模型说 “我要调用工具” → 客户端本地调用 → 客户端再把结果发回模型 → 模型回答\
  客户端需要两轮以及以上请求

- **服务端工具调用**\
  客户端发请求 → 模型在服务商服务器内部自己调用工具、自己拿结果、自己生成最终回答 → 直接把完整结果给客户端\
  客户端仅需一轮请求

# 返回格式
Langchain对调用服务端工具时返回的格式做了一层封装\
即服务端工具返回的结果，各服务商原生不统一，LangChain封装后才统一


# 返回结果
调用模型服务端工具返回的响应消息里，会直接包含工具调用的过程和结果，它被包含在响应里的content块里\
content块不是单纯字符串，而是结构化块数组

content里可能包含：
- 普通文本
- 工具调用（tool call）
- 工具执行结果（tool result）

# 示例

示例代表一轮完整对话回合，它不需要像客户端工具调用那样，再传入对应的ToolMessage对象
```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-4.1-mini")

tool = {"type": "web_search"}
model_with_tools = model.bind_tools([tool])

response = model_with_tools.invoke("What was a positive news story from today?")
print(response.content_blocks)
```

Result
```json
[
    {
        "type": "server_tool_call",
        "name": "web_search",
        "args": {
            "query": "positive news stories today",
            "type": "search"
        },
        "id": "ws_abc123"
    },
    {
        "type": "server_tool_result",
        "tool_call_id": "ws_abc123",
        "status": "success"
    },
    {
        "type": "text",
        "text": "Here are some positive news stories from today...",
        "annotations": [
            {
                "end_index": 410,
                "start_index": 337,
                "title": "article title",
                "type": "citation",
                "url": "..."
            }
        ]
    }
]
```


