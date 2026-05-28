[目录](../目录.md)


# 关于Storage类资源
Storage类资源，主要包括:
- CSIDriver
- CSINode
- CSIStorageCapacity
- StorageClass
- VolumeAttachment
- VolumeAttributesClass


# CSI
关于容器存储接口
英文全称： Container Storage Interface，CSI\
它由Kubernetes、Mesos、Docker等容器社区联合制定的一套行业标准接口规范\
用于让各类存储系统能够对接容器化应用

CSI规范明确了存储厂商开发兼容型卷插件（Volume Plugin）所需实现的最小操作集合与部署要求\
CSI规范的核心是定义卷插件所必须遵循的标准接口

**注：**\
- CSI本身是接口规范，并非K8s标准API资源
- 实现CSI规范的组件(CSI驱动、CSI控制器、节点服务、CSIDriver、CSINode等)，均为集群级资源