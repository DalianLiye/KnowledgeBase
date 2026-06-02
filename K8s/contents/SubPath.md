[目录](../目录.md)


# 关于SubPath
SubPath用于挂载ConfigMap或secret的某一个key到Pod容器指定路径下的单文件
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
  subPath: etc/nginx/nginx.conf  # 必须和 volumes.items.path 一样

volumes:
- name: config-volume  # 你这里漏写了 name，必须和上面对应
  configMap:
    name: nginx-conf
    items:
    - key: nginx.conf    # ConfigMap 里的 key
      path: etc/nginx/nginx.conf  # 不能以 / 开头
```
**注：**\
- 定义volumes时需要增加items属性，配置key和path，且path的值不能从/开始
- 在容器的volumeMounts中增加subpath属性，该值与volumes中的items.path的值相同


    volumeMounts:
    - name: db-config
      mountPath: "/usr/local/mysql/conf/db.properties"  # 指向【具体文件】
      subPath: "db.properties"                           # 关键：加了 subPath！
      readOnly: true
  volumes:
    - name: db-config
      configMap:
        name: test-dir-config  # 还是用同一个 configmap
  restartPolicy: Never