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


## Deployment


### 创建Deployment
Deployment的创建方式有以下几种

- **定义配置文件**\
  执行命令：
  ```shell
  kubectl create -f xxx.yaml --record
  ```
  注：–record会在annotation中记录当前命令创建或升级了资源，后续可以查看做过哪些变动操作

- **kubectl命令**	
  执行命令：
  ```shell
  kubectl create deploy nginx-deploy --image=nginx:1.7.9
  ```


### 查看Deployment
查看Deployment信息，执行命令：
```shell
kubectl get deployment  #返回nginx-deploy记录
kubectl get replicaset  #返回nginx-deploy-xxxxxxxxxx记录
kubectl get pod  #返回nginx-deploy-xxxxxxxxxx-xxxxx记录

kubectl get deploymenet <deployment name> -o yaml  #以yaml格式输出deployment配置

kubectl get po,rs,deploy  # 可以同时输出po，rs和deploy信息
```
**注：**\
Deployment包含了ReplicaSet，ReplicaSet包含了Pod\
比如Deployment的name是nginx-deploy，则其对应的ReplicaSet就是nginx-deploy-xxxxxxxxxx, 对应的Pod就是nginx-deploy-xxxxxxxxxx-xxxxx

以下是Deployment配置实例
```yaml
apiVersion: apps/v1  # deployment api 版本
kind: Deployment  # 资源类型为deployment
metadadta；  # 元数据
  labels:  #标签配置信息
    app: nginx-deploy
  name: nginx-deploy  # deployment名字
  namespace: default  # 所在命名空间
spec:
  replicas； 1  # 期望副本数
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
      restartPolicy: Always  # 重启策略
      terminationGracePeriodSeconds: 30  # 最大宽限时间
```


### 滚动更新

- **示例**\
  以下是当前Deployment的配置信息
  ```yaml
  apiVersion: apps/v1  # deployment api 版本
  kind: Deployment  # 资源类型为deployment
  metadadta；  # 元数据
    labels:  #标签配置信息
      app: nginx-deploy
      test: test
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
        restartPolicy: Always  # 重启策略
        terminationGracePeriodSeconds: 30  # 最大宽限时间
  ```

修改nginx版本号， 命令如下：
```shell
kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1  # 通过set image命令修改

kubectl set image deployment/nginx-deployment nginx=nginx:1.9.1 --record  # --record参数用于写明修改原因，便于回滚时找到指定的历史版本

kubectl edit deployment/nginx-deployment  #直接edit修改
```

查看滚动更新的过程， 命令如下：
```shell
kubectl rollout status deploy <deployment_name>
```

通过kubectl edit命令，在metadadta.labels追加了test:test标签，保存后，会发现：
1) Deployment并没有触发更新
2) 通过kubectl decribe查看event，也不会发现有添加标签操作的记录

注: 只有当修改了Deployment配置文件中的template.spec中的属性后，才会触发更新操作

通过kubectl edit命令，将spec.replicas从1更新为3，保存后，会发现：
1) Deployment并没有触发更新
2) Pod数量会按照Pod Template的最新配置，从1个变成3个, 但不会滚动更新

通过kubectl edit命令，将spec.template.spec.containers[0].image改成1.9.1后，保存后，会发现：
1) Deployment触发了滚动更新，由于更新是滚动进行，ready总数在更新过程中一直不变

通过kubectl set image命令，将image更新为1.9.1后，会发现：
1) Deployment触发了滚动更新，由于更新是滚动进行，ready总数在更新过程中一直不变

**注：**
1) 滚动更新过程是可以通过kubectl describe 的event追踪到的
2) 滚动更新后，可以通过以下命令，看到两个rs，历史版本的rs下，desired，current字段都是0，当前最新的rs是有值的，执行命令：
```shell
kubectl get rs --show-labels
```

同时也会发现pod都是关联到最新的rs上的，执行命令：
```shell
kubectl get po --show-labels
```

**并发滚动更新**\
当前deploy下有一个rs1，修改deploy后，会创建rs2进行滚动更新\
此时如果rs2尚未滚动更新完成再次对deploy进行修改，那么会创建rs3进行滚动更新，原先正在进行滚动更新的rs2会停止\
r2和r3都会被记录到历史中


### 回滚
Deployment可以执行回滚操作，来回退到一个历史版本\
例如：当前的Deployment不稳定，一直crash looping，可以执行回滚操作，将其回退到历史上某一个稳定的版本

默认情况下，k8s会在系统中保存前两次的deployment的rollout历史记录，以便可以随时回退\
可以修改Deployment配置的.spec.revisionHistoryLimit属性来更改可以保存的revision数，如果设置为0，则表示不允许Deployment回退

- **示例：**\
  更新Deployment的镜像时，镜像参数不小心写错，比如应该是nginx1.9.1，但写成了nginx1.91，执行命令：
  ```shell
  kubectl set image deployment/nginx-deploy nginx=nginx:1.91  #误将Deployment镜像版本更新为1.91
  ```

  监控滚动升级状态发现，由于镜像名称错误导致下载镜像失败，因此更新过程会被卡住，执行命令：
  ```shell
  kubectl rollout status deployment nginx-deploy  # 监控滚动更新状态
  ```

  结束监听后，获取rs信息，可以看到新增的rs副本数是1(原来的rs的副本数是3), 但其状态是not ready, 执行命令：
  ```shell
  kubectl get rs
  ```

  通过kubectl get pods获取pods的信息，可以看到关联到新的rs的pod，状态处于imagePullBackOff状态, 原来deploy的3个pod是running，新的deploy的1个pod是imagePullBackOff, 执行命令：
  ```shell
  kubectl get pods
  ```

  此时查看deploy，发现ready是3/3. up-to-date是1，available是3\
  虽然deploy也是可用的，但是修改后的deploy并没有更新进来
  ```shell
  kubectl get deploy
  ```

  为了修复这个问题，需要找到回退的reversion进行回退\
  先获取reversion列表，执行命令:
  ```shell
  kubectl rollout history deployment/nginx-deploy
  ```

  查看历史某版本的详细信息, 执行命令:\
  注: 它只会返回历史版本当时修改的section的信息，不会将整个yaml都输出
  ```shell
  kubectl rollout history deployment/nginx-deploy --revision=2
  ```

  确认要回退的版本后，就可以回退到上一个版本， 执行命令:
  ```shell
  kubectl rollout undo deployment/nginx-deploy
  ```

  也可以通过以下命令，回退到指定的revision
  ```shell
  kubectl rollout undo deployment/nginx-deploy --to-revision=2
  ```

  查看到版本已经回退到对应的历史revision上了，执行命令:
  ```shell
  kubectl get deployment nginx-deploy
  kubectl describe deployment nginx-deploy
  ```

  此时再查看rs，发现历史版本的rs有了数字，而原来最新的rs下没有了数字
  ```shell
  kubectl get rs
  ```


### 扩缩容
可以通过以下两种方式进行扩缩容

- **kube scale命令**\
  通过kube scale命令可以进行自动扩缩容
  ```shell
  kubectl scale --replicas=6 deploy nginx-deploy
  ```

- **kube edit编辑replicas**\
  通过kube edit编辑replicas也可以实现扩缩容

注: 扩容与缩容只是直接创建副本数，没有更新Pod template, 因此不会创建新的rs


### 暂停与恢复
由于每次对Pod template中的信息发生修改后，都会触发更新Deployment操作\
那么此时如果频繁修改信息，都会产生多次更新，而实际上只需要执行最后一次更新即可\
当出现此类情况时,就可以先暂停Deployment 的rollout


- **示例**\
  先暂停Deployment，执行命令:
  ```shell
  kubectl rollout pause deployment <name>
  ```

  此时对容器进行修改，执行命令:
  ```shell
  kubectl set image deploy <name> nginx=nginx=1.17.9
  ```

  然后查看Pod，发现Pod并没有被更新操作，执行命令:
  ```shell
  kubectl get po
  ```

  再次进行修改一些属性， 如限制nginx容器的最大cpu为0.2核心，最大内存为128M，最小内存为64M，最小cpu为0.1核，执行命令:
  ```shell
  kubectl set resources deploy <deploy_name> -c <container_name> --limits=cpu=200m, memory=128Mi --requests=cpu 100m,memory=64Mi
  ```

  通过格式化输出deployment配置, 看到配置确实发生了修改，执行命令：
  ```shell
  kubectl get deploy <name> -o yaml
  ```

  再次查看Pod，也没有被更新，执行命令：
  ```shell
  kubectl get po
  ```

  恢复rollout，执行命令:
  ```shell
  kubectl rollout resume deploy <name>
  ```

  恢复rollout后，再次查看rs和po信息，可以看到rs和po开始进行滚动更新操作了，执行命令:
  ```shell
  kubectl get rs
  kubectl get po
  ```

  查看历史版本确认历史和最新的记录，执行命令：
  ```shell
  kubectl rollout history deploy nginx-deploy # 查看历史版本
  kubectl rollout history deploy nginx-deploy --revision=<版本号>
  ```