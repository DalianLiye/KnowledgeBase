[目录](../目录.md)


# 关于对数概率

对数概率（log probabilities） 是模型生成文本时，对每个词元（token）输出的置信度指标\
它表示模型认为 “下一个词元是这个值” 的可能性大小
- 概率越高（越接近 0，比如 -0.1）:说明模型对这个词元越有把握\
- 概率越低（越负，比如 -5.0）:说明模型越不确定

部分模型可以通过在调用时设置logprobs参数，返回词元（token）级别的对数概率

```python
model = init_chat_model(
    model="gpt-4.1",
    model_provider="openai"
).bind(logprobs=True)

response = model.invoke("Why do parrots talk?")
print(response.response_metadata["logprobs"])
```