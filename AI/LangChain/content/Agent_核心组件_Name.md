# 关于Name
当通过create_agent函数创建agent时，有一个可选项name，它会为agent设置名称\
当该agent在多agent系统中作为subgraph添加时，name将用作节点标识符

示例：
```python
agent = create_agent(
    model,
    tools,
    name="research_assistant"
)
```

# 命名规范
agent名称推荐的命名规范：snake_case 格式\
比如research_assistant，而不是Research Assistant\
因为有一些provider会不识别空格或一些特殊字符\
仅使用字母数字字符、下划线和连字符可以确保在所有提供商之间的兼容性