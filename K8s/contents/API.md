[目录](../目录.md)


# API类型
- **Alpha**\
  尝鲜版本，内置最新功能，但稳定性差、可能存在缺陷，仅适用于短期测试与功能验证
- **Beta**\
  已完成充分测试，整体可用，但部分细节、接口仍可能调整变更
- **Stable**\
  正式稳定版本，可直接应用于生产环境


# 访问控制
通过图形界面（GUI）访问集群时，必须经过认证与授权两道校验


# 废弃api说明
K8s官方废弃API规则及迁移指南：\
https://kubernetes.io/zh-cn/docs/reference/using-api/deprecation-guide/


# Pod与集群
K8s API可对以下资源进行交互管理：
- 运行中的Pod
- 集群节点与整个集群


# 资源类型与别名
pods: po\
deployments: deploy\
services: svc\
namespace: ns\
nodes: no\
statefulset: sts\
daemonset: ds\
endpoints: ep\
configmap: cm


# 格式化输出
输出JSON格式	-o json\
仅打印资源名称	-o name\
纯文本展示完整信息（含扩展列）	-o wide\
输出yaml格式	-o yaml
