[目录](../目录.md)


# 使用短期记忆
要为agent添加短期记忆（线程级持久化），需要在创建agent时指定一个checkpointer

LangChain的agent将短期记忆作为其状态的一部分进行管理\
Agent通过将这些信息存储在图状态中，既可以访问特定对话的完整上下文，又能保持不同线程之间的隔离\
状态会通过检查点器持久化到数据库（或内存）中，因此线程可以随时恢复\
短期记忆会在Agent被调用或一个步骤（如工具调用）完成时更新，并且状态会在每个步骤开始时被读取。

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  


agent = create_agent(
    "gpt-5",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}},
)
```

**生产环境用法**\
在生产环境中，应使用由数据库支持的checkpointer

```shell
pip install langgraph-checkpoint-postgres
```

```python
from langchain.agents import create_agent

from langgraph.checkpoint.postgres import PostgresSaver  


DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
    checkpointer.setup() # auto create tables in PostgreSQL
    agent = create_agent(
        "gpt-5",
        tools=[get_user_info],
        checkpointer=checkpointer,
    )
```