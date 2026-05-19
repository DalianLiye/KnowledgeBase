[目录](../目录.md)


# 关于结构化输出
结构化输出可让agent按固定规范格式返回数据，无需解析自然语言\
可直接获取JSON、Pydantic模型等结构化数据，方便应用直接使用

LangChain的create_agent原生支持结构化输出：\
只需定义输出Schema，模型生成的结构化数据会被自动捕获、验证，并以structured_response存入agent状态

部分模型支持原生结构化输出，下文示例基于create_agent实现框架层结构化输出，不依赖模型原生能力

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