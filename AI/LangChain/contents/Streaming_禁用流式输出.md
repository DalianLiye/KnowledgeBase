[目录](../目录.md)


# 禁用流式输出

在某些应用场景下，你可能需要为特定模型禁用单个 token 的流式输出。这在以下场景中非常有用：
- 处理多 agent 系统，控制哪些 agent 流式输出结果
- 混合使用支持流式和不支持流式的模型
- 部署到 LangSmith 时，希望防止某些模型的输出被流式传输到客户端

在初始化模型时设置 streaming=False 即可
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-5.4",
    streaming=False
)
```

提示：
部署到 LangSmith 时，对于不希望流式传输到客户端的模型，请设置 streaming=False。这需要在部署前的图代码中进行配置。

注意：
并非所有聊天模型集成都支持 streaming 参数。如果你的模型不支持，请改用 disable_streaming=True，该参数在所有聊天模型的基类中都可用。