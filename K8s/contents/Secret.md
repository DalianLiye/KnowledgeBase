[目录](../目录.md)


# 关于Secret
功能用法与ConfigMap相近，专门用于存储密码、令牌、密钥等敏感数据\
数据会以编码形式存储，避免明文暴露，防止敏感信息泄露\
使用时可挂载或注入到Pod中，无需将敏感数据直接写入镜像或Pod配置清单

**注：**\
- Secret仅做Base64 编码（非强加密），生产环境可配合权限策略进一步加固安全
- 在创建secret时，要注意如果要加密的字符中，包含了有特殊字符，需要使用转义字符转义\
  例如,"$"需要写成"\$", 也可以对特殊字符使用单引号描述，这样就不需要转义了\
  例如, 1$289*-! 可以写成'1$289*-!'


使用方式：
- Volume挂载
- 环境变量注入

# Secret类型
secret类型包括：
- **Service Account**\
  用于Pod访问K8s API的身份凭证，由集群自动创建，会自动挂载到Pod内路径：/run/secrets/kubernetes.io/serviceaccount

- **Opaque**\
  默认数据以Base64编码存储，常用于存放密码、密钥等敏感数据\
  注：Base64仅为编码方式，并非加密，可逆向解码还原原始数据

- **kubernetes.io/dockerconfigjson**\
  专门存储私有镜像仓库的登录认证信息，用于拉取私有镜像


# 示例
通过literal方式创建generic secret, 执行命令：
```shell
kubectl create secret generic orig-secret --from-literal=username=admin --from-literal=password='1$289*-!' # password如果不进行转义或单引号括起来，secret虽然创建成功，但其实password的值是有缺失的
```

创建docker-registry secret，执行命令：
```shell
kubectl create secret docker-registry <name> --docker-username=<username> --docker-password=<password> --docker-email=<email address> [--docker-server=<server>]
```

查看docker-registry secret的详细信息，执行命令：
```shell
kubectl eidt secret <secret_name> 

# 将.dockerconfigjson的value解码，就可以看到明文
echo <.dockerconfigjson string> | base64 -d
```

执行kubectl create命令创建如下Pod，文件名：private-image-pull-pod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: private-image-pull-pod
spec:
  imagePullSecrets: # 配置登录docker registry
  - name: harbor-secret  # 设置secret name，用这个secret的credentials信息登录镜像私有库
  containers:
  - name: nginx
    image: 192.168.113.122:8858/opensource/nginx:1.9.1  # 镜像位于私有仓库,且本地不存在
    command: ["/bin/sh","-c", "sleep 3600"]
    imagePullPolicy: IfNotPresent
    env:
    - name: JAVA_VM_OPTS
      valueFrom: 
        configMapKeyRef:
          name: test-env-config
          key: JAVA_OPTS_TEST     
     - name: APP
       valueFrom:
         configMapKeyRef:
           name: test-env-config
           key: APP_NAME
    volumeMounts:  # 加载数据卷
    - name: db-config  
      mountPath: "/usr/local/mysql/conf"  
      readOnly: true  # 是否只读
  volumes:  #数据卷挂载， configMap，sercret
    - name: db-config  # 数据卷的名字，名字可以自定义
      configMap: #数据卷类型为configMap
        name: test-dir-config  
        items:  
        - key: "db.properties"  # configmap中的key
          path: "db.properties"  # 将该key中的值转换为文件
  restartPolicy: Never
```
注：额外配置.sepc.imagePullSecrets


# 不可变secret
对于一些敏感服务的配置文件，在线上有时是不允许修改的\
此时在配置secret时可以设置immutable：true来禁止修改