### NodeAffinity
节点亲和性，将Pod一定或尽量调度到指定的节点上\
节点亲和性包含以下类型：

- **requiredDuringSchedulingIngoredDuringExecution**\
  硬亲和力，一定(不)部署在指定的节点上
- **preferredDuringSchedulingIngoredDuringExecution**\
  软亲和力，尽量(不)部署在满足条件的节点上

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - antarctica-east1
            - antarctica-west1
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
  containers:
  - name: with-node-affinity
    image: registry.k8s.io/pause:3.8
```

Operator有以下几种类型：
- In
- NotIn
- Exists
- DoesNotExists
- Gt
- Lt