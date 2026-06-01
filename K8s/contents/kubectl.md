[目录](../目录.md)


# 关于kubectl
kubectl是K8s官方提供的命令行工具，通过调用K8s API与集群控制平面交互，完成集群、资源的各类管理操作\
官方命令参考文档：\
URL：https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands


# 资源操作
kubectl核心用法围绕集群资源展开，常用操作分类如下:
- 创建资源对象
- 查看、检索资源
- 更新资源配置
- 补丁修改资源
- 在线编辑资源
- 弹性扩缩容（scale）
- 删除资源

注：如需查看命令详情，可使用帮助指令
```shell
kubectl 子命令 --help
```
