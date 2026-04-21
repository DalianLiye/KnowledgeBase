[目录](../目录.md)


# 关于流式输出

LangChain实现了一套流式输出系统，用于提供实时更新

流式输出对于提升基于大模型的应用的响应速度至关重要

在完整响应生成前，通过逐步展示输出，能显著改善用户体验（UX），尤其是在处理 LLM 的延迟问题时

LangChain的流式系统让你可以将 agent 运行的实时反馈传递到应用中
使用 LangChain 流式输出可以实现：
- Stream agent progress（agent 进度流）
  在每个 agent 步骤后获取状态更新。
- Stream LLM tokens（LLM token 流）
  在语言模型生成 token 时进行流式输出。
- Stream thinking / reasoning tokens（思考 / 推理 token 流）
  在模型生成过程中展示其推理过程。
- Stream custom updates（自定义更新流）
  发出用户定义的信号（例如：“已获取 10/100 条记录”）。
- Stream multiple modes（多种模式流）
  可选择 updates（agent 进度）、messages（LLM token + 元数据）或 custom（任意用户数据）模式。
