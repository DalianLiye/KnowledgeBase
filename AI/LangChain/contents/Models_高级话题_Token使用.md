[目录](../目录.md)


# 关于Token使用

Token使用(Token usage)指的是模型调用中消耗的Token数量，包括：
- 输入 Token（prompt 部分）
- 输出 Token（模型生成部分）

Token使用是计费和限流的核心依据，也是成本控制的核心指标


# 获取Token使用信息

**非流式调用**\
在非流式调用中，Token使用信息会直接包含在返回的AIMessage对象里\
可以通过 response.response_metadata["token_usage"] 访问

```python
response = model.invoke("Hello")
print(response.response_metadata["token_usage"])
# 输出类似：{"prompt_tokens": 5, "completion_tokens": 10, "total_tokens": 15}
```

**流式调用**\
OpenAI/Azure OpenAI等服务商，在流式（streaming）模式下，默认不返回Token使用数据\
需要主动开启相关选项（如 stream_options={"include_usage": True}），才能在流结束时收到Token使用信息


**全局统计**\
LangChain可以跟踪整个应用的累计Token消耗，通过以下两种方式：
- **回调函数（callback）**\
  在每次模型调用时自动记录Token使用情况
- **上下文管理器（context manager）**\
  在特定代码块内统计Token消耗

示例1：callback handler
```python
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import UsageMetadataCallbackHandler

model_1 = init_chat_model(model="gpt-4.1-mini")
model_2 = init_chat_model(model="claude-haiku-4-5-20251001")

callback = UsageMetadataCallbackHandler()
result_1 = model_1.invoke("Hello", config={"callbacks": [callback]})
result_2 = model_2.invoke("Hello", config={"callbacks": [callback]})
print(callback.usage_metadata)
```

示例2：context manager
```python
from langchain.chat_models import init_chat_model
from langchain_core.callbacks import get_usage_metadata_callback

model_1 = init_chat_model(model="gpt-4.1-mini")
model_2 = init_chat_model(model="claude-haiku-4-5-20251001")

with get_usage_metadata_callback() as cb:
    model_1.invoke("Hello")
    model_2.invoke("Hello")
    print(cb.usage_metadata)
```

示例1和示例2返回结果
```json
{
    'gpt-4.1-mini-2025-04-14': {
        'input_tokens': 8,
        'output_tokens': 10,
        'total_tokens': 18,
        'input_token_details': {'audio': 0, 'cache_read': 0},
        'output_token_details': {'audio': 0, 'reasoning': 0}
    },
    'claude-haiku-4-5-20251001': {
        'input_tokens': 8,
        'output_tokens': 21,
        'total_tokens': 29,
        'input_token_details': {'cache_read': 0, 'cache_creation': 0}
    }
}
```

# 总结
Token使用情况是模型调用的关键数据，非流式调用可直接从AIMessage中获取\
OpenAI/Azure OpenAI流式调用需主动开启才能获取\
LangChain支持通过回调或上下文管理器实现全局Token统计