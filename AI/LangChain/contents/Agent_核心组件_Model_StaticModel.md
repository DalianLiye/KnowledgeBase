[目录](../目录.md)

# 关于Static Model
Static model就是创建Agent时指定model后，该model在agent整个生命周期内都不会改变\
Static model是最普遍，最直接的一种指定model的方式


# 示例

示例：
```python
from langchain.agents import create_agent
from dotenv import load_dotenv
load_dotenv()   

tools = [] 

agent = create_agent("openai:gpt-5", tools=tools)
```
注: \
model name的格式为：<model_name> 或者 <provider_name>:<model_name>\
单独写<model_name>，langchain会自动分析出对应的provider


示例2：\
如果想对model的配置有更细粒度的控制，可以直接通过provider package创建agent\
这些更细粒度的配置，会根据provider的不同而不同\
这个provider package就是安装的integration，比如langchain_openai
```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv  
load_dotenv()    

model = ChatOpenAI(
    model="gpt-5",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
    # ... (other params)
)

tools=[]

agent = create_agent(model, tools=tools)
```