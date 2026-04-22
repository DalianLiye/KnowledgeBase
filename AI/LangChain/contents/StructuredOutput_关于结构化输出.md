[目录](../目录.md)


# 关于结构化输出
结构化输出允许 agent 以特定、可预测的格式返回数据。你无需再解析自然语言响应，而是可以直接获取 JSON 对象、Pydantic 模型或数据类形式的结构化数据，供应用程序直接使用。

提示：本页介绍了使用 create_agent 的 agent 结构化输出。如需直接在模型上使用结构化输出（不使用 agent），请参阅「Models - Structured output」部分

LangChain 的 create_agent 会自动处理结构化输出。用户设置期望的结构化输出 schema 后，当模型生成结构化数据时，它会被捕获、验证，并以 structured_response 键的形式返回到 agent 的状态中

```python
def create_agent(
    ...
    response_format: Union[
        ToolStrategy[StructuredResponseT],
        ProviderStrategy[StructuredResponseT],
        type[StructuredResponseT],
        None,
    ]
```