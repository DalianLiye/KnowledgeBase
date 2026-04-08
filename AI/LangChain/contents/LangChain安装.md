[目录](../目录.md)

LangChain安装需要注意以下几点：
- 要求Python 3.10以及以上版本
- LangChain的Integration需要额外单独安装，比如如果想要agent跟OpenAI相关的LLM交互，还需要额外安装langchain-openai这个integration

安装LangChain
```shell
pip install -U langchain
```

安装OpenAI integration和Anthropic integration
```shell
pip install -U langchain-openai
pip install -U langchain-anthropic
```



