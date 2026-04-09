[目录](../目录.md)


# 工具和工具调用
模型可根据需求主动请求调用工具，典型场景包括：
- 数据库查询
- 联网搜索
- 代码执行

工具由两部分组成
- **接口定义**\
  工具名、描述、参数结构（通常为 JSON Schema）
- **执行逻辑**\
  同步函数或异步协程
  
工具调用本质可理解为模型驱动的函数调用

以下是用户和模型之间，基本的工具调用流程示例：
![Models](./img/models001.png)

通过bind_tools()将工具与模型绑定，模型即可在推理中自主选择调用\
部分厂商提供内置工具直接使用

```python
from langchain.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."


model_with_tools = model.bind_tools([get_weather])

response = model_with_tools.invoke("What's the weather like in Boston?")
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")
```

模型绑定用户自定义工具后，模型的响应会包含工具调用请求
- **直接使用模型：**\
  需用户手动执行工具并将结果回传模型
- **使用Agent：**\
  agent会循环自动处理工具执行与多轮交互


# 常见工具调用方式

- **工具执行循环**\
  **工具执行循环流程：**\
  模型发起工具调用 → 执行工具 → 将结果以ToolMessage回传 → 模型继续推理生成最终回答\
  每条ToolMessage携带 tool_call_id，用于关联请求与结果

  ```python
  # Bind (potentially multiple) tools to the model
  model_with_tools = model.bind_tools([get_weather])

  # Step 1: Model generates tool calls
  messages = [{"role": "user", "content": "What's the weather in Boston?"}]
  ai_msg = model_with_tools.invoke(messages)
  messages.append(ai_msg)

  # Step 2: Execute tools and collect results
  for tool_call in ai_msg.tool_calls:
      # Execute the tool with the generated arguments
      tool_result = get_weather.invoke(tool_call)
      messages.append(tool_result)

  # Step 3: Pass results back to model for final response
  final_response = model_with_tools.invoke(messages)
  print(final_response.text)
  # "The current weather in Boston is 72°F and sunny."
  ```


- **强制工具调用(Forcing tool calls)**\
  默认情况下，模型可自主判断是否调用工具，但也可通过tool_choice强制模型使用特定工具

  示例：允许模型使用任何工具
  ```python
  model_with_tools = model.bind_tools([tool_1], tool_choice="any")
  ```

  示例：强制模型使用特定工具
  ```python
  model_with_tools = model.bind_tools([tool_1], tool_choice="tool_1")
  ```

- **并行工具调用**\
  多数模型支持同时调用多个工具，提升信息获取效率\
  模型会自动判断任务是否可并行
  比如, 查询A和B两个城市的天气，模型会同时调用工具获取A和B城市天气(并行)\
  查询经纬度地区的天气，模型会先查询经纬度所在城市，再通过城市查看天气(串行)


  示例：
  ```python
  model_with_tools = model.bind_tools([get_weather])

  response = model_with_tools.invoke(
      "What's the weather in Boston and Tokyo?"
  )


  # The model may generate multiple tool calls
  print(response.tool_calls)
  # [
  #   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
  #   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
  # ]


  # Execute all tools (can be done in parallel with async)
  results = []
  for tool_call in response.tool_calls:
      if tool_call['name'] == 'get_weather':
          result = get_weather.invoke(tool_call)
      ...
      results.append(result)
  ```

  一些模型是可以关闭并行特性
  
  示例：
  ```python
  model.bind_tools([get_weather], parallel_tool_calls=False)
  ```

- **流式工具调用**\
  当流式处理模型的响应输出时，工具调用会通过ToolCallChunk逐步构建\
  这样就可以看到工具调用的整个过程，而不用等待到整个响应结束

  示例1: 
  ```python
  for chunk in model_with_tools.stream(
      "What's the weather in Boston and Tokyo?"
  ):
      # Tool call chunks arrive progressively
      for tool_chunk in chunk.tool_call_chunks:
          if name := tool_chunk.get("name"):
              print(f"Tool: {name}")
          if id_ := tool_chunk.get("id"):
              print(f"ID: {id_}")
          if args := tool_chunk.get("args"):
              print(f"Args: {args}")

  # Output:
  # Tool: get_weather
  # ID: call_SvMlU1TVIZugrFLckFE2ceRE
  # Args: {"lo
  # Args: catio
  # Args: n": "B
  # Args: osto
  # Args: n"}
  # Tool: get_weather
  # ID: call_QMZdy6qInx13oWKE7KhuhOLR
  # Args: {"lo
  # Args: catio
  # Args: n": "T
  # Args: okyo
  # Args: "}
  ```

  示例2：将每次返回的chunk拼接在一起后，再输出
  ```python
  gathered = None
  for chunk in model_with_tools.stream("What's the weather in Boston?"):
      gathered = chunk if gathered is None else gathered + chunk
      print(gathered.tool_calls)]
  ```