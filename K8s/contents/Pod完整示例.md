[目录](../目录.md)



以下示例包含了三个探针，两个生命周期函数，以及初始化容器的配置
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: demo-pod-with-init-lifecycle-probes
  labels:
    app: demo
spec:
  # 1) 三个初始化容器：做环境检查、下载依赖、数据库迁移等
  initContainers:
    - name: init-check-env
      image: busybox:1.36
      command: ["sh", "-c", "echo 'Checking environment...'; env; sleep 2"]
      resources:
        requests:
          cpu: "50m"
          memory: "64Mi"
        limits:
          cpu: "200m"
          memory: "128Mi"
    - name: init-download-assets
      image: curlimages/curl:8.8.0
      command:
        - sh
        - -c
        - |
          echo "Downloading assets...";
          curl -fsSL https://example.com/assets.tar.gz -o /work/assets.tar.gz || exit 1;
          echo "Assets downloaded."
      volumeMounts:
        - name: workdir
          mountPath: /work
    - name: init-db-migrate
      image: bitnami/kubectl:1.30
      command:
        - sh
        - -c
        - |
          echo "Simulating DB migration..."; 
          # 假设通过一个服务探活来判断数据库是否可用
          # 实际生产中可替换为 flyway/liquibase/应用内置迁移命令
          for i in $(seq 1 30); do
            nc -zv db.example.svc.cluster.local 5432 && echo "DB ready" && exit 0;
            echo "Waiting DB... $i"; sleep 2;
          done;
          echo "DB not ready in time"; exit 1
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        allowPrivilegeEscalation: false

  # 2) 主容器，包含 lifecycle（postStart / preStop）与三种探针
  containers:
    - name: app
      image: nginx:1.27-alpine
      ports:
        - name: http
          containerPort: 8080
      command: ["sh", "-c"]
      args:
        - |
          # 简单起一个 Nginx 并将 8080 转发到 80
          sed -i 's/listen       80;/listen 8080;/' /etc/nginx/conf.d/default.conf;
          nginx -g 'daemon off;'
      env:
        - name: APP_ENV
          value: "production"

      # lifecycle 定义：postStart / preStop
      lifecycle:
        postStart:
          exec:
            command:
              - sh
              - -c
              - |
                echo "[postStart] Initializing side tasks...";
                # 例如：预热缓存、生成临时文件等
                mkdir -p /var/cache/app && echo "warmed" > /var/cache/app/status
        preStop:
          exec:
            command:
              - sh
              - -c
              - |
                echo "[preStop] Graceful shutdown start...";
                # 通知应用进入优雅退出（这里仅示例打印）
                # 可在真实应用里触发 SIGTERM 处理或调用退出 API
                sleep 5
                echo "[preStop] Cleanup done."

      # 3) 三个探针：startupProbe / readinessProbe / livenessProbe
      # startupProbe：容器启动初期的就绪检查，避免过早开始 liveness/readiness
      startupProbe:
        httpGet:
          path: /healthz/startup
          port: http
          scheme: HTTP
        failureThreshold: 30   # 最多失败 30 次
        periodSeconds: 2       # 每 2 秒探测一次
        timeoutSeconds: 1

      # readinessProbe：是否可对外提供流量
      readinessProbe:
        httpGet:
          path: /healthz/ready
          port: http
          scheme: HTTP
        initialDelaySeconds: 5
        periodSeconds: 5
        timeoutSeconds: 2
        successThreshold: 1
        failureThreshold: 3

      # livenessProbe：进程是否存活
      livenessProbe:
        httpGet:
          path: /healthz/live
          port: http
          scheme: HTTP
        initialDelaySeconds: 10
        periodSeconds: 10
        timeoutSeconds: 2
        successThreshold: 1
        failureThreshold: 3

      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "500m"
          memory: "256Mi"

      volumeMounts:
        - name: workdir
          mountPath: /usr/share/nginx/html/assets
        - name: cache
          mountPath: /var/cache/app

  volumes:
    - name: workdir
      emptyDir: {}
    - name: cache
      emptyDir: {}

  restartPolicy: Always
```
