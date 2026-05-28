[目录](../目录.md)


# 关于Deployment(Deploy)
对ReplicaSet进行高级封装，提供完整的应用生命周期管理能力，生产环境首选


# 核心功能
- **创建ReplicaSet/Pod**\
  创建Deployment时，会自动创建关联的ReplicaSet，并由ReplicaSet创建Pod

- **滚动升级/回滚**\
  修改镜像/配置后自动触发滚动更新，保证服务不间断、用户无感知

  ----------------------示例---------------------
  背景：当前Deployment对应ReplicaSet1, ReplicaSet1下包括Pod A和Pod B

  - **滚动升级**\
    当更新了Deployment里的Pod Template之后，会执行以下步骤执行滚动升级：

    1) Deployment创建ReplicaSet2，ReplicaSet2是空的，不包含任何Pod
    2) 在ReplicaSet2里，基于修改后的Pod Template创建Pod C
    3) 禁用ReplicaSet1的Pod A
    4) 在ReplicaSet2里，基于修改后的Pod Template创建Pod D
    5) 禁用ReplicaSet1的Pod B
    注：ReplicaSet1整体会被保留一段时间，不会立即删除，以备未来做回滚

  - **滚动回滚**\
    滚动升级后，执行kubectl rollout命令后，会按照以下步骤执行滚动回滚：

    1) 恢复ReplicaSet1的Pod A
    2) 禁用ReplicaSet2的Pod C
    3) 恢复ReplicaSet1的Pod B
    4) 禁用ReplicaSet2的Pod D
    注：ReplicaSet2不会被立即删除，它的replica数会变成0

- **平滑扩缩容**\
  通过kubectl scale命令实现，可作用于Deployment或ReplicaSet
  推荐对Deployment 操作，不建议直接操作ReplicaSet

- **暂停与恢复Deployment**\
  若需多次修改配置，可先暂停Deployment，避免频繁触发滚动更新
  修改完成后恢复，仅执行一次最终更新，减少不必要的版本切换

  若滚动更新过程中再次修改配置, 会执行以下操作：
  - 当前更新立即停止，已变更版本记入历史
  - 最新修改触发新一轮滚动更新