# 基础

容器技术是一种虚拟化技术，为软件应用及其依赖组件提供独立的运行环境。容器包含了应用程序及其所有资源，容器内与容器外的程序共享操作系统，但是文件系统、网络、内存相互隔离

# Docker

Docker是基于Linux容器（Linux Container，LXC）技术的一个虚拟化工具。Linux容器可以简单视作一个轻量级虚拟机，不同容器共享操作系统，但是文件系统、网络、进程相互隔离；而Docker在此基础上提供了创建、运行容器的服务

- **镜像**（Image）：包含了程序运行所需要的所有内容，包括代码、配置文件、库文件、环境变量等。Docker镜像只读，不可修改
- **容器**（Container）：镜像的运行实例，每个容器具有自己的文件系统、网络和进程空间

## 安装

使用官方脚本安装：

```bash
 curl -fsSL https://test.docker.com -o test-docker.sh
 sudo sh test-docker.sh
```

手动安装：

```bash
# 卸载旧版本
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# 安装。比较复杂，此处从略
```

## 运行

```bash
sudo systemctl start docker   # 启动Docker守护进程

# 启动容器，并运行程序
# 本地没有ubuntu:15.10镜像，因此会自动从仓库下载；命令完成后会自动退出容器
docker run ubuntu:15.10 /bin/echo "Hello world"

# 启动容器，并在后台运行
docker run -d ubuntu:15.10 /bin/echo "Hello world"
docker ps -a                    # 查看所有容器。后续操作可用这一步看到的容器ID或name
docker exec -it $cid /bin/bash  # 在当前容器运行interactive shell
docker stop $cid                # 停止容器
docker rm $cid                  # 删除容器
```

### Docker Compose

Compose是管理多个容器的工具

```bash
docker compose up -d   # 读取当前目录的compose.yml配置并启动容器
docker compose down
```

## 镜像

```bash
docker images             # 查看本地镜像
docker pull ubuntu:13.10  # 从仓库下载镜像。默认是https://hub.docker.com/
docker rmi ubuntu:13.10   # 删除镜像
```

注意：Docker Hub被墙了，需要配置代理或者镜像

### 构建镜像

可以使用Dockerfile构建镜像。Dockerfile文件包含了创建镜像使用的每一条指令

```dockerfile
FROM python:3.12
WORKDIR /usr/local/app

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 5000

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

详细说明见[文档](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/)。注：这只是一个简单示例，文档建议采用[Dockerfile Reference](https://docs.docker.com/reference/dockerfile/)的写法

```bash
docker build -t "my_image:dev" ./
```

### 管理镜像

```bash
docker image ls
docker image rm $REPO
```

## 配置

代理、镜像

Docker仓库被墙了，需要配置代理或者镜像。在`/etc/docker/daemon.json`写入（两者选一个即可）

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "https://proxy.example.com:3129",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }

  "registry-mirrors": ["https://docker.xuanyuan.me/"]
}
```

写完之后可能要重启服务：

```bash
sudo systemctl daemon-reload
sudo systemctl restart docker
```

