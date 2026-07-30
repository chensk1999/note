本笔记记录部署各种服务的经验

# Web服务

## Nginx

拉取镜像：
```bash
docker pull nginx
```

创建工作目录`~/docker`，配置`compose.yml`。配置完之后，把容器里面的配置文件复制一份出来：

```bash
mkdir nginx

docker run --rm --name temp-nginx -d nginx:latest
docker cp temp-nginx:/etc/nginx/conf.d ./nginx
docker cp temp-nginx:/usr/share/nginx/html ./nginx
docker stop temp-nginx
```
其他配置文件夹同理。然后运行`docker compose up`就能访问Nginx默认页了

## 域名配置

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

## 配置HTTPS访问

参考：[Docker部署Certbot](https://www.cnblogs.com/vishun/p/15746849.html)，这个笔记将证书目录同时挂载到Certbot和Nginx容器，并使用HTTP验证。泛域名证书必须要用DNS验证，因此进行了一些修改

登录[CloudFlare控制台](https://dash.cloudflare.com/)，创建API Key，并创建`~/.secrets/certbot/cloudflare.ini`，写入`dns_cloudflare_api_token = <API Key>`

然后运行`certbot/dns-cloudflare`容器（注意：需要将密钥目录、证书目录都挂载出来）。运行之后会存放在`证书挂载点/live/<域名>`

```bash
docker run \
  --rm
  -v ~/.secrets/certbot:/secrets:ro \
  -v ~/nginx/cert:/etc/letsencrypt:rw \
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

可以把SSL配置写进另一个文件，如`ssl.include`，在主配置文件里面只写`include /etc/nginx/conf.d/ssl.include;`

# AI智能体

## Hermes

时效性：2026.05.18

参考：[Using Hermes](https://hermes-agent.nousresearch.com/docs/user-guide/docker)

```bash
docker pull nousresearch/hermes-agent:latest
```

试运行

```bash
# 初始化工具。配置模型和API Key
docker run -it --rm --user hermes -v ./hermes:/opt/data nousresearch/hermes-agent setup

# 测试对话。能收到回复、能调用系统功能比如“查看磁盘占用”，则成功
docker run -it --rm --user hermes -v ./hermes:/opt/data nousresearch/hermes-agent
docker run -it --rm  --user hermes-v ./hermes:/opt/data nousresearch/hermes-agent -c  # 恢复Session

# 测试Gateway连接。运行之后给它发消息能收到回复
docker run -it --rm --user hermes -v ./hermes:/opt/data nousresearch/hermes-agent setup gateway # 初始配置
docker run -it --rm --user hermes -v ./hermes:/opt/data nousresearch/hermes-agent gateway run
.venv/bin/hermes config set MESSAGING_CWD /opt/data/workspace    # 配置Gateway工作目录
```

注意：官方docker镜像的`entrypoint.sh`会将用户切换到`hermes`（id为`10000:10000`），运行`docker run`和`docker exec`时要指定用户，否则可能导致文件权限异常

在已经启动的容器打开TUI：

```bash
docker exec -it --user hermes --workdir /opt/data/workspace hermes /opt/hermes/.venv/bin/hermes
docker exec -it --user hermes --workdir /opt/data/workspace/novelist hermes /opt/hermes/.venv/bin/hermes
```

配置工作目录：在`config.yaml`中写入以下内容（有些教程说配置环境变量`MESSAGING_CWD`，那是旧版本的，已经不能用了）

```yaml
terminal:
  cwd: /your/project/path
```

**上下文管理**

[Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)：Session开始时注入

- `HERMES_HOME/MEMORY.md`，环境、规定，不超过800 token
- `HERMES_HOME/SOUL.md`：用户习惯，不超过500token

[Context Files](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-files)：项目配置

- `HERMES.md`，最高优先级，在git root发现
- `AGENTS.md`，中等优先级，在CWD寻找，读子目录时逐步读取子目录的`AGENTS.md`

[Context References](https://hermes-agent.nousresearch.com/docs/user-guide/features/context-references)

- `@file:path_to_file.py:10-25`：注入文件内容
- `@folder:path/to/dir`：注入目录树
- `@diff, @staged`：注入git diff
- `@git:5`：注入最近5次提交信息
- `@url:https://example.com`：加载网页并注入

## OpenClaw

OpenClaw架构的网关、智能体是独立两部分，可以分开安装。使用[官方脚本](https://docs.openclaw.ai/zh-CN/install)一键安装智能体和网关（使用Ubuntu 2024.04安装）

```bash
# 安装curl（注意不要装snap源的，那个处理隐藏目录时会出问题）
sudo apt install curl

# 安装nvm（因为node.js需要更新）
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash
nvm --version   # 重启终端，然后检查nvm安装是否成功

# 安装node.js 24
nvm install 24
node -v
npm -v

# 安装OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

openclaw --version
openclaw onboard    # 初始化配置。如果安装时做了，可以跳过这一步
openclaw configure  # 全量配置
```

使用：[OpenClaw Gateway](https://docs.openclaw.ai/cli/gateway)

```bash
openclaw gateway       # 启动服务
openclaw gateway stop  # 停止服务
openclaw gateway status

openclaw dashboard     # 在浏览器打开dashboard
openclaw tui           # 命令行对话
```

开放外部访问：配置`~/.openclaw/openclaw.json`

```json
{
  "gateway":
    "bind": "lan",   // 监听0.0.0.0
    "controlUi": {
      "allowInsecureAuth": true,            // 允许http连接
      "dangerouslyDisableDeviceAuth": true  // 允许外部连接
    }
}
```

接入微信。参考：[openclaw-weixin](https://github.com/Tencent/openclaw-weixin/blob/main/README.zh_CN.md)

```bash
openclaw channels list --all

# 一键安装微信插件
npx -y @tencent-weixin/openclaw-weixin-cli@latest install

# 手动安装
openclaw channels add  # 选择微信并安装
openclaw config set plugins.entries.openclaw-weixin.enabled true  # 启用插件
openclaw channels login --channel openclaw-weixin                 # 扫码登录
```

## Astrbot

https://github.com/AstrBotDevs/AstrBot/blob/master/README_zh.md

https://docs.astrbot.app/what-is-astrbot.html

使用uv部署

```bash
uv tool install astrbot --python 3.12
astrbot init # 仅首次执行此命令以初始化环境
astrbot run
```

然后访问http://127.0.0.1:6185

仪表盘网页白屏，F12显示`Failed to load module script: Expected a JavaScript-or-Wasm module script but the server responded with a MIME type of "text/plain"`，把注册表`\HKEY_CLASSES_ROOT\.js`的Content Type改成`application/javascript`

## aibeat

https://github.com/tophant-ai/aibeat

```bash
# 在软件根目录执行运行前检查
./bin/promptbeat --version
./bin/promptbeat validate --config examples/llm-basic/promptbeat.yaml

# 如果提示找不到python，是因为软链接错误
cd runtime/venv/bin
sudo rm python3
sudo ln -s ${软件根目录}/runtime/python/bin/python3
```



# AI模型

## Ollama

```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 管理模型。可用模型：https://ollama.com/library
model="deepseek-r1:1.5b"
ollama pull $model
ollama list
ollama rm $model

# 进行推理
ollama serve       # 开启服务。访问http://127.0.0.1:11434/api/tags，应该能看到模型信息
ollama run $model  # TUI对话

# 接入服务
ollama launch openclaw --model qwen3:0.6b  # 接入OpenClaw并设为默认
```

模型文件保存位置：`%USERPROFILE%\.ollama\models`（Windows），`/usr/share/ollama/.ollama/models`（Linux），`~/.ollama/models`（MacOS），或通过`OLLAMA_MODELS`环境变量指定

启用远程访问：

```bash
# 监听0.0.0.0：在 [Service] 下写入 Environment="OLLAMA_HOST=0.0.0.0:11434"
systemctl edit ollama.service

# 重启服务
systemctl daemon-reload
systemctl restart ollama
```

**性能需求估算**

模型本体的显存占用：BF16精度，每十亿参数需要2GB显存；Q8每需要1 GB；Q4需要0.5 GB。在此基础加上30%~40%余量。普通推理建议Q4

配置KV Cache精度：`OLLAMA_KV_CACHE_TYPE=q8_0`

## whisper

语音识别

https://github.com/openai/whisper

```shell
# 安装
pip install openai-whisper
sudo apt install ffmpeg    # whisper依赖ffmpeg

python -m whisper --help
python -m whisper "src.mp4" --language zh
```

首次使用时需要下载模型，会自动下载并放在`%USERPROFILE%/.cache/whisper`

其他常用参数：

- 输出：`--output_dir 输出目录`， `--output_format {txt,vtt,srt,tsv,json,all}`
- 线程：`--threads `

# 钓鱼

## EwoMail邮件服务器

1. 官方安装脚本：http://doc.ewomail.com/docs/ewomail/install。由于CentOS仓库过期、部分官方资源过期，很容易出问题。官方脚本必须在干净系统上安装，假如安装中途失败（尤其是安装mysql后发生问题），就要重装系统从头开始，因此不建议在真机上装
2. Docker安装：https://github.com/tangramor/ewomail-docker。mysql要降版本（仓库内的compose.yml使用了`default-authentication-plugin`，当前版本已经不再支持，要降到`mysql:8.0.26`）。启动后CPU、磁盘占用极高，导致服务器卡死，怀疑是ClamAV组件发力了
3. 在CentOS的Docker容器安装：https://github.com/en0th/EwoMailForDocker。在CentOS的Docker容器内用官方脚本安装成功

```bash
# 构建镜像
docker build -t ewomail:v1 .;

docker run -itd --name ewomail --privileged=true \
  -p 7000:7000 -p 7010:7010 -p 25:25 -p 143:143 -p 993:993 \
  -p 995:995 -p 587:587 -p 110:110 -p 465:465 -p 8020:8020 \
  -p 8000:8000 -p 8010:8010 ewomail:v1;

docker exec -it --privileged ewomail /bin/sh
```

然后在容器内进行安装。安装前需要解决的问题有：

1. `sh: setenforce: command not found`：容器没有`setenforce`指令。注释掉start.sh的setenforce一行
2. 如果带`en`参数安装（`start.sh xxx.com en`），安装脚本会从`http://download.ewomail.org`下载rpm包，而这个网站已经不在了，因此不能带`en`参数
3. 如果不带`en`参数（`start.sh xxx.com`），安装脚本的`epel_replace`函数会换到北师大源，导致安装失败，因此需要删掉`epel_replace`函数的内容
4. yum源失效：换阿里云镜像

```bash
# 按照1~3要求编辑/root/install/start.sh

# 换阿里云镜像
curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
yum clean all
yum makecache

# 运行安装脚本
cd /root/install
/bin/bash -x start.sh xxx.com  # 替换为服务器主域名。若不需要收信，可以随便填

# 若没有真正的域名，可以添加host记录方便测试和本机访问
echo '127.0.0.1   mail.xxx.com smtp.xxx.com imap.xxx.com' >> /etc/hosts
```

- 邮箱管理后台：http://127.0.0.1:8010 （默认账号admin，密码ewomail123。务必登上去改密码）
- 邮件系统：http://127.0.0.1:8000
- web数据库管理：https://127.0.0.1:8020（账号密码在`/ewomail/config.ini`）
- https的管理后台、邮件系统：7010和7000端口
- 其他监听端口：25、143、993、995、587、110、465

## Gophish

Docker安装

```bash
docker pull gophish/gophish
docker run -itd --name gophish -p 3333:3333 -p 8003:80 -p 8004:8080 gophish/gophish
```

- https://127.0.0.1:3333：后台访问端口。`docker logs gophish`查看初始密码
- http://127.0.0.1:8003：钓鱼页面端口。容器的80端口

### 邮件发送配置

Sending Profile - New

使用EwoMail转发：

- Name：随意
- SMTP From：发件人邮箱。要和Username相同
- Host：`IP地址:25`，通过SMTPS协议提交邮件
- Username：邮箱名
- Password：Ewomail登录密码

QQ邮箱代发：

- Name：随意
- SMTP From：发件人邮箱。必须和Username相同。可以用`虚假发件人<真实邮箱>`部分伪装
- Host：`smtp.qq.com:465`
- Username：QQ邮箱名
- Password：授权码。登录QQ邮箱，设置 - 账号与安全 - 安全设置 - POP3/IMAP/SMTP服务 - 获取授权码

填好之后，可以在Send Test Email发送测试邮件。Email字段写收件人邮箱，其余随便写

### 邮件模板

Email Templates- New。可以用Import Email，在邮箱查看邮件原文，复制粘贴到Email Content栏即可（处理中文可能出问题）。Envelope Sender可以留空，采用Sending Profile的设置

邮件内容的钓鱼页面链接写`{{.URL}}`；勾选Add Tracking Image会在邮件底部加一张隐藏图片，用来检测哪些用户点开了邮件

邮件中加入`{{.Tracker}}`似乎也能插入检测图片？

### 钓鱼页面

Landing Page - New。可以用Import Site直接导入网站外观，但是容易出问题，建议保存网页（Ctrl + S或者用Save Page WE等浏览器插件均可）、手动编辑之后再上传

网页内表单的Action必须为空：`<form method="post" action="">`

将页面粘贴到文本框内，勾选Capture Submitted Data和Capture Passwords，记录上钩的人提交的表单；Redirect to链接则是提交表单之后跳转的页面

### 邮箱列表

User & Groups - New Group

### 进行钓鱼

Campaigns - New Campaign，其中URL是钓鱼页面URL，使用Docker部署时默认在`http://本机IP:8003`



**钓鱼思路和实施**

链接：自带统计和数据收集功能

附件：可以用下载链接

二维码：不能给不同邮件添加不同二维码，因此无法直接统计。可以考虑弄一个生成二维码链接的服务，如插入`<img src="https://gen-qrcode.com/{{.URL}}">`这样的图片

## vShell

远控平台

```bash
# 修改配置
vim conf/settings.conf

# 运行权限
chmod +x v_linux_amd64

# 启动
nohup ./v_linux_amd64
```

然后访问8082端口（或者settings.conf里面配的端口）
