[目录](../目录.md)

# 响应格式

使用 response_format 来控制 agent 返回结构化数据的方式：
- ToolStrategy[StructuredResponseT]：使用工具调用实现结构化输出
- ProviderStrategy[StructuredResponseT]：使用模型服务商原生的结构化输出能力
- type[StructuredResponseT]：直接传入 Schema 类型，LangChain 会根据模型能力自动选择最佳策略
- None：不明确要求结构化输出

当直接传入一个 Schema 类型时，LangChain 会自动选择策略：
- 如果模型和服务商支持原生结构化输出（如 OpenAI、Anthropic (Claude) 或 xAI (Grok)），则使用 ProviderStrategy
- 对于所有其他模型，则使用 ToolStrategy

使用 langchain>=1.1 时，对原生结构化输出功能的支持会动态从模型的 profile 数据中读取。如果无法获取数据，可以使用其他条件或手动指定：
```python
custom_profile = {
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```

如果指定了工具，模型必须支持同时使用工具和结构化输出。
结构化响应会返回到 agent 最终状态的 structured_response 键中。