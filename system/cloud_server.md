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
docker cp nginx:/etc/nginx/conf.d ./nginx

docker stop temp-nginx
docker rm temp-nginx
```
其他配置文件夹同理。然后创建`./nginx/html/index.html`（或者从容器复制一份出来），运行`docker compose up`就能访问Nginx默认页了

# 域名配置

参考[免费域名注册笔记](https://shenao.de/blog/)，在[Stackryze](https://domain.stackryze.com/)注册域名。注册完成后，然后用[CloudFlare](https://dash.cloudflare.com/)托管

托管流程：在Cloudflare添加域名和DNS记录，获得Name Server；回到Stackryze，将域名的Name Server改为CF的服务器；等待DNS生效

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

