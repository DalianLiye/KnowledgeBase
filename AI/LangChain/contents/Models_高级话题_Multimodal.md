[目录](../目录.md)


# 关于Multimodal
有些模型既可以处理文本数据，也可以处理非文本数据（如图像、音频、视频）\
多模态(Multimodal)，就是指能处理/生成 文本 + 图像 + 音频 + 视频等多种类型数据的模型


# 关于内容块
向模型传非文本数据时，不能直接传文件，需要将数据封装到内容块（content blocks），LangChain才能统一处理\
内容块就是LangChain用来封装多模态数据的结构化单元

当模型生成多模态内容时，返回的AIMessage对象会包含多模态类型的内容块\
即模型生成的多模态数据，会被封装成content_blocks列表，存在返回的AIMessage里\
然后就可以从response.content_blocks里拿到文本、图片等所有类型的结果

内容块使用场景：
- **纯文本**\
  直接传字符串 (str)，LangChain自动打包，无需内容块
- **非文本（图像 / 音频）**\
  必须放进内容块里
- **混合输入（纯文本 + 非文本）**\
  必须用内容块列表
- **多模态输出**\
  结果都在AIMessage.content_blocks里

示例：
```python
# 调用模型生成一张猫的图片
response = model.invoke("Create a picture of a cat")
# 打印内容块列表
print(response.content_blocks)
# [
#     {"type": "text", "text": "Here's a picture of a cat"},
#     {"type": "image", "base64": "...", "mime_type": "image/jpeg"},
# ]
```

# Multimodal输入格式
所有具备多模态能力的LangChain chat model，都支持以下输入格式：
- 跨提供商标准格式（LangChain 统一的消息格式）
- OpenAI聊天补全格式（OpenAI 原生的多轮对话格式）
- 模型提供商原生格式（例如 Anthropic 模型支持 Anthropic 原生格式）

**LangChain做了格式兼容层:**\
无论用OpenAI、Anthropic还是其他多模态模型，都能用LangChain统一的标准格式传数据\
同时兼容厂商原生格式，无需修改代码即可切换模型\
核心价值：一次编码，多模型兼容


