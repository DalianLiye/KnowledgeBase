[目录](../目录.md)


# 关于Horizontal Pod Autoscaling(HPA)
HPA依据内置（CPU/内存）或自定义指标，动态调整Deployment、StatefulSet等工作负载控制器的Pod副本数量，实现Pod水平扩缩容\
作用域：命名空间

默认每30秒查询一次指标数据，轮询间隔可通过kube-controller-manager的以下参数参数修改
- 参数: horizontal-pod-autoscaler-sync-period

HPA支持以下指标类型：
- 内置指标：按资源利用率计算，如Pod CPU/内存
- 自定义Pod指标：按原始数值计算
- 自定义对象指标：如其他资源的状态指标

HPA指标获取方式
- Heapster: 早期方式，不推荐
- Metrics Server: 主流, 提供基础指标
- 自定义REST API: 获取扩展指标

**注：**\
可以通过配置多组指标联合判断扩缩容策略



## HPA自动扩/缩容
HPA自动扩缩容，是指通过观察Pod的cpu，内存使用率或自定义metrics指标针对Pod的数量，自动进行扩容或缩容\
英文全称，“HorizontalPodAutoscaler”
  
HPA自动扩缩容通常用于Deployment ，对于无法扩缩容的对象不适用，比如DaemonSet\
控制管理器每隔30s(该时间间隔通过-horizontal-pod-audoscaler-sync-period属性修改)查阅metrics的资源使用情况


### 创建HPA
Deployment的创建方式有以下几种

- **定义配置文件**\	
  执行命令：
  ```shell
  kubectl create -f hpa-create.yaml
  ```

- **kubectl命令**\
  执行命令：
  ```shell
  kubectl autoscale deployment myapp --min=2 --max=10 --cpu-percent=50
  ```


### HPA配置
配置文件：
```yaml
apiVersion: autoscaling/v2beta2
kind: HorizontalPodAutoscaler
metadata:
  name: legacy-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: legacy-app
  minReplicas: 1
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```


### 开启指标服务
配置HPA自动扩缩容，需要先开启指标服务，操作步骤如下：

下载metrics-server组件配置文件到本地，执行命令：
```shell
wget https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml -O metrics-server-components.yaml
```

修改配置文件中的镜像地址为国内的地址，执行命令：
```shell
sed -i 's/k8s.gcr.io\/metrics-server/registry.cn-hangzhou.aliyuncs.com\/google_containers/g' metrics-server-components.yaml

grep image metrics-server-components.yaml  # 查看镜像是否修改成功
```

修改容器的tls配置，使其不验证tls\
在yaml文件的.spec.template.spec.args里添加--kubelet-insecure-tls\
注：由于本地没有https证书，加上该参数后，就可以不用校验https证书了，证明是可信任的

yaml配置文件修改好后，执行安装，执行命令：
```shell
kubectl apply -f metrics-server-components.yaml
```

查看Pod状态，执行命令
```shell
kubectl get po -A | grep metrics  # 确认pod正在运行
```


### cpu，内存指标监控
监控某对象的cpu或内存，需具备以下前提条件：
- 对象配置了resources.requests.cpu
- 对象配置了resources.requests.memory

可以为cpu或memory配置阈值，阈值可以是具体数值或百分比，当达到阈值时自动进行扩缩容



  **示例**\
  创建以及测试HPA, 执行以下步骤：
  1) 创建一个Deployment，该Deployment必须进行了资源的限制(request/limit)
      ```yaml
      apiVersion: apps/v1  # deployment api 版本
      kind: Deployment  # 资源类型为deployment
      metadadta；  # 元数据
        labels:  #标签配置信息
          app: nginx-deploy
        name: nginx-deploy  # deployment名字
        namespace: default  # 所在命名空间
      spec:
        replicas: 1  # 期望副本数
        revisionHistoryLimit: 10  #进行滚动更新后保留的历史版本数
        selector:  # 选择器
          matchLabels:  #按照标签匹配
            app: nginx-deploy   # 匹配的标签key-value
        strategy:  # 更新策略
          rollingUpdate:  # 滚动更新配置 
            maxSurge: 25%  # 进行滚动更新时，更新的个数最多可以超过期望副本数的个数或比例
            maxUnavailable； 25%  #进行滚动更新时，最大不可用比例，表示在所有副本数中，最多可以有多少个可以不更新成功
          type: RollingUpdate  # 更新类型，采用滚动更新
        template:  #Pod模板
          metadata:  # Pod的元数据
            labels:  # Pod标签
              app: nginx-deploy
          spec:  # Pod期望
            containers:  # Pod容器
            - image: nginx:1.7.9  # Pod镜像
              imagePullPolicy: IfNotPresent   # Pod容器拉取策略
              name: nginx  # Pod容器名称
              resources:
                limits:
                  cpu: 200m
                  memory: 128Mi
                requests:
                  cpu: 100m
                  memory: 128Mi 
            restartPolicy: Always  # 重启策略
            terminationGracePeriodSeconds: 30  # 最大宽限时间
      ```
  
  2) 配置HPA，执行命令：
      ```shell
      kubectl autoscale deploy <deploy_name>  --cpu-percent=20  --min=2 --max=5

      # --cpu-percent=20：目标 CPU 利用率为 20%。当 Deployment 中所有 Pod 的平均 CPU 使用率超过 20% 时，HPA 会尝试增加 Pod 数量；低于 20% 时，会尝试减少 Pod 数量
      # --min=2：Pod 副本数的最小值，至少保持 2 个 Pod
      # --max=5：Pod 副本数的最大值，最多扩展到 5 个 Pod
      ```

  3) 获取HPA信息，执行命令：
      ```shell
      kubectl get hpa

      kubectl top  # 可以查看cpu和内存占用情况，需要开启指标服务metrics service
      ```

  4) 配置service\
      配置了service后，才可以通过curl访问Pod
      ```yaml
      apiVersion: v1
      kind: Service
      metadata:
        name: nginx-svc
        labels:
          app: nginx
      spec:
        selector:
          app: nginx-deploy  
        ports:
        - port: 80
          targetPort: 80
          name: web
        type: NodePort
      ```

1) 测试\
    找到对应服务的service，编写循环测试脚本提升内存与cpu负载
    ```shell
    while true: do wget -q -O - http://<ip:port> > /dev/null; done  #死循环
    ```
    可以通过多台机器执行上述命令，增加负载，当超过负载后可以查看pods的扩容情况


### 自定义metrics
控制管理器开启-horizontal-pod-autoscaler-use-rest-clients\
控制管理器的-apiserver指向API server aggregator\
在API server aggregator中注册自定义的metrics API
