[目录](../目录.md)


# 关于Persistent Volume(PV)
PV即: 持久化卷\
PV是集群级存储资源，对NFS、云盘、iSCSI等底层存储进行统一抽象\
PV的作用是为整个集群提供可用的持久化存储载体

# 特点:
- 可由管理员手动创建，也可通过StorageClass动态自动创建
- 生命周期独立于Pod，不受Pod启停、删除影响
- 定义存储容量、访问模式（如 ReadWriteOnce、ReadOnlyMany、ReadWriteMany）、存储类型、回收策略等属性

**注：**\
PV是集群级资源