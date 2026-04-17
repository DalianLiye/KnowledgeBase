[目录](../目录.md)


# 关于限流

限流也叫速率限制（rate limiting）\
许多聊天模型服务商，都会对单位时间内可发起的调用次数设置上限\
一旦触发了限流，通常会收到服务商返回的限流错误响应，并且必须等待一段时间后才能继续发送请求\
比如：
- 每分钟最多调用 100 次（RPM）
- 每分钟最多消耗 10 万 Token（TPM）\

超过上限，服务商会直接拒绝请求，返回 429 Too Many Requests 错误


**限流作用**\
防止滥用、控制成本和负载


**管理限流**\
LangChain的聊天模型集成支持rate_limiter参数\
可以在初始化模型时传入，自动控制请求的发送速率

LangChain自带了一个可选的内置限流器：InMemoryRateLimiter\
这个限流器是线程安全的，可以被同一进程内的多个线程共享使用


# 示例

```python
from langchain_core.rate_limiters import InMemoryRateLimiter

rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.1,  # 1 request every 10s
    check_every_n_seconds=0.1,  # Check every 100ms whether allowed to make a request
    max_bucket_size=10,  # Controls the maximum burst size.
)

model = init_chat_model(
    model="gpt-5",
    model_provider="openai",
    rate_limiter=rate_limiter  
)
```
注：\
当前提供的限流器 只能限制「单位时间内的请求次数」\
如果需要基于请求大小（如 Token 数量）进行限流，它无法实现