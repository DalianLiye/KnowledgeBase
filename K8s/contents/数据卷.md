[目录](../目录.md)


# 关于数据卷
数据卷(Volume)可实现同一个Pod内多个容器共享数据，核心用于数据持久化\
容器异常销毁后，卷内数据不会丢失\
典型场景:数据库等有状态服务

K8s持久化存储核心分为:
- 持久化卷(PV)
- 持久化卷声明(PVC)


## SubPath
使用ConfigMap或secret挂载到目录的时候，会将容器中原来的目录覆盖掉\
此时可能只想覆盖目录中的某一个文件，但是这样的操作会覆盖整个文件夹，因此需要使用到subpath

比如以下配置，pod启动后，会将整个/usr/local/mysql/conf目录覆盖，整个目录原来的文件就都没有了，会只有db.properties
```yaml
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
```


subPath的配置方式如下：
```yaml
containers:
....
  volumeMounts:
  - mountPath: /etc/nginx/nginx.conf 
    name: config-volume
    subPath: etc/nginx/nginx.conf # 与volumes.[0].items.path 相同
volumes:
- configMap:
  name: nginx-conf  # configMap名字
  items:
    key: nginx.conf  #configMap中的文件名
    path: etc/nginx/nginx.conf  # subpath路径
```
**说明：**\
1）定义volumes时需要增加items属性，配置key和path，且path的值不能从/开始\
2）在容器的volumeMounts中增加subpath属性，该值与volumes中的items.path的值相同



## Volumes


### HostPath
将节点上的文件或目录挂载到Pod上，此时它会变成持久化存储目录\
即便Pod被删除后重启，也可以重新加载到该目录，该目录下的文件不会丢失

执行kubectl create命令创建如下Pod，文件名volume-test-pd.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: test-volume-pd
spec:
  containers:
  - image: nginx
    name: nginx-volume
    volumeMounts:
    - mountPath: /test-pd  # 挂载到容器哪个目录
      name: test-volume  # 挂载哪个volume
  volumes:
  - name: test-volume
    hostPath:  # 与主机共享目录，加载主机中的指定目录到容器
      path: /data  # 节点中的目录
      type: DirectoryOrCreate  # 检查类型，在挂载前对比挂载目录做什么检查操作，有多种选项，默认为空字符串，不做任何检查
```
Pod运行所在节点的/data目录和Pod容器内的/test-pd目录是互通的



**hostPath的检查类型**\
hostPath的type字段用于指定宿主机路径的预期类型，k8s会根据这个类型做一些校验，确保挂载的路径符合预期，避免因路径类型不符导致的错误

检查类型有以下几种： 
- **空字符串**\
  ""（空字符串\
  不做任何类型检查，路径必须存在，且类型不限（默认行为）

- **DirectoryOrCreate**\
  如果路径不存在，则创建目录，权限为755\
  如果存在则必须是目录

- **Directory**\
  路径必须存在且是一个目录

- **FileOrCreate**\
  如果路径不存在，则创建空文件，权限为644
  如果存在，则必须是普通文件

- **File**\
  路径必须存在且是一个普通文件

- **Socket**\
  路径必须存在且是一个Unix socket文件

- **CharDevice**\
  路径必须存在且是一个字符设备文件

- **BlockDevice**\
  路径必须存在且是一个块设备文件


### EmptyDir
EmptyDir主要用于一个Pod中的不同container间共享数据\
由于只是在Pod内部使用，因此与其他volume比较大的区别是，当Pod如果被删除了，那么emptyDir也会被删除

存储介质可以是任意类型，比如SSD，磁盘或网络存储，甚至内存\
当存储介质设置为内存时，emptyDir.medium被设置为Memory, 从而让k8s使用tmpfs(内存支持文件系统)，速度比较快\
但是重启tmpfs节点时，数据会被清除，且设置的大小会计入到Container的内存限制中

执行kubectl create命令创建如下Pod，文件名empty-dir-pd.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: empty-dir-pd
spec:
  containers:
  - image: alpine
    name: nginx-emptydir1
    command: ["/bin/sh","-c","sleep 3600;"]
    volumeMounts:
    - mountPath: /cache
      name: cache-volume
  - image: alpine
    name: nginx-emptydir2
    command: ["/bin/sh","-c","sleep 3600;"]
    volumeMounts:
    - mountPath: /opt
      name: cache-volume 
  volumes:
  - name: cache-volume
    emptyDir: {}  # 表示创建一个临时的空目录卷，供Pod中的所有容器共享使用
```
nginx-emptydir1容器的/cache目录和nginx-emptydir2容器的/opt目录是互通的


## NFS挂载
NFS卷可以将NFS(网络文件系统)挂载到Pod中\
与emptyDir不同，NFS卷的内容在删除Pod时会被持久化保存，卷只是被卸载\
NFS卷可以被预先填充数据，并且这些数据可以在Pod之间共享\
NFS由于需要网络IO，因此它的效率并不高，不适合用于频繁以及高并发的读写操作


### NFS系统搭建
安装NFS包\
注：k8s每个节点都执行
```shell
yum install nfs-utils -y
```

启动NFS\
注：k8s每个节点都执行
```shell
systemctl start nfs-server
```

查看NFS版本\
注：k8s每个节点都执行
```shell
cat /proc/fs/nfsd/version
```

创建共享目录\
注：在Node01节点执行，即选择存储空间比较大的节点
```shell
mkdir -p /home/nfs
cd /home/nfs
mkdir rw
mkdir ro
```

设置共享目录export\
注：在Node01节点执行
```shell
vim /etc/exports

/home/nfs/rw 192.168.113.0/24(rw,sync,no_subtree_check,no_root_squash)
/home/nfs/ro 192.168.113.0/24(ro,sync,no_subtree_check,no_root_squash)

# 192.168.113.0/24是整个k8s的CIDR
```

重新加载(node01上操作)
```shell
exports -f
systemctl reload nfs-server

touch /home/nfs/ro/README.md
echo 'hello...nfs' > /home/nfs/ro/README.md
```

到Node02节点测试
```shell
mkdir -p /mnt/nfs/rw
mkdir -p /mnt/nfs/ro
mount -t nfs 192.168.113.121:/home/nfs/rw /mnt/nfs/rw  
mount -t nfs 192.168.113.121:/home/nfs/ro /mnt/nfs/ro 

# 192.168.113.121是node01的ip

ls /mnt/nfs/ro  # 会发现有README.md文件
touch /mnt/nfs/ro/test.csv  # 会报错，提示cannot touch test.csv, read-only file system

touch /mnt/nfs/rw/test.csv # 文件创建成功

# 登录node01节点，执行以下命令查询发现test.csv
ls /home/nfs/rw/
```

### 配置NFS到Pod
执行kubectl create命令创建如下Pod，文件名nfs-test-pd.yaml
```yaml
apiVersion: v1
kind: Pod
matadata:
  name: nfs-test-pd1
spec:
  containers:
  - image: nginx
    name: test_container
    volumeMounts:
    - mountPath: /my-nfs-data
      name: test-volume
  volumes:
  - name: test-volume
    nfs:
      server: 192.168.113.121  # 网络存储服务地址，即设置了共享目录的Node01节点的IP
      path: /home/nfs/rw/www/wolfcode  # 网络存储路径
      readOnly: false   # 是否只读
```

node1创建如下目录
```shell
mkdir -p /home/nfs/rw/www/wolfcode
echo 'hello ' > /home/nfs/rw/www/wolfcode/index.html
```
nfs-test-pd1 Pod容器中，可以看到/my-nfs-data目录下上一步创建的index.html文件\
即容器的/my-nfs-data和/home/nfs/rw/www/wolfcode是连通的