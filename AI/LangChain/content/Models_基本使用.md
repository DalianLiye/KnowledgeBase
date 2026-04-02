# 基本使用
Model可以通过以下两种方式使用：
- With agent\
  可以在创建agent时动态指定model\
  model可以在复杂的“基于 agent 的工作流”中调用

- Standalone\
  可以直接单次调用model，无需agent framework做循环处理\
  例如直接生成文本、做分类或抽取信息


# 初始化model
通过以下两种方式初始化model：
- chat model class\
  如果要初始化一个standalone model，通过init_chat_model方式最简单，最直接
- provider model class
  
示例：langchain提供的标准接口初始化model
```python
import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-5.2")

response = model.invoke("Why do parrots talk?")
```

示例：通过provider提供的原生方式初始化model
```python
import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-5.2")

response = model.invoke("Why do parrots talk?")
```

# 支持的Model
Langchain支持所有当前主流的provider的model\
每个provider提供的model的能力也各不相同

# Key Method
model主要包括以下关键的方法：

- invoke\
  向model提交message作为输入，然后生成response后返回输出

- stream\
  调用model时，实时返回正在生成的结果

- batch\
  同时向model批量发送多个请求，这样可以提高处理效率

除了聊天（对话）模型之外，LangChain 还支持其它相关技术\
例如用于生成向量表示的 embedding 模型和用于存储与检索这些向量的向量数据库（vector store）