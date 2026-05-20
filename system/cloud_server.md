本笔记记录在云服务器部署各种服务的经验

# 服务配置

拉取镜像：
```bash
docker pull nginx
docker pull gitea/gitea
```

创建工作目录`~/docker`，配置`compose.yml`。配置注意点：

1. 镜像版本名不用`latest`，避免版本更新导致`latest`不知道指向哪里
2. 全部服务放在同一个network

```yml
services:
  nginx:
    image: nginx:1.29
    container_name: nginx
    ports:
      - "80:80"
    volumes:
      - ./nginx/html:/usr/share/nginx/html:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./nginx/logs:/var/log/nginx
    networks:
      - webnet

  gitea:
    image: gitea/gitea:1.26.1
    container_name: gitea
    environment:
      - USER_UID=1000
      - USER_GID=1000
    restart: always
    volumes:
      - ./gitea:/data
      - /etc/timezone:/etc/timezone:ro
      - /etc/localtime:/etc/localtime:ro
    networks:
      - webnet

networks:
  webnet:
    driver: bridge
```

配置完之后，把容器里面的配置文件复制一份出来：
```bash
mkdir nginx

docker run --name temp-nginx -d nginx:1.29
docker cp temp-nginx:/etc/nginx/conf.d ./nginx

docker stop temp-nginx
docker rm temp-nginx
```
其他配置文件夹同理。然后创建`./nginx/html/index.html`（或者从容器复制一份出来），运行`docker compose up`就能访问Nginx默认页了

# 域名配置

参考[免费域名注册笔记](https://shenao.de/blog/)，在[Stackryze](https://domain.stackryze.com/)注册域名。注册完成后，然后用[CloudFlare](https://dash.cloudflare.com/)托管

托管流程：在Cloudflare添加域名和DNS记录，获得Name Server；回到Stackryze，将域名的Name Server改为CF的服务器；等待DNS生效。注意：**不要配置域名泛解析**。域名泛解析到境外服务器可能被风控判定为高危服务，遭到DNS封锁

写Nginx配置文件，将子域名代理到各种真实服务

```nginx
# Default
server {
    listen       80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}

# Gitea
server {
    listen 80;
    server_name gitea.example.com;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

# 配置HTTPS访问

参考：[Docker部署Certbot](https://www.cnblogs.com/vishun/p/15746849.html)，这个笔记将证书目录同时挂载到Certbot和Nginx容器，并使用HTTP验证。泛域名证书必须要用DNS验证，因此进行了一些修改

登录[CloudFlare控制台](https://dash.cloudflare.com/)，创建API Key，并创建`~/.secrets/certbot/cloudflare.ini`，写入`dns_cloudflare_api_token = <API Key>`

然后运行带有certbot-dns-cloudflare（注意：需要将密钥目录、证书目录都挂载出来）。确认没问题的话还可以加上`--rm`参数运行，跑完自动删掉容器。运行之后会存放在`证书挂载点/live/<域名>`

```bash
docker run \
  -v ~/.secrets/certbot:/secrets:ro \
  -v ~/docker/nginx/cert:/etc/letsencrypt:rw \
  certbot/dns-cloudflare \
  certonly \
  --non-interactive \
  --agree-tos \
  --email chensk1999@outlook.com \
  --dns-cloudflare \
  --dns-cloudflare-credentials /secrets/cloudflare.ini \
  -d arclight.indevs.in \
  -d "*.arclight.indevs.in"
```

certbot偶尔跑一次获取证书就够了，因此也可以考虑直接安装（但是尝试在云服务器安装certbot时遇到了python版本不匹配的问题，最终还是回到Docker）

nginx服务器配置：

```nginx
server {
    listen 80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}

# HTTPS
server {
    listen 443 ssl default_server;
    http2 on;
    server_name _;
    ssl_certificate     /etc/nginx/ssl/live/arclight.indevs.in/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/live/arclight.indevs.in/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
```

可以把SSL配置写进另一个文件，如`ssl.conf`，在主配置文件里面只写`include /etc/nginx/conf.d/ssl.conf;`

# 安装Hermes

时效性：2026.05.18

参考：[Using Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/docker)

```bash
docker pull nousresearch/hermes-agent:latest
```

## 测试

```bash
# 初始化工具。配置模型和API Key
docker run -it --rm --user hermes -v ./hermes:/opt/data nousresearch/hermes-agent setup

# 测试对话。能收到回复、能调用系统功能比如“查看磁盘占用”，则成功
docker run -it --rm --user hermes -v ./hermes:/opt/data nousresearch/hermes-agent
docker run -it --rm  --user hermes-v ./hermes:/opt/data nousresearch/hermes-agent -c  # 恢复Session

# 测试Gateway连接。运行之后给它发消息能收到回复
docker run -it --rm -v ./hermes:/opt/data nousresearch/hermes-agent setup gateway # 初始配置
docker run -it --rm -v ./hermes:/opt/data nousresearch/hermes-agent gateway run
.venv/bin/hermes config set MESSAGING_CWD /opt/data/workspace    # 配置Gateway工作目录
```

注意：官方docker镜像的`entrypoint.sh`会将用户切换到`hermes`（id为`10000:10000`），运行`docker run`和`docker exec`时要指定用户，否则可能导致文件权限异常

在已经启动的容器打开TUI：

```bash
docker exec -it --workdir /opt/data/workspace hermes /opt/hermes/.venv/bin/hermes
docker exec -it --workdir /opt/data/workspace/novelist hermes /opt/hermes/.venv/bin/hermes
```

配置工作目录：在`config.yaml`中写入

```yaml
terminal:
  cwd: /your/project/path
```

有些教程说配置`MESSAGING_CWD`之类的环境变量，都是旧版本的







https://hermes-agent.nousresearch.com/docs/user-guide/features/memory

MEMORY.md 环境、规定 800 token

SOUL.md 用户习惯，500token

Session开始时注入

https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files

hermes.md 项目配置，最高优先级 搜索git root

agents.md 项目配置，中等优先级 在CWD寻找

soul.md 智能体性格、用语配置 `HERMES_HOME/SOUL.md`

https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references

`@file:path_to_file.py:10-25 ` 注入文件内容

`@folder:path/to/dir` 注入目录树

`@diff, @staged` 注入git diff

`@git:5` 注入最近5次提交信息

`@url:https://example.com` 加载网页并注入

注入指定内容
