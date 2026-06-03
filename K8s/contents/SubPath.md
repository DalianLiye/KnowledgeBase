[目录](../目录.md)


# 关于SubPath
使用ConfigMap或secret挂载到容器整个目录时，容器的目录整体会跟着ConfigMap或secret同步更新\
这样，如果目录里有其他文件，那么也会被覆盖更新

通过SubPath就可以规避这个问题，它可以挂载ConfigMap或secret的某一个key到Pod容器指定路径下的单个文件

**示例1:**\
Pod启动后，将ConfigMap test-dir-config下key=db.properties的内容导出到容器的/usr/local/mysql/conf/db.properties文件内\
此时，如果容器的/usr/local/mysql/conf/目录下有其他文件，那么就会被清理掉，只剩下db.properties这个文件
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



**示例2:**\
使用subPath同步ConfigMap的key到单个文件, 具体执行步骤：
1) Pod启动，K8s解析volumes配置,找到ConfigMap：nginx-conf
2) K8s为当前Pod创建独立虚拟卷\
   Pod挂载ConfigMap时，都会单独分配一个独立的虚拟卷, 这个卷和容器原文件系统完全隔离
3) 根据items，读取ConfigMap：nginx-conf中key=nginx.conf的value内容在独立虚拟卷内生成文件\
   生成文件的路径为: 虚拟卷根/etc/nginx/nginx.conf\
   因此，items.path不能以/开头，因为它是虚拟卷内的相对路径，不是容器路径
4) K8s解析volumeMounts + subPath\
   K8s通过subPath会去独立虚拟卷里，找这个路径的文件：虚拟卷根/etc/nginx/nginx.conf\
   因此，subPath必须和volumes.items.path完全一样，否则K8s无法在独立虚拟卷找到文件
5) K8s将独立虚拟卷中的文件，挂载到容器目标文件

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





