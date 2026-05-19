[目录](../目录.md)

# 响应格式

使用response_format来控制agent返回结构化数据的方式：
- **ToolStrategy[StructuredResponseT]**\
  通过工具调用实现结构化输出
- **ProviderStrategy[StructuredResponseT]**\
  使用模型服务商原生的结构化输出能力
- **type[StructuredResponseT]**\
  直接传入Schema类型，LangChain会根据模型能力自动选择最佳策略\
  只定好要什么格式数据，框架自动选最合适的方式
- **None**\
  不明确要求结构化输出, 不限制格式，AI随便自由回答

直接传入Schema类型时，LangChain的自动选择策略如下：
- 如果模型/服务商支持原生结构化输出（如 OpenAI、Anthropic (Claude) 或 xAI (Grok)），自动使用ProviderStrategy
- 其他模型默认使用ToolStrategy

使用langchain>=1.1时，会自动识别模型支不支持结构化输出\
它会自动从模型profile动态读取信息的方式来识别\
如果无法从模型profile动态获取，那么就手动配置：
```python
custom_profile = {
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```

**注：**\
如果代码里同时用到了工具调用，所使用的模型必须既要能用工具，又要支持规整格式输出\
最终整理好的标准数据，都会统一放在structured_response里面直接取用