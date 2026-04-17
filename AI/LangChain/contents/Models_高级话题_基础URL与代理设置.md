[目录](../目录.md)


# 关于基础URL与代理设置

对于实现了OpenAI对话补全API规范的服务商，可以配置自定义基础URL

使用model_provider="openai"（或直接使用 ChatOpenAI）时，它会严格遵循OpenAI官方的API规范\
来自路由/代理服务商的特有扩展字段，可能无法被正确解析或保留

对于OpenRouter和LiteLLM，推荐使用它们的专用集成：
- OpenRouter via ChatOpenRouter（langchain-openrouter 包）
- LiteLLM via ChatLiteLLM / ChatLiteLLMRouter（langchain-litellm 包）


# 自定义基础URL

许多模型服务商提供兼容OpenAI格式的API（例如 DeepSeek）\
它们都采用了和OpenAI一致的接口规范（如 /chat/completions接口格式）\
这意味着可以用同一套OpenAI风格代码调用不同服务商的模型\
关键就是通过base_url参数，将请求转发到目标服务商的地址\
可以通过指定对应的base_url参数，使用init_chat_model调用这些服务商的模型

**总结:**\
只要模型是OpenAI兼容API，model_provider就固定写"openai"，只需要替换base_url

```python
model = init_chat_model(
    model="MODEL_NAME",
    model_provider="openai",
    base_url="BASE_URL",
    api_key="YOUR_API_KEY",
)
```


# HTTP代理配置

当应用服务部署在受网络限制的环境中（比如企业内网、无法直接访问 OpenAI 等外部服务），需要通过HTTP代理来转发请求，才能正常调用模型API\
对于需要通过HTTP代理的环境，部分模型集成支持代理配置

不同模型服务商/集成的代理配置方式不同：
- langchain-openai用openai_proxy 参数
- 其他服务商可能用proxy、http_proxy或通过环境变量配置


```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-4.1",
    openai_proxy="http://proxy.example.com:8080"
)
```

**总结：**\
在受限网络环境中调用OpenAI系列模型时，可以通过openai_proxy参数配置HTTP代理\
但不同模型集成的代理支持方式不同，需要查阅对应文档确认
