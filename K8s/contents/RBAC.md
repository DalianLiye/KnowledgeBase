[目录](../目录.md)


## 授权
k8s的授权都是基于角色来进行控制访问的\
即RBAC， Role Based Access Control



# 关于RBAC
全称：Role Based Access Control

RBAC相关对象主要包括:
- Role
- RoleBinding
- ClusterRole
- ClusterRoleBinding


### Role
Role代表了一个角色，它包含了一组权限

关于Role包含的权限，有以下特点:
- 只定义允许(Allow)规则，即明确列出哪些资源和操作是被允许的
- 不定义拒绝(Deny)规则，即没有类似“禁止”或“拒绝”的规则
- 默认拒绝：如果某个操作没有被明确允许，则该操作就会被拒绝

Role是namespace级别的资源，只能作用与namespace之内

查看Role信息，执行命令：
```shell
kubectl get role -n <namespace> <role_name> -o yaml
```

### ClusterRole
功能与Role一样，区别是资源类型为集群类型，而Role只作用在Namespace

查看Cluster_Role信息，执行命令：
```shell
kubectl get clusterrole <cluster_role_name> -o yaml
```




# Role
单个命名空间内的权限集合\
作用域：命名空间\
例如：可配置查看Pod、查看Deployment等权限，专门用于对当前命名空间内的资源做权限管控

**注:**
需配合RoleBinding使用，才能将权限授予用户、用户组、ServiceAccount等主体


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



### RoleBinding
Role只是用于指定权限集合，具体作用与什么对象上，需要使用RoleBinding来进行绑定\
RoleBinding是命名空间级别资源，可以将Role或ClusterRole绑定到集群的User和Group上，或者某个命名空间的Service Account上

查看RoleBinding信息
```shell
kubectl get rolebinding -A
```

查看指定RoleBinding的配置信息
```shell
kubectl get rolebinding <role_binding_name> -A -o yaml
```

### ClusterRoleBinding
ClusterRoleBinding是集群级别资源\
ClusterRoleBinding的功能与RoleBinding一样，只是作用的对象是集群级别的资源




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