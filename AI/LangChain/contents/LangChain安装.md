[目录](../目录.md)

LangChain安装需要注意以下几点：
- 要求Python 3.10以及以上版本
- LangChain的各类模型集成（Integration）需要单独安装，例如与 OpenAI、Anthropic等大模型交互时，需额外安装对应的集成包

安装LangChain核心包
```shell
pip install -U langchain
```

安装OpenAI和Anthropic集成包
```shell
pip install -U langchain-openai
pip install -U langchain-anthropic
```



