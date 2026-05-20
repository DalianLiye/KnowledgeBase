[目录](../目录.md)


# 使用短期记忆

为Agent添加短期记忆（线程级对话记忆），只需在创建Agent时指定一个checkpointer\
LangChain Agent会将短期记忆作为状态（state）的一部分自动管理：
- Agent 通过图状态存储对话上下文
- 不同线程（thread）之间的记忆完全隔离
- 状态会通过 checkpointer 自动持久化到内存或数据库
- 线程可随时暂停、恢复、继续对话
- 短期记忆会在 Agent 调用或步骤（如工具调用）完成时自动更新
- 每个步骤开始时会自动读取最新状态


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
生产环境推荐使用数据库持久化的checkpointer，确保记忆不会丢失
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