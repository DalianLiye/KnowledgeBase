[目录](../目录.md)


# 关于kubectl
kubectl是K8s官方提供的命令行工具\
kubectl通过调用K8s API与集群控制平面交互，完成集群、资源的各类管理操作\
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


# 常用命令

```shell
kubectl 子命令 --help
```

**格式化输出**
| **格式化输出参数** |              **说明**              |
|:----------:|:------------------------------:|
|  -o json   |          输出JSON格式          |
|  -o name   |         仅打印资源名称         |
|  -o wide   | 纯文本展示完整信息（含扩展列） |
|  -o yaml   |          输出yaml格式          |
