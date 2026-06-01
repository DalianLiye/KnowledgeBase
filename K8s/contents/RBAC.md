[目录](../目录.md)


# 关于RBAC
K8s的授权都是基于角色来进行控制访问的\
即RBAC， Role Based Access Control

RBAC相关对象主要包括:
- Role
- RoleBinding
- ClusterRole
- ClusterRoleBinding


# Role
Role代表角色，封装一组权限，属于命名空间级别资源，仅在单个命名空间内生效\
Role用于管控当前命名空间下的资源操作, 例如配置查看Pod、Deployment等权限

**注:**\
该资源需配合RoleBinding使用，才能将权限授予用户、用户组、ServiceAccount等主体

权限特点:
- 仅定义允许(Allow)规则，只罗列可执行的资源与操作
- 不支持拒绝(Deny)规则，无法配置禁止策略
- 遵循默认拒绝原则：未明确允许的操作，都会被拒绝

查看Role信息，执行命令：
```shell
kubectl get role -n <namespace> <role_name> -o yaml
```


# RoleBinding
用于将Role的权限绑定到自身所在命名空间下的主体（用户、用户组、ServiceAccount）\
作用域：命名空间\
它既可以绑定同命名空间下的Role，也可以绑定集群级的ClusterRole\
当绑定ClusterRole时，ClusterRole定义的权限仅在当前命名空间内生效，不会跨命名空间授权

**注:**
- 虽然绑定的是ClusterRole，但ClusterRole的权限也只会限定在当前命名空间内使用
- 绑定ClusterRole的目的，仅为复用ClusterRole的权限规则，不会改变RoleBinding命名空间级的属性

查看RoleBinding信息
```shell
kubectl get rolebinding -A
```

查看指定RoleBinding的配置信息
```shell
kubectl get rolebinding <role_binding_name> -A -o yaml
```


# ClusterRole
功能与Role类似，用于定义权限规则，需搭配ClusterRoleBinding完成权限绑定\
作用域：集群

查看Cluster_Role信息，执行命令：
```shell
kubectl get clusterrole <cluster_role_name> -o yaml
```


# ClusterRoleBinding
ClusterRoleBinding用于将集群级权限绑定到整个集群范围内的主体\
仅能绑定ClusterRole，对所有命名空间生效\
作用域：集群


# RoleBinding和ClusterRoleBinding比较
- **RoleBinding**
  - **作用范围**\
    RoleBinding所在命名空间
  - **绑定的角色**	
    - Role（命名空间角色）
    - ClusterRole（集群角色）
  - **绑定的对象**
    - User/Group（集群范围）
    - ServiceAccount（同一命名空间）
  - **权限生效范围**\
    RoleBinding所在命名空间
  - **使用场景**\
    给某个命名空间内的User或Service Account授权

- **ClusterRoleBinding**
  - **作用范围**\
    整个集群
  - **绑定的角色**	
    - ClusterRole（集群角色）
  - **绑定的对象**
    - User/Group（集群范围）
    - ServiceAccount（任一命名空间）
  - **权限生效范围**\
    整个集群
  - **使用场景**\
    给集群范围内的User、Group或某个命名空间的Service Account授权