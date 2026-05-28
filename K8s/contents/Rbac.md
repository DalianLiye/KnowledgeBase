[目录](../目录.md)


# 关于Rbac类资源
Rbac类(鉴权类)资源，主要包括:
- Role
- RoleBinding
- ClusterRole
- ClusterRoleBinding


# Role
定义单个命名空间内的权限集合\
作用域：命名空间\
例如：可配置查看Pod、查看Deployment等权限，专门用于对当前命名空间内的资源做权限管控

**注:**
- 需配合RoleBinding使用，才能将权限授予用户、用户组、ServiceAccount等主体


# RoleBinding
RoleBinding用于将权限规则绑定到自身所在命名空间下的主体（用户、用户组、ServiceAccount）\
作用域：命名空间\
它既可以绑定同命名空间下的Role，也可以绑定集群级的ClusterRole\
当绑定ClusterRole时，权限仅在当前命名空间内生效，不会跨命名空间授权

**注:**
- 即便绑定集群级ClusterRole，对应的权限也只会限定在当前命名空间内使用
- 绑定ClusterRole的目的，仅为复用ClusterRole的权限规则，不会改变RoleBinding命名空间级的属性


# ClusterRole
功能与Role类似，用于定义权限规则，作用域为整个集群，需搭配ClusterRoleBinding完成权限绑定\
作用域：集群


# ClusterRoleBinding
ClusterRoleBinding用于将集群级权限绑定到整个集群范围内的主体\
仅能绑定ClusterRole，权限作用域覆盖整个集群，对所有命名空间生效\
作用域：集群



