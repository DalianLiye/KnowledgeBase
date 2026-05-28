[目录](../目录.md)


# 关于RBAC
全称：Role Based Access Control, RBAC

RBAC相关对象主要包括:
- Role
- RoleBinding
- ClusterRole
- ClusterRoleBinding


# Role
单个命名空间内的权限集合\
作用域：命名空间\
例如：可配置查看Pod、查看Deployment等权限，专门用于对当前命名空间内的资源做权限管控

**注:**
- 需配合RoleBinding使用，才能将权限授予用户、用户组、ServiceAccount等主体


# RoleBinding
用于将Role的权限绑定到自身所在命名空间下的主体（用户、用户组、ServiceAccount）\
作用域：命名空间\
它既可以绑定同命名空间下的Role，也可以绑定集群级的ClusterRole\
当绑定ClusterRole时，ClusterRole定义的权限仅在当前命名空间内生效，不会跨命名空间授权

**注:**
- 虽然绑定的是ClusterRole，但ClusterRole的权限也只会限定在当前命名空间内使用
- 绑定ClusterRole的目的，仅为复用ClusterRole的权限规则，不会改变RoleBinding命名空间级的属性


# ClusterRole
功能与Role类似，用于定义权限规则，需搭配ClusterRoleBinding完成权限绑定\
作用域：集群


# ClusterRoleBinding
ClusterRoleBinding用于将集群级权限绑定到整个集群范围内的主体\
仅能绑定ClusterRole，对所有命名空间生效\
作用域：集群



