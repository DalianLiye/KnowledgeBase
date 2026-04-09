[目录](../目录.md)

# 关于Agent
Agent可以让Model和Tool结合，这样Model就可以分析task，调用合适的Tool，然后再利用Tool的结果反馈给Model再次分析\
这样不断的循环，最后达成最终的解决方案

当达到某个指定条件，或者循环达到上限，循环就会断开，并返回最终结果\
![agent](./img/agent001.png)


# Agent创建
通过create_agent函数，可以创建一个可发布生产的agent\
create_agent函数创建agent时，langchain内部会通过LangGraph把一个agent的执行过程搭建成“节点 + 边”的有向图（graph），构建出了一个基于图结构的Agent运行时系统


# 示例
示例1：openai
```python
from langchain.agents import create_agent
from dotenv import load_dotenv  
load_dotenv()                  

tools = []  # 你的工具
agent = create_agent("openai:gpt-5", tools=tools)
```

示例2：deepseek
```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
load_dotenv()                   
import os

# DeepSeek
llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"), # 如果.env文件里已经有DEEPSEEK_API_KEY这个变量，那么这行代码可以不写
    base_url="https://api.deepseek.com/v1"
)

tools = []  # 你的工具
agent = create_agent(llm, tools=tools)
```


