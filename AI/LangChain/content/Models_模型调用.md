# 关于模型调用
chat model的调用有以下几种方法：
- invoke
- stream
- batch


## invoke()
可以通过invoke()方法发送一个或一组message到模型，然后模型将所有结果一次性全部输出返回

示例：发送一个message
```python
response = model.invoke("Why do parrots have colorful feathers?")
print(response)
```

示例：发送一组message，可以用来代表历史聊天记录\
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

示例：发送一组message，可以通过Messge对象封装各个message
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
大部分模型都支持stream输出，提升用户体验，特别是响应时间较长的请求\
调用 stream() 会返回一个迭代器，它会在输出生成时逐块返回，可以使用循环实时处理每个块

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
通过astream_events()流式处理语义事件(semantic events)

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
在某些特定的场景下，即便没有显式的执行stream，但langchain也会自动进行streaming\
当使用invoke()进行非流式处理，但仍然希望流式处理整个应用程序时，包括来自聊天模型的中间结果时，这尤其有用



## batch()
由于模型可以并行处理请求，可以将各请求批量发送给模型，会显著提高性能和降低成本\
可以通过batch()方法实现这样的批量操作\
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