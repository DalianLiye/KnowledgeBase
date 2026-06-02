[目录](../目录.md)


# 关于ConfigMap
用于存储键值（key-value）格式的非敏感配置数据\
可以通过环境变量或挂载文件的方式注入到Pod中，供容器读取使用\
ConfigMap实现了应用与配置解耦，支持多Pod、多容器共享同一配置，集中管理、便于修改，大幅提升配置维护效率

**注：**
- ConfigMap存储明文数据，不提供任何加密能力
- 敏感信息（密码、密钥、Token、证书）严禁存入 ConfigMap，必须使用 Secret


# 创建ConfigMap

创建ConfigMap的方式主要包括：
- 基于文件夹
- 基于文件（推荐）
- 直接指定key-value


## 基于文件夹
创建db.properties文件，内容如下：
```shell
username=root
password=admin
```

创建redis.properties文件，内容如下：
```shell
host: 127.0.0.1
port: 6379
```

将db.properties和redis.properties两个文件保存至/test文件夹下\
进入到/test文件夹同级目录，创建configmap，执行命令：
```shell
kubectl create configmap test-dir-config --from-file=test/
```

获取configmap列表，执行命令：
```shell
kubectl get cm  # 可以查看刚才看到的configmap
```
<img src="./img/ConfigMap_001.png" alt="ConfigMap001" width="500">

查看configmap具体信息，执行命令：
```shell
kubectl describe cm test-dir-config
```
<img src="./img/ConfigMap_002.png" alt="ConfigMap002" width="500">


## 基于文件
创建application.yaml文件内容如下，并保存至/test目录下
```yaml
spring:
  application:
    name: test-app
server: 
  port: 8080
```

创建configmap，执行命令：
```shell
kubectl create configmap spring-boot-test-yaml --from-file=/test/application.yaml
```

获取configmap列表，执行命令：
```shell
kubectl get cm  # 可以查看刚才看到的configmap
```
<img src="./img/ConfigMap_003.png" alt="ConfigMap003" width="500">

查看configmap具体信息，执行命令：
```shell
kubectl describe cm spring-boot-test-yaml
```
<img src="./img/ConfigMap_004.png" alt="ConfigMap004" width="500">

再次通过以下方式创建configmap，执行命令：
```shell
kubectl create configmap spring-boot-test-alises-yaml --from-file=app.yml=/test/application.yaml
```

查看configmap详细信息，执行命令：
```shell
kubectl describe cm spring-boot-test-alises-yaml

kubectl describe configmap/spring-boot-test-alises-yaml  #另一种表达方式
```
<img src="./img/ConfigMap_005.png" alt="ConfigMap005" width="500">\
注：文件名变成了app.yml, 而不是application.yaml


## 直接指定key-value
一般不建议使用该方式，但如果参数少是可以

创建configmap，执行命令：
```shell
kubectl create configmap test-key-value-config  --from-literal=username=root --from-literal=password=admin
```

查看configmap详细信息，执行命令：
```shell
kubectl describe configmap test-key-value-config
```
<img src="./img/ConfigMap_006.png" alt="ConfigMap006" width="500">\
注：通过键值对直接创建cm是没有文件名的



# 使用ConfigMap

- **示例1**\
  创建configmap，执行命令：
  ```shell
  kubectl create configmap test-env-config --from-literal=JAVA_OPTS_TEST='-Xms512m -Xmx512m' --from-literal=APP_NAME=springboot-env-test
  ```

  查看configmap详细信息，执行命令：
  ```shell
  kubectl describe configmap test-env-config
  ```
  <img src="./img/ConfigMap_007.png" alt="ConfigMap007" width="500">


  执行kubectl create命令创建如下Pod，文件名env-test-pod.yaml文件
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: test-env-pod
  spec:
    containers:
    - name: env-test
      image: alpine  # 轻量级的linux系统
      command: ["/bin/sh","-c","env; sleep 3600"] # 为避免执行命令后直接退出容器，设置睡眠3600秒
      imagePullPolicy: IfNotPresent
      env:
      - name: JAVA_VM_OPTS
        valueFrom: 
          configMapKeyRef:
            name: test-env-config # configmap的名字
            key: JAVA_OPTS_TEST # 从configmap中获取名字为key的value，将其赋值给容器本地的环境变量JAVA_VM_OPTS     
      - name: APP
        valueFrom:
          configMapKeyRef:
            name: test-env-config
            key: APP_NAME
    restartPolicy: Never
  ```

  查看pod容器中的日志，可以发现环境变量已被设置，执行命令：
  ```shell
  kubectl logs -f test-env-pod  # -f不是file，是follow的意思
  ```
  <img src="./img/ConfigMap_008.png" alt="ConfigMap008" width="500">


- **示例2**\
  执行kubectl create命令创建如下Pod，文件名file-test-pod.yaml文件
  ```yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: test-configfile-pod
  spec:
    containers:
    - name: config-test
      image: alpine  # 轻量级的linux系统
      command: ["/bin/sh","-c","env; sleep 3600"]
      imagePullPolicy: IfNotPresent
      env:
      - name: JAVA_VM_OPTS
        valueFrom: 
          configMapKeyRef:
            name: test-env-config # configmap的名字
            key: JAVA_OPTS_TEST # 从configmap中获取名字为key的value，将其赋值给容器本地的环境变量JAVA_VM_OPTS     
      - name: APP
        valueFrom:
          configMapKeyRef:
            name: test-env-config
            key: APP_NAME
      volumeMounts:  # 加载数据卷
      - name: db-config  # 要加载数据卷的名字
        mountPath: "/usr/local/mysql/conf"  # 想要将数据卷中的文件加载到哪个目录下
        readOnly: true  # 是否只读
    volumes:  #数据卷挂载， configMap，sercret
      - name: db-config  # 数据卷的名字，名字可以自定义
        configMap: #数据卷类型为configMap
          name: test-dir-config  # configMap的名字，跟想要加载的configmap name相同
          items:  # 对configmap中的key进行映射，如果不指定，默认会将configmap中所有的key全部转换为同名的文件
          - key: "db.properties"  # configmap中的key
            path: "db.properties"  # 将该key中的值转换为文件
    restartPolicy: Never
  ```
  注：如果path: "db.properties" 改成path: "/test1/test2/db_test.properties",那么该文件在容器内的生成路径为/usr/local/mysql/conf/test1/test2/db_test.properties

  进入容器，可以看到指定路径下有db.properties，执行命令：
  ```shell
  kubectl exec -it test-configfile-pod -- sh

  ls /usr/local/mysql/conf  # 可以发现db.properties文件存在
  cat /usr/local/mysql/conf/db.properties  # 内容跟创建configmap时一致
  ```
  <img src="./img/ConfigMap_009.png" alt="ConfigMap009" width="500">



# 不可变configmap
对于一些敏感服务的配置文件，在线上有时是不允许修改的\
此时在配置configmap时可以设置immutable：true来禁止修改\
<img src="./img/ConfigMap_010.png" alt="ConfigMap010" width="500">