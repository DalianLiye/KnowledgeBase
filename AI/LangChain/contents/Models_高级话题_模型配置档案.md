[目录](../目录.md)


# 关于模型配置档案

模型配置档案（Model profile）可以让程序根据模型能力（上下文长度、tool_calling、模态、最大 token 等）动态自适应，不用硬编码\
目前属于beta测试功能，配置的格式未来可能会变化\
要求的langchain版本： >= 1.1

LangChain初始化chat model时，会自带一个.profile属性\
该属性是一个字典，里面包含模型支持的所有特性和能力\
这个字典就是模型配置档案


```python
model.profile
# {
#   "max_input_tokens": 400000,
#   "image_inputs": True,
#   "reasoning_output": True,
#   "tool_calling": True,
#   ...
# }

custom_profile = {
    "max_input_tokens": 100_000,
    "tool_calling": True,
    "structured_output": True,
    # ...
}
model = init_chat_model("...", profile=custom_profile)
```

LangChain的模型配置档案数据主要来自开源项目models.dev\
models.dev是一个专门维护模型能力信息的开源项目\
LangChain会在其数据基础上扩展额外字段，并与上游models.dev保持同步更新


模型配置档案的核心价值：让应用程序根据模型自身能力动态调整行为，无需写死代码
例如：
- 总结中间件可根据模型上下文窗口大小，自动判断是否需要总结\
  例如：上下文过长 → 自动压缩 / 总结
- 创建 Agent 时，可自动判断使用哪种结构化输出策略\
  例如：检查模型是否支持原生函数调用 / JSON 输出
- 可根据模型支持的输入类型（文本 / 图像）和最大 token 限制，自动过滤或截断输入
- Deep Agents CLI 会自动筛选出支持 tool_calling + 文本 I/O 的模型并在界面中显示上下文长度、能力标签等信息

