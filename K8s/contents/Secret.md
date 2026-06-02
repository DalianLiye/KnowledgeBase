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


# Secret类型
secret类型包括：
- **Service Account**\
  用于Pod访问K8s API的身份凭证，由集群自动创建，会自动挂载到Pod内路径：/run/secrets/kubernetes.io/serviceaccount

- **Opaque**\
  默认数据以Base64编码存储，常用于存放密码、密钥等敏感数据\
  注：Base64仅为编码方式，并非加密，可逆向解码还原原始数据

- **kubernetes.io/dockerconfigjson**\
  专门存储私有镜像仓库的登录认证信息，用于拉取私有镜像


# Secret创建
跟ConfigMap一样，Secret创建方式主要包括：
- 基于文件夹
- 基于文件(推荐)
- 直接指定key-value

## 基于文件夹
```shell
kubectl create secret generic <secret_name> --from-file=<path_to_folder>
```

## 基于文件
```shell
kubectl create secret generic <secret_name> --from-file=<path_to_file>

kubectl create secret generic <secret_name> --from-file=app.yml=test.yaml
```

## 直接指定key-value
```shell
kubectl create secret generic <secret_name> --from-literal=k1=v1 --from-literal=k2=v2...  # Secret
```


# Secret使用
跟ConfigMap基本一样，Secret使用方式主要包括：
- 环境变量注入
- Volume整目录挂载
- 单文件挂载(使用subPath)
- 镜像拉取（secret专属）

## 环境变量注入
环境变量注入就是将Secret中的键值对直接转为容器内的环境变量

**示例:**\
创建一个存放账号密码的Secret
```shell
kubectl create secret generic user-secret \
  --from-literal=username=root \
  --from-literal=password=Admin@123456
```

定义Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-env-pod
spec:
  containers:
  - name: secret-test
    image: alpine
    command: ["/bin/sh","-c","env; sleep 3600"]
    imagePullPolicy: IfNotPresent

    # 👇 👇 这里就是 环境变量注入 Secret
    env:
    - name: DB_USER
      valueFrom:
        secretKeyRef:        # 关键：从 Secret 取值
          name: user-secret  # 你的 Secret 名称
          key: username      # Secret 里的 key

    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: user-secret
          key: password

  restartPolicy: Never
```


## Volume整目录挂载
Volume整目录挂载就是将整个Secret挂载为容器内的一个目录\
目录下一个key一个文件，文件内容为key的value值

**示例:**\
创建一个存放账号密码的Secret
```shell
kubectl create secret generic db-secret \
  --from-literal=username=root \
  --from-literal=password=Admin@123456
```

定义Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-volume-pod
spec:
  containers:
  - name: secret-test
    image: alpine
    command: ["/bin/sh","-c","sleep 3600"]
    imagePullPolicy: IfNotPresent

    # 挂载 Secret 到容器目录
    volumeMounts:
    - name: secret-volume      # 卷名称（要和下面对应）
      mountPath: "/etc/secrets"  # 容器内的目录
      readOnly: true

  # 定义数据卷：类型是 secret
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret  # 你要挂载的 Secret 名称

  restartPolicy: Never
```
容器内/etc/secrets路径下会有两个文件，一个是username，一个password，每个文件里的内容分别是root和Admin@123456


## 单文件挂载
单文件挂载就是只挂载Secret中的某一个key作为单个文件

**注:**\
不支持将将整个secret的内容挂载到一个单个文件,只能一个key一个文件

**示例:**\
创建Secret（含多个 key）
```shell
kubectl create secret generic db-secret \
  --from-literal=username=root \
  --from-literal=password=Admin@123456 \
  --from-literal=host=mysql-service
```

定义Pod
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: secret-subpath-pod
spec:
  containers:
  - name: secret-test
    image: alpine
    command: ["/bin/sh","-c","sleep 3600"]
    imagePullPolicy: IfNotPresent

    # 挂载单个文件：只挂 password
    volumeMounts:
    - name: secret-volume
      # 容器内最终的文件路径（必须是文件，不是目录）
      mountPath: "/tmp/my-password.txt"
      # 要挂载的 Secret 里的 key
      subPath: password
      readOnly: true

  # 定义 Secret 数据卷
  volumes:
  - name: secret-volume
    secret:
      secretName: db-secret

  restartPolicy: Never
```
容器下/tmp/my-password.txt内容为Admin@123456


## 镜像拉取
镜像拉取需要dockerconfigjson类型的secret，并配置在Pod定义里的.sepc.imagePullSecrets属性中

**示例:**\
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

定义Pod
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


# Secret不可变
对于一些敏感服务的配置文件，在线上有时是不允许修改的\
此时在配置secret时可以设置immutable：true来禁止修改