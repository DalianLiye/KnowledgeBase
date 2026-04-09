[目录](../目录.md)


# 关于Agent命名
create_agent函数支持可选参数name，用于为Agent设置名称\
在多Agent系统中，该名称会作为子图（subgraph）节点标识符

示例：
```python
agent = create_agent(
    model,
    tools,
    name="research_assistant"
)
```

# 命名规范
推荐使用snake_case（小写字母 + 下划线），避免空格与特殊符号
仅使用字母、数字、下划线、连字符，保证跨供应商平台兼容性



