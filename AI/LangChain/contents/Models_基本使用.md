[目录](../目录.md)


# 基本使用
Model可以通过以下两种方式使用：
- **With agent**\
  创建Agent时动态指定Model，Model可在复杂的Agent工作流中被调用

- **Standalone**\
  直接单次调用Model，无需Agent框架的循环处理，适用于生成文本、分类、信息抽取等场景


# 初始化model

两种方式：
- **chat model class**\
  初始化Standalone Model最简单直接的方式：使用 init_chat_model
- **provider model class**\
  使用各厂商提供的原生Model类

示例：使用LangChain标准接口初始化Model
```python
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.2")

response = model.invoke("Why do parrots talk?")
```

示例：通过Provider原生方式初始化Model
```python
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.2")

response = model.invoke("Why do parrots talk?")
```

# 支持的Model
LangChain支持当前所有主流厂商模型，不同厂商提供的模型能力各有差异


# 核心方法
Model包含以下核心方法：

- **invoke**\
  提交消息输入，等待生成完成后返回完整响应

- **stream**\
  调用model时，实时流式返回响应内容

- **batch**\
  同时向model批量发送多个请求，提升处理效率

除聊天模型外，LangChain 还支持相关技术体系\
例如：用于生成向量表示的Embedding模型，以及用于存储和检索向量的向量数据库（Vector Store）

