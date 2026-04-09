[目录](../目录.md)


# 关于模型调用
Chat Model提供三种核心调用方式：
- invoke
- stream
- batch


## invoke()
通过invoke()方法可以发送单条或一组消息给模型，等待全部生成完成后一次性返回结果

支持三种输入格式：
- 字符串（单条用户消息）
- 字典数组（对话历史）
- Message对象数组（SystemMessage / HumanMessage / AIMessage）


示例：发送字符串
```python
response = model.invoke("Why do parrots have colorful feathers?")
print(response)
```

示例：发送字典数组\
可以用来代表历史聊天记录\
每一个message都有一个role，模型可以用来判断是谁发出的
```python
conversation = [
    {"role": "system", "content": "You are a helpful assistant that translates English to French."},
    {"role": "user", "content": "Translate: I love programming."},
    {"role": "assistant", "content": "J'adore la programmation."},
    {"role": "user", "content": "Translate: I love building applications."}
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
```

示例：发送Message对象数组，通过Messge对象封装各个message
```python
from langchain.messages import HumanMessage, AIMessage, SystemMessage

conversation = [
    SystemMessage("You are a helpful assistant that translates English to French."),
    HumanMessage("Translate: I love programming."),
    AIMessage("J'adore la programmation."),
    HumanMessage("Translate: I love building applications.")
]

response = model.invoke(conversation)
print(response)  # AIMessage("J'adore créer des applications.")
```


## stream()
通过stream()方法可以实现流式逐块返回输出，无需等待全部生成，大幅提升长响应场景的用户体验\
返回迭代器，可实时展示、拼接片段


示例1：
```python
for chunk in model.stream("Why do parrots have colorful feathers?"):
    print(chunk.text, end="|", flush=True)
```

示例2：
```python
for chunk in model.stream("What color is the sky?"):
    for block in chunk.content_blocks:
        if block["type"] == "reasoning" and (reasoning := block.get("reasoning")):
            print(f"Reasoning: {reasoning}")
        elif block["type"] == "tool_call_chunk":
            print(f"Tool call chunk: {block}")
        elif block["type"] == "text":
            print(block["text"])
        else:
            ...
```

示例3: 可以将每一个输出chunk通过循环做累加，最后得到的是全部的输出
```python
full = None  # None | AIMessageChunk
for chunk in model.stream("What color is the sky?"):
    full = chunk if full is None else full + chunk
    print(full.text)

# The
# The sky
# The sky is
# The sky is typically
# The sky is typically blue
# ...

print(full.content_blocks)
# [{"type": "text", "text": "The sky is typically blue..."}]
```

从模型的输出结果上看，stream()和invoke()返回的结果是一样的，它们的结果都可以整合到message历史中，作为会话上下文再次给到模型\
只有当程序中的每一个处理步骤都能处理“分块流”（stream of chunks）时，流式处理（streaming）才有效\
也就是说要真正利用流式输出的好处，整个处理链路中的每一步都要能按片段增量处理数据\
只在部分环节支持流式而其他环节仍然要求完整数据，就无法充分利用streaming的优势


**Streaming Event**\
通过astream_events()方法可以流式处理语义事件(semantic events)

示例：
```python
async for event in model.astream_events("Hello"):

    if event["event"] == "on_chat_model_start":
        print(f"Input: {event['data']['input']}")

    elif event["event"] == "on_chat_model_stream":
        print(f"Token: {event['data']['chunk'].text}")

    elif event["event"] == "on_chat_model_end":
        print(f"Full message: {event['data']['output'].text}")

    else:
        pass
```

**Auto-Streaming**\
特定场景下，即使不显式调用stream()，LangChain也会自动开启流式处理，适合用invoke() 但仍想获取中间流式结果的场景

## batch()
通过batch()方法可以批量发送多条请求，利用模型并行处理能力，提升效率、降低成本\
注：batch()方法跟provider提供的原生batch API是不同的


示例1：\
batch()会在模型将批量发送请求都处理完后，再返回最终的输出
```python
responses = model.batch([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print(response)
```

示例2：\
batch_as_completed()可以实时返回每个请求的输出\
它返回每个请求的输出的顺序是随机的，如果要按照指定顺序输出，可以根据input index按照指定顺序输出
```python
for response in model.batch_as_completed([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
]):
    print(response)
```

不管是batch()还是batch_as_completed()，可以通过max_concurrency参数控制最大并发量，该参数所在类型为RunnableConfig
```python
model.batch(
    list_of_inputs,
    config={
        'max_concurrency': 5,  # Limit to 5 parallel calls
    }
)
```