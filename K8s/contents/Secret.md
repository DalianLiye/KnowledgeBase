[目录](../目录.md)


# 关于Secret
功能用法与ConfigMap相近，专门用于存储密码、令牌、密钥等敏感数据\
数据会以编码形式存储，避免明文暴露，防止敏感信息泄露\
使用时可挂载或注入到Pod中，无需将敏感数据直接写入镜像或Pod配置清单

**注：**\
Secret仅做Base64 编码（非强加密），生产环境可配合权限策略进一步加固安全

使用方式：
- Volume挂载
- 环境变量注入

Secret类型:
- **Service Account**\
  用于Pod访问K8s API的身份凭证，由集群自动创建，会自动挂载到Pod内路径：/run/secrets/kubernetes.io/serviceaccount

- **Opaque**\
  默认数据以Base64编码存储，常用于存放密码、密钥等敏感数据\
  注：Base64仅为编码方式，并非加密，可逆向解码还原原始数据

- **kubernetes.io/dockerconfigjson**\
  专门存储私有镜像仓库的登录认证信息，用于拉取私有镜像