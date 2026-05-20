[目录](../目录.md)


# 关于流式输出
LangChain内置完整的流式输出体系，用于实时推送运行动态\
流式输出对于提升基于大模型的应用的响应速度至关重要\
在完整响应生成前，通过逐步展示输出，能显著改善用户体验（UX），尤其是在处理 LLM 的延迟问题时

LangChain的流式系统让你可以将 agent 运行的实时反馈传递到应用中
使用LangChain流式输出可以实现：
- **Stream agent progress（agent 进度流）**\
  每完成一个执行步骤，实时获取状态变更信息
- **Stream LLM tokens（LLM token 流）**\
  跟随模型生成节奏，逐字流式输出文本内容
- **Stream thinking / reasoning tokens（思考 / 推理 token 流）**\
  实时展示模型思考与逻辑推导过程
- **Stream custom updates（自定义更新流）**\
  按需推送自定义业务状态提示，如数据拉取进度、任务节点提示, 发出用户定义的信号（例如：“已获取 10/100 条记录”）
- **Stream multiple modes（多种模式流）**\
  灵活组合使用多种流式模式，可选择updates（agent 进度）、messages（LLM token + 元数据）或 custom（任意用户数据）模式