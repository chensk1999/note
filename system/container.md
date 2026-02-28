# 基础

容器是一种**虚拟化技术**，为软件应用及其依赖组件提供独立的运行环境。容器包含了应用程序及其所有资源，容器内与容器外的程序共享操作系统，但是文件系统、网络、内存相互隔离

容器技术源于**软件部署的需求**：现代软件除了自己之外，还有大量依赖，比如某个库的DLL文件，系统环境变量，特定的操作系统功能等。软件更新时这些依赖有可能改变，而且在同一台计算机上安装多个软件时依赖可能冲突。这些麻烦的解决方案就是把软件本身和依赖打包在一起，在独立的环境中运行

打包、独立环境最初的实现方法是虚拟机。但运行虚拟机时，在宿主机的操作系统上运行了虚拟机操作系统，两个操作系统的文件、功能都有冗余——宿主有一套操作系统文件，虚拟机中又有一套；宿主的内核进程管理着内存和CPU的分配，虚拟机的内核进程也在做类似的事。为了减少冗余提高性能，发展出了以下技术：

- **联合文件系统**（Union File System）：Union FS是一种分层的文件系统，访问文件时首先寻找上层，若上层没有则使用下层的文件。在容器中，下层是共享的系统文件，若需要修改，则增加一层，在容器自己独有的层中修改。这样就实现了文件复用
- **控制组**（Control Groups）：简称cgroup，是Linux内核功能。cgroup控制进程组使用的系统资源（内存，CPU占用，IO带宽等）。运行在cgroup中的进程只能使用组内资源，并且无法和组外进程直接通信。这样，只需要一套操作系统内核就能管理多个容器的资源

将上述技术整合在一起，并提供一套好用的接口，这就是我们今天使用的容器。最早也最出名的容器是Docker，但它在激烈竞争中落败，目前最成功的容器软件是Kubernetes，简称K8s

# Docker

Docker是基于Linux容器（Linux Container，LXC）技术的一个虚拟化工具。Linux容器可以简单视作一个轻量级虚拟机，不同容器共享操作系统，但是文件系统、网络、进程相互隔离；而Docker在此基础上提供了创建、运行容器的服务

- **镜像**（Image）：包含了程序运行所需要的所有内容，包括代码、配置文件、库文件、环境变量等。Docker镜像只读，不可修改
- **容器**（Container）：镜像的运行实例，每个容器具有自己的文件系统、网络和进程空间

## 安装

使用官方脚本安装：

```bash
 curl -fsSL https://test.docker.com -o test-docker.sh
 sudo sh test-docker.sh
 
 sudo systemctl start docker   # 启动Docker守护进程
```

手动安装：

```bash
# 卸载旧版本
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# 安装。比较复杂，此处从略
```

## 容器

```bash
# 启动容器，并运行程序
# 若本地没有ubuntu:15.10镜像，则会从仓库下载
docker run ubuntu:15.10 /bin/echo "Hello world"

# 启动容器，并在后台运行
docker run -d ubuntu:15.10 /bin/echo "Hello world"
docker ps -a                    # 查看所有容器。后续操作可用这一步看到的容器ID或name
docker exec -it $cid /bin/bash  # 在当前容器运行interactive shell
docker stop $cid                # 停止容器
docker rm $cid                  # 删除容器
```

### Docker Compose

Compose是管理多个容器的工具（旧版本为`docker-compose`，需要独立安装）

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

Docker配置文件位于`/etc/docker/daemon.json`。注意，Docker可能占用了配置文件，如果写不进去就要关掉Docker再改

```bash
sudo systemctl stop docker     # 关闭Docker
systemctl list-units --type=service | grep docker  # 确认已经关掉了

sudo systemctl daemon-reload
sudo systemctl restart docker  # 重启Docker
```

### 代理和镜像

Docker仓库被墙了，需要配置代理或者镜像

```json
{
    // 代理
    "proxies": {
        "http-proxy": "http://proxy.example.com:3128",
        "https-proxy": "https://proxy.example.com:3129",
        "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
    }

    // 镜像
    "registry-mirrors": ["https://docker.xuanyuan.me/"]
}
```

### TLS验证

如果仓库的CA证书有问题，Docker会拒绝操作（`tls: failed to verify certificate`），需要加上如下配置：

```json
{
    "insecure-registries": ["registrydomain.com:5000"]
}
```

