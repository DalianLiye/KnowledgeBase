[目录](../目录.md)


# Pod亲和性(PodAffinity)
将Pod一定或尽量调度到与指定的其他Pod所在的同一节点上


## 示例
有两个Pod，商品Pod和订单Pod，通过Pod亲和性来实现将它们俩运行在一个节点上

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-pod-affinity
spec:
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
      - labelSelector:
          matchExpressions: 
          - key: security  # Pod的标签必须要有security key且值是S1
            operator: In
            values:
            - S1
        topologyKey: topology.kubernetes.io/zone # 节点必须要有这个标签
    podAntiAffinity:
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 100
        podAffinityTerm:
          labelSelector:
            matchExpressions:
            - key: security  # Pod的标签必须要有security key且值是S2
              operator: In
              values:
              - S2
          topologyKey: topology.kubernetes.io/zone #节点必须要有这样的标签key
  containers:
  - name: with-pod-affinity
    image: registry.k8s.io/pause:3.8
```


# Pod反亲和性(PodAntiAffinity)
将Pod一定或尽量不要调度到与指定的其他Pod所在的同一节点上