[目录](../目录.md)


# 关于SubPath
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


# SubPath配置
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
**注：**\
- 定义volumes时需要增加items属性，配置key和path，且path的值不能从/开始
- 在容器的volumeMounts中增加subpath属性，该值与volumes中的items.path的值相同


