[目录](../目录.md)


# 关于配置资源
配置资源，主要包括：
- ConfigMap
- Secret
- Downward API

注：Downward API不是独立的顶级资源（无单独 Kind），是依托Pod配置实现的功能，它依附Pod存在，归属命名空间级，功能上归为配置类

# ConfigMap
用于存储键值（key-value）格式的非敏感配置数据，可被挂载或注入到Pod中，供容器读取使用\
ConfigMap可集中统一管理应用配置，多个Pod/容器可共用同一份配置，避免逐个单独维护，提升配置管理效率

**注：**\
由于ConfigMap采用的是普通明文配置，敏感数据建议使用Secret

# Secret
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



