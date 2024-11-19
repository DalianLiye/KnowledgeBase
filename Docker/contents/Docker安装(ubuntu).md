# 安装步骤
- **更新系统包索引**\
确保系统包索引是最新的
```bash
sudo apt update
```

- **安装必要的依赖包**
安装一些必要的包，以便apt可以通过HTTPS使用仓库
```bash
sudo apt install apt-transport-https ca-certificates curl software-properties-common
```

- **添加Docker的官方GPG密钥**
```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

- **设置Docker的稳定版仓库**\
添加Docker的稳定版仓库到你的系统
```bash
echo deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- **更新包索引**\
再次更新包索引，以包含Docker仓库中的包
```bash
sudo apt update
```

- **安装Docker**\
安装Docker CE（社区版）
```bash
sudo apt install docker-ce docker-ce-cli containerd.io
```

- **验证Docker安装**\
运行以下命令来验证Docker是否安装成功
```bash
sudo docker run hello-world
```
如果一切正常，会看到一条欢迎消息，说明Docker已经成功安装并运行


- **启动和启用Docker服务**
```bash
sudo systemctl start docker
sudo systemctl enable docker
```


- **将当前用户添加到docker组（可选）**\
为了在不使用sudo的情况下运行Docker命令，可以将当前用户添加到 docker组
```bash
sudo usermod -aG docker ${USER}
```
注：需要重新登录或重启系统以使更改生效


- **验证用户组更改**\
重新登录后，运行以下命令来验证当前用户是否已经添加到docker组
```bash
groups
```
应该会看到docker组在输出中


- **测试Docker**\
再次运行一个简单的Docker容器来确保一切正常
```bash
docker run hello-world
```
如果一切正常，会看到相同的欢迎消息


- **安装Docker Compose**
```bash
sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

验证安装
```bash
docker-compose --version
```

# 注意
- docker安装时，需要在以下配置文件中设置正确的镜像网站
```bash
/etc/docker/daemon.json
```
其内容格式为：
```bash
{
  "registry-mirrors": ["https://docker.1panel.live"]
}

```

- 通过以下命令，查看docker的日志信息
```bash
sudo journalctl -u docker
```

- 通过以下命令，查看docker状态信息
```bash
sudo systemctl status docker
```

- 常见的镜像网站\
URL：https://www.coderjia.cn/archives/dba3f94c-a021-468a-8ac6-e840f85867ea
