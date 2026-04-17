[目录](../目录.md)


# 关于推理
许多大模型都具备多步推理（reasoning）能力，可以将复杂问题拆解为更小、更易处理的步骤，最终得出结论

不是所有模型都支持返回推理过程，只有专门的推理模型（如 DeepSeek Reasoner、OpenAI o1）才支持\
LangChain会把模型的思考步骤以结构化内容块的形式返回，从而更好地理解模型是如何得出最终答案的，让开发者能拿到、能分析、能调试


示例1：流式输出推理过程
```python
for chunk in model.stream("Why do parrots have colorful feathers?"):
    reasoning_steps = [r for r in chunk.content_blocks if r["type"] == "reasoning"]
    print(reasoning_steps if reasoning_steps else chunk.text)
```

示例2：全量输出推理过程
```python
response = model.invoke("Why do parrots have colorful feathers?")
reasoning_steps = [b for b in response.content_blocks if b["type"] == "reasoning"]
print(" ".join(step["reasoning"] for step in reasoning_steps))
```

**控制Reasoning强度**\
根据模型的不同，有时可以指定模型在推理上投入的努力程度，也可以要求模型完全关闭推理功能

控制方式通常有两种：
- **分类式推理层级**\
  例如 low 低强度 / high 高强度
- **整数型Token预算**\
  限制推理最多用多少Token