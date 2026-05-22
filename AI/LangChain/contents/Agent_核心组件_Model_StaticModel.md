[目录](../目录.md)

# 关于静态选择模型
静态选择模型就是创建Agent时选定模型后，该模型在Agent整个生命周期内都不会改变，该方式最普遍，最直接


# 示例

- 示例1：默认配置
  ```python
  from langchain.agents import create_agent
  from dotenv import load_dotenv
  load_dotenv()   

  tools = [] 

  agent = create_agent("openai:gpt-5", tools=tools)
  ```
  说明: \
  指定模型时，其格式为：<model_name> 或者 <provider_name>:<model_name>\
  单独写<model_name>，langchain会自动分析出对应的提供商


- 示例2：更细粒度配置
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
  说明：\
  如果对模型有更细粒度的控制，可直接通过provider package创建Agent实例\
  不同provider会有不同的配置\
  所谓的provider package，其实就是安装的integration，比如langchain_openai