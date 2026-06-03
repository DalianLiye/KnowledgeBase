[目录](../目录.md)


# 关于Pod水平自动扩缩
Pod水平自动扩缩(Horizontal Pod Autoscaling,HPA)依据内置（CPU/内存）或自定义指标，动态调整Deployment、StatefulSet等工作负载控制器的Pod副本数量，实现Pod水平扩缩容\



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

**注：**
- 可以通过配置多组指标联合判断扩缩容策略
- HPA自动扩缩容通常用于Deployment ，对于无法扩缩容的对象不适用，比如DaemonSet



# HPA创建
Deployment的创建方式包括:

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


# HPA配置

定义HPA
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


# 开启指标服务
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


# 监控指标配置(cpu+内存)
监控某对象的cpu或内存，需具备以下前提条件：
- 对象配置了resources.requests.cpu
- 对象配置了resources.requests.memory

可以为cpu或memory配置阈值，阈值可以是具体数值或百分比，当达到阈值时自动进行扩缩容



**示例**\
创建以及测试HPA, 执行以下步骤：

创建Deployment，该Deployment必须进行了资源的限制(request/limit)
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
 labels:
   app: nginx-deploy
 name: nginx-deploy
 namespace: default
spec:
 replicas: 1
 revisionHistoryLimit: 10
 selector:
   matchLabels:
     app: nginx-deploy
 strategy:
   rollingUpdate:
     maxSurge: 25%
     maxUnavailable: 25%
   type: RollingUpdate
 template:
   metadata:
     labels:
       app: nginx-deploy
   spec:
     containers:
     - image: nginx:1.7.9
       imagePullPolicy: IfNotPresent
       name: nginx
       resources:
         limits:
           cpu: 200m
           memory: 128Mi
         requests:
           cpu: 100m
           memory: 128Mi
     restartPolicy: Always
     terminationGracePeriodSeconds: 30
```
  
配置HPA，执行命令：
```shell
kubectl autoscale deploy <deploy_name>  --cpu-percent=20  --min=2 --max=5
```
- cpu-percent=20：目标CPU利用率为20%, 当Deployment中所有Pod的平均CPU使用率超过20%时，HPA会尝试增加Pod数量；低于20%时，会尝试减少Pod数量
- min=2：Pod 副本数的最小值，至少保持2个Pod
- max=5：Pod 副本数的最大值，最多扩展到5个Pod

获取HPA信息，执行命令：
```shell
kubectl get hpa
kubectl top  # 可以查看cpu和内存占用情况，需要开启指标服务metrics service
```

配置service, 通过curl访问Pod
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

找到对应服务的service，编写循环测试脚本提升内存与cpu负载，测试HPA\
可以通过多台机器执行上述命令，增加负载，当超过负载后可以查看pods的扩容情况
```shell
while true: do wget -q -O - http://<ip:port> > /dev/null; done  #死循环
```


# 自定义metrics
HPA使用自定义指标custom.metrics.k8s.io，集群三项开关必须打开：
- **kube-apiserver**\
  开启API聚合层\
  启动参数：--enable-aggregator-routing=true\
  作用：开启API聚合转发，聚合网关收到自定义指标API请求，转发给对应适配器服务
- **kube-controller-manager**\
  启用HPA REST客户端\
  启动参数：--horizontal-pod-autoscaler-use-rest-clients=true\
  作用：HPA不再依赖老旧Heapster，改用API接口拉取指标，支持自定义/外部指标, 关闭仅支持CPU、内存原生指标
- **通过APIService在API聚合器注册自定义指标API**