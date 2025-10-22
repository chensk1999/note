参考：[Linux 101](https://101.lug.ustc.edu.cn/)

# Linux简介

## 起源

1969年，美国AT&T公司的贝尔实验室开发了UNIX操作系统，并在此后的 10 年里在学术机构和大型企业中得到了广泛的应用。在这段时间，许多计算机从业者开发了很多基于UNIX的变种，统称为“类UNIX操作系统”。然而后来AT&T公司决定改变商业策略，将代码闭源，并声明拥有类UNIX操作系统的著作权

1983年9月27日，理查德·斯托曼（Richard Stallman）在麻省理工学院发起了GNU计划，它的目标是创建一套类似UNIX但完全自由的操作系统。数年后，林纳斯·托瓦兹（Linus Torvalds）在他的大学时期编写并发布了自己的操作系统，也就是后来所谓的 “Linux内核”

Linux内核过于精简，并不是一个完整的操作系统。许多自由软件社区的开发人员和一些计算机商业公司便开始把各种组件添加到这个内核之上，这才构建成了一个完整的Linux操作系统。开源社区的诸多成员以及许多商业公司的去中心化的贡献，让Linux充满了多样性。基于Linux内核构造出来的操作系统称为“Linux发行版”

**省流**：Linux是Unix的精神续作，Linux内核+组件（组件有很多人在做，没有统一版本）构成Linux发行版。市面上有五花八门的Linux发行版，Ubuntu、CentOS、ArchLinux等都是Linux发行版

**补充（现代操作系统的功能）**：进程管理、内存管理、文件系统、网络通信、安全机制、用户界面、驱动程序

## 用户界面

用户操作计算机时，必须有一个“中介”将用户的鼠标动作、键盘输入“翻译”为对操作系统的指令，这一工具称作用户界面（User Interface），也叫做Shell，与操作系统内核（Kernel）相对。最早的Shell是通过键盘输入指令的**命令行界面**（Command-Line Interface，CLI），狭义的Shell专指命令行界面；后来又出现了以鼠标操作为主的**图形用户界面**（Graphical Shell，又称Graphical User Interface，GUI）

图形界面的学习成本低，因此占据了主流。但是，命令行可以使用自动化脚本执行重复任务、方便远程控制、节约资源，最重要的是许多系统维护工具只有命令行界面，没有图形界面（原因也很好理解，设计图形界面比命令行界面麻烦太多太多了）

Linux最常见的Shell是Bash，也有的发行版会使用zsh等Shell，可以用`echo $SHELL`查看当前Shell，`cat /etc/shells`查看已安装的Shell（绝大部分Shell语法相同，一般不必在意正在使用哪个Shell）。通常通过在终端（Terminal）中输入指令来操作Shell

本笔记各节都附带相关Bash指令，Bash语法一节将详细解释Bash语法以及脚本编写。遇到不理解的指令可在[Explain Shell](https://www.explainshell.com/)网站查询

# Bash语法

## 重定向与管道

Bash通常从终端接受输入，并将输出打印到终端，而重定向运算符将输入和输出的位置更改到其他文件。需要注意的是，Linux的设计思想是将设备视作文件，终端就是这么被Bash当作若干个文件来读写的；重定向除了可以把输出写入文件，还可以传给其他应用、通过网络发送、直接丢弃，等等

```bash
grep "txt" < file1.txt > file2.txt  # 将file1.txt作为grep指令的输入，匹配后输出到file2.txt
```

### 重定向

[GNU文档](https://www.gnu.org/software/bash/manual/html_node/Redirections.html)

重定向其实是对文件描述符（File Descriptor）的操作。文件描述符是进程为文件分配的编号，效果类似于文件指针。`stdin`的描述符是0、`stdout`为1、`stderr`为2；3~9一般由用户定义。需要注意，不同描述符可以指向同一文件；不同进程的同一描述符可以指向不同文件

**输入重定向**：`n< file`，将文件内容写入n号描述符

```bash
grep "txt" < file.txt   # 省略n时默认重定向到0，即stdin
```

**输出重定向**：`n> file`，本来要写入n号描述符的内容改为写入文件

```bash
ls >  file       # 省略n时取n=1，即stdout。将stdout写入文件
ls 2> /dev/null  # 将stderr重定向到/dev/null（即丢弃掉）
ls &> file       # 将stdout和stderr都重定向到file
ls >> file       # >>表示向文件末尾添加（>则会覆盖文件）
```

**复制文件描述符**：`n>&m`，本来写入n号描述符的改为写入m号描述符

```bash
ls 1>filelist 2>&1
ls 2>&1 1>filelist
```

注意，顺序很重要。可以把重定向当作赋值形象理解：前一种情况，`$1 = filelist; $2 = $1;`，结果是`$1`和`$2`都被改为`filelist`文件，全部内容写入文件；后一种，`$2 = $1; $1 = filelist;`，结果是错误信息写入stdout，输出写入文件

**打开与关闭文件**

```bash
3<>tmp.txt  # 打开tmp.txt，文件标识符为3
<&3-        # 关闭3号文件标识符
```

重定向时经常使用一些**特殊文件**：

| 路径        | 说明                   |
| ----------- | ---------------------- |
| `/dev/null` | 空文件，常用于丢弃输出 |

### 管道

管道符`|`将前一个命令的输出作为文件传给第二个命令

```bash
ls -l | grep ^d  # 将ls列出的文件信息传给grep筛选。此命令的效果是筛选出当前目录的全部文件夹
```

还有一些类似的：

```bash
clear; ls                    # 结束符;，一行的若干命令相继执行
cat filelist.txt && ls -l    # 组合符&&，若前一个命令成功，继续执行后一个
mkdir foo || mkdir bar       # 组合符||，若第一个命令失败，则执行后一个
```

## 变量

bash变量没有类别，一切都是字符串

### 自定义变量

变量基本使用

```bash
a=1       # 定义变量。注意不能加空格
b="str b" # 如果变量值有空格，需要用双引号括起来
c="price is \$100"  # "$"等特殊符号需要反斜杠转义

echo $a           # 访问变量。详见“Shell扩展 - 参数扩展”
```

变量扩展（详见Shell扩展）

```bash
echo $a      # "$变量"替换为变量值
echo 'a=$a'  # 单引号中的不会替换
echo "a=$(cat flag.txt)" # $()执行指令
echo "a=`cat flag.txt`"  # 反引号执行指令

# 正则表达式替换
# "${src/pattern/rep}"，将src变量中匹配pattern的都替换成rep
a='Hello, world'
f='example.png'
echo "${a/o/O}"       # 匹配第一个，得到HellO, world
echo "${a//o/O}"      # 匹配全部，得到HellO, wOrld
echo "${f/%png/txt}"  # 匹配最后一个，得到example.txt
```

数组和关联数组

```bash
# 数组
arr=(1 2 3)
echo ${arr[0]}   # 数组索引
echo ${arr[@]}   # 数组所有元素
echo ${#arr[@]}  # 数组长度
arr+=(4)  # 添加元素
# 遍历数组
for a in ${arr[@]}; do
  echo $a
done

# 关联数组
declare -A dict
dict[apple]=red
dict[banana]=yellow
# 遍历字典
for key in "${!my_dict[@]}"; do
  echo "$key -> ${my_dict[$key]}"
done
```

### 环境变量

每个用户登录系统后，Linux 都会为其建立一个默认的工作环境，将许多系统配置、应用配置存储在环境变量内。用户可以通过修改这些环境变量，来定制自己工作环境（但一般在脚本中定义，很少需要在shell中更改）

```shell
env       # 打印所有环境变量
set       # 打印所有环境变量、用户定义的变量
export PATH=$PATH:/home/username/mysql/bin  # 环境变量赋值
```

环境变量一般在下列文件中定义（列出若干常见的，具体用哪个取决于系统版本）。打开shell时自动运行这些文件，因此在其中加入`export ENV_VAR=VALUE`这样的代码，就会在每次打开shell时载入环境变量。系统环境变量的文件也可能是用户登录时运行

1. 系统环境变量：`/etc/environment`，`/etc/profile`，`/etc/bash.bashrc`
2. 用户环境变量：`~/.profile`，`~/.bashrc`

### 特殊变量

- 上一个命令：退出码`$?`；最后一个参数`$_`
- 当前shell：进程ID`$$`；名称`$0`；启动参数`$-`
- 后台异步命令的进程ID：`$!`
- 脚本参数：脚本文件名`$0`；第一至第九个参数`$1-$9`；脚本参数总数`$#`

## 控制流

```bash
# 遍历当前目录所有文件
for f in *; do
  echo "File -> $f"
done
```

## Shell扩展

处理指令时，Bash首先将一条指令拆分为若干Token，例如`ls /var`拆分为`["ls", "/var"]`；然后，对每个Token进行Shell扩展（Shell Expansion），扩展执行次序如下。参考：[GNU Bash Reference Menu](https://www.gnu.org/software/bash/manual/bash.html#Shell-Expansions)

1. 大括号扩展（Brace Expansion）：`{a,b,c}.txt` → `a.txt b.txt c.txt`
2. 波浪线扩展（Tilde Expansion）：`~` → `$HOME`
3. 参数扩展（Parameter Expansion）：`$a` → 变量a的值
4. 命令替换（Command Substitution）：`$(command)`，反括号括起来的命令 → 命令执行结果
5. 算数扩展（Arithmatic Expansion）：`$((1+1))` → 表达式计算结果
6. 进程替换（Process Substitution）：`<(进程名), >(进程名)` → 该进程的输入输出的文件名
7. 词切割（Word Splitting）：使用`$IFS`作为分隔符，拆分不在双引号中的参数扩展、命令替换和算数扩展结果
8. 文件名扩展（Filename Expansion）：`*, ?, []` → 文件名
9. 引号移除（Quote Removal）：移除多余反斜杠、单引号 、双引号

### 参数扩展

```bash
a="Hello"
echo $a           # $ + 变量名，扩展为变量的值
echo "a = $a"     # 双引号字符串中变量一样扩展
echo "${a}_file"  # 变量名和其他字符连用，可以用花括号分隔
echo '$a'         # 单引号不会扩展

# 变量默认值
echo ${var:-0}    # 若变量不存在，扩展为默认值（此例子中为0）
echo ${var:=0}    # 若变量不存在，扩展为默认值，并将变量设为默认值
echo ${var:?undefined}    # 若变量不存在，报错
```

### 模式扩展

不在单引号、双引号中的`*, ?, []`字符都会进行模式扩展（Filename Expansion，俗称Globbing），替换为实际存在的文件名

```bash
ls ?.txt     # ? = 单个字符
ls *.txt     # * = 任意个字符
ls [ab].txt  # [] = 其中任意字符
ls [^a].txt
ls [a-z].txt
ls [[:xdigit:]] # 字符类。例子是十六进制字符
```

## 其他

### 脚本

第一行指定使用的解释器

```bash
#! /bin/bash
#! /usr/bin/env bash
```

执行脚本：

```bash
. ./script.sh    # 用句点表示执行脚本。注意，必须是脚本路径，不能是文件名，否则bash找不到
source script.sh # 句点的别名
```

# 文件、用户和权限

## 文件系统

Linux全部文件从根目录`/`开始，组织为树状，磁盘分区挂载（mount）在树上；计算机设备也抽象为文件的形式挂在树上。大部分发行版的文件结构遵循文件系统层次结构标准（FHS, Filesystem Hierarchy Standard）

**系统文件**

| 目录    | 含义     | 说明                                 | 举例                      |
| ------- | -------- | ------------------------------------ | ------------------------- |
| `/bin`  | Binaries | 系统命令                             | `ls`，`cp`                |
| `/etc`  | Etcetra  | 系统配置文件                         | 用户账号信息`/etc/passwd` |
| `/dev`  | Device   | 设备文件，即被抽象为文件的计算机设备 | 硬盘`/dev/sda`            |
| `/mnt`  | Mount    | 临时挂载的其他文件系统               | 光驱                      |
| `/proc` | Process  | 进程的伪文件，是系统内存的映射       |                           |
| `/lib`  | Library  | 各种程序使用的动态链接库             |                           |
| `/boot` | Boot     | Linux系统启动时使用的核心文件        |                           |

**其他**

| 目录    | 含义                  | 说明                                               | 举例       |
| ------- | --------------------- | -------------------------------------------------- | ---------- |
| `/home` | Home                  | 用户主目录                                         |            |
| `/usr`  | Unix System Resources | 各种程序、文档、头文件、库文件（应该是Unix的遗产） |            |
| `/var`  | Variable              | 经常变动的文件                                     | `/var/www` |
| `/srv`  | Service               | 网络服务文件                                       | `/srv/ftp` |
| `/opt`  | Optional              | 可选软件安装目录，通常装第三方商业软件             |            |
| `/tmp`  | Temp                  | 临时文件。其中文件用完就删，重启时会被清空         |            |

文件目录中，有若干文件夹结构和根目录很类似，例如，`/usr`下面也有`/usr/bin`，`/usr/lib`等目录。安装程序时一般按用途装到这些位置：

- `/bin`：操作系统命令
- `/usr/bin`：使用包管理器安装的程序
- `/usr/local/bin`：用户手动安装的程序

完整安装位置和搜索顺序可以查看`$PATH`环境变量

## 用户与用户组

- 超级用户：用户名为root，ID为0。大部分Linux发行版禁止使用root登录。拥有所有文件的权限，可管理所有进程
- 普通用户：用户ID为500以上 / 1000以上，取决于版本。home目录是`/home/username`（每个普通用户拥有自己home目录的文件权限。登录后可以用`~`指代自己的home目录），只能操作自己启动的进程。可以通过`sudo`指令临时获得root权限
- 系统用户：ID为1~499 / 100~999，不能登录，一般由系统服务使用。此类用户文件、指令操作权限都有严格限制，旨在防止服务受攻后获取过高权限

此外，Linux还用用户组管理权限，用户组的成员享有某些权限。比如使用docker时，可以把自己加入 `docker` 用户组，从而不需要使用 `root` 权限，也可以访问它的接口

```bash
# 查看用户与权限
id               # 查看当前用户名、uid、用户组和gid
whoami           # 查看当前用户名
cat /etc/passwd  # 查看用户列表。每行内容为用户名:密码占位符:用户ID:组ID:注释:主目录:登录Shell

# 查看用户组
groups           # 查看当前用户组
cat /etc/group   # 查看用户组列表

# 编辑用户组
sudo groupadd $group_name
sudo usermod -aG $group_name $USER   # 添加成员
newgrp $group_name                   # 登录新加入的组
```

### sudo

sudo，全称Super User DO，允许普通用户以其他用户权限执行指令。常用sudo暂时获取root用户权限进行操作：`sudo <需要root权限的指令>`

sudo配置存储在`/etc/sudoers`文件中，可用`sudo visudo`编辑配置。`sudo -l`可以查看当前用户的配置，它的输出是`(用户) 配置 命令`，例如`(root) NOPASSWORD /usr/bin/bash`表示可以以root权限无需输入密码执行`bash`，`(ALL:ALL) ALL`表示可以以任意用户、任意用户组权限执行任意命令

## 文件权限

在 Linux 中，每个文件和目录都有自己的权限，其权限由12个标志位控制

```
+----------------------+-------+-------+-------+
|         11-9         |  8-6  |  5-3  |  2-0  |
+----------------------+-------+-------+-------+
|       Special        | User  | Group | Other |
+----------------------+-------+-------+-------+
| SUID | SGID | Sticky | r,w,x | r,w,x | r,w,x |
+----------------------+-------+-------+-------+
```

- 11-9比特：特殊标志位
  - SUID：全称Set User Identity，执行`SUID=1`的文件时，暂时获取文件所有者的权限
  - SGID：全称Set Group Identity，执行`SGID=1`的文件时，暂时获得文件所属用户组的权限
  - Sticky：也叫Sticky bit，若目录设置`Sticky=1`，则改目录下的文件只有各自的属主可以删除
- 8-6比特：文件所有者（**U**ser）的权限。包括读（**R**ead）、写（**W**rite）、执行（e**X**ecute）。拥有文件执行权限就可以将它作为程序代码执行，拥有目录执行权限就可以查看这个目录下有什么文件
- 5-3比特：文件所属用户组（**G**roup）的权限
- 2-0比特：其他用户（**O**ther）的权限

### 查看权限

可以使用 `ls -l` 查看文件权限

```bash
$ ls -l
total 8
-rwxrw-r-- 1 root root   40 Feb  3 22:37 a_file
drwxrwxr-x 2 root root 4096 Feb  3 22:38 a_folder
```

第一列的字符串从左到右意义分别是

- 第一位：文件类型，`-`为文件，`d`为目录，`l`为符号链接
- 第二~四位：文件所有者的权限
- 第五~七位：文件所属用户组的权限
- 第八~十位：其他人的权限

第三、四列为文件所有者和用户组。可以使用 `chmod` (**ch**ange file **mod**e bits) 修改权限，`chown` (**ch**ange file **own**er) 修改文件所有者

### 更改权限

`chmod`指令可以更改文件权限

```shell
chmod g+w main.py
chmod o-rwx file_name
```

其中`g+w`表示向用户组成员授予写权限，`o-rwx`表示撤销其他用户的读、写、执行权限。这个参数由“Who What Which”三部分组成：

- `ugoa`：修改谁的权限。四个字母分别表示所有者（User）、用户组（Group）、其他用户（Other）、全部（All）
- `+=-`：如何修改权限。`+`授予权限，`-`撤销权限，`=`设置权限
- `rwxst`：修改哪些权限。分别是读、写、执行、SUID / SGID、Sticky

此外还可以用三位或四位数字表示权限。每位数表示3比特

```bash
chmod 777 main.py  # 授予所有用户读、写、执行权限
chmod 4755 main.py # 设置SUID=1，并授予文件属主rwx权限，授予用户组、其他用户读与执行权限

# 补充：修改目录下全部文件（Recursive）
chmod -R u+rwx dir_name
```

## 文件操作指令

```bash
# 文件
cat file.txt    # 显示文件内容
less file.txt   # 分页显示，操作类似vim

# 目录
cd ..   # change directory
ls -li  # list
pwd     # print working directory
```

其他常用命令：`cp`复制，`mv`移动，`rm`删除，`mkdir`创建目录，`touch`创建文件

`find`指令可用于搜索文件，它的语法是`find [路径] [搜索条件]`。完整文档可参考[Linux Manual](https://man7.org/linux/man-pages/man1/find.1.html)，下面列出常用参数

```bash
find ~ -name *.pdf -size +1M    # 在用户home目录下搜索名字以.pdf结尾、大小超过1MB的东西
find ~ -name adb* -type f,d     # 在用户home目录下搜索名字以adb开头的文件、目录
find / -name file | grep -v "Permission denied"  # 搜根目录的时候可以过滤掉看不到的目录
find / -name file 2>/dev/null                    # 另一种过滤方式。原理是不显示报错信息
find ~ -type f -exec file {} \; # 对每个找到的文件执行命令。{}是文件名占位符，\;表示命令结束
```

# 包管理器

[参考](https://www.digitalocean.com/community/tutorials/package-management-basics-apt-yum-dnf-pkg)

| 发行版         | 管理器    | 备注 |
| -------------- | --------- | ---- |
| Debian, Ubuntu | dpkg, apt |      |
| CentOS         | rpm       |      |
| CentOS 6, 7    | yum       |      |
| CentOS 8       | dnf       |      |
| FreeBSD        | pkg       |      |

换源、镜像：修改`/etc/apt/sources.list`，并添加公钥文件

`sudo wget https://archive.kali.org/archive-keyring.gpg -O /usr/share/keyrings/kali-archive-keyring.gpg`

# 其他指令

## systemctl - 系统服务

`systemctl`指令与后台的`systemd`交互，管理系统服务。以`nginx`服务器为例

```bash
sudo systemctl start nginx    # 开启服务
sudo systemctl stop nginx     # 终止服务
sudo systemctl status nginx   # 查看服务状态

sudo systemctl enable nginx      # 设置开机自动启动
sudo systemctl disable nginx     # 取消开机自动启动
sudo systemctl is-enabled nginx  # 检查是否启用自动启动

systemctl list-units --type=service       # 当前运行的服务
systemctl list-unit-files --type=service  # 所有服务及其启用状态
```

老版本可能需要使用`service`命令

## openssl - SSL / TLS加密

**passwd**：生成密码。下面例子使用SHA256算法、以`salt`为盐计算123456的哈希

```bash
openssl passwd -6 -salt salt 123456
```

**x509**：CA证书

```bash
# 格式转换
openssl x509 -in cert.crt -inform pem -out cert.der -outform der
# 计算哈希值
openssl x509 -in cert.pem -inform PEM -subject_hash
```

**s_client**：TLS客户端。`openssl s_client -connect $ip:$port`。加上参数`quiet`隐藏握手等信息

## SSH

```bash
ssh -p 22 $user@$ip
```

密钥登录

1. 生成密钥：`ssh-keygen`，私钥存储在`~/.ssh/id_rsa`，公钥存储在`~/.ssh/id_rsa.pub`
2. 在服务器上安装公钥：`cat id_ras.pub >> ~/.ssh/authorized_keys`
3. 配置`/etc/ssh/sshd_config`，开启`RSAAuthentication`，`PubkeyAuthentication`。还可以禁用`PasswordAuthentication`
4. 重启SSH：`service sshd restart`
5. 使用私钥登录：`ssh -i $key_file $user@$ip`

## 打印二进制文件hex值

**hexdump**

```bash
hexdump -v -e '30/1 "%02x" "\n"' example.png > example.txt
# -v: 遇到两行相同的不把后面的行省略为*号
# -e：输出格式。说明：读取30个1字节的数据，以%02x格式打印，然后打印一个换行符。此格式和xxd的plain格式相同
```

**xxd**

```bash
xxd -p example.jpg example.txt      # -p: plain hex，不打印offset等东西
xxd -p -r example.txt revert.jpg    # -r: reverse，将hex转bin
```

以上是Unix指令。windows可以用WSL，或者git bash也可以

## 压缩文件

```shell
# tar：归档工具，打包但不压缩数据，后缀.tar
# 常配合其他压缩工具，压缩为.tar.gz, .tar.bz2, .tar.xz等类型
tar -cvf archive.tar dir/   # 打包tar。参数表示create, verbose, file
tar -xvf archive.tar        # 解包tar。参数x表示extract
tar -czvf archive.tar.gz dir/    # 打包并用gzip压缩。参数z表示gzip
tar -xzvf archive.tar.gz -C d2/  # 用gzip解压并解包到目录d2/

# gzip: 单文件压缩工具，后缀.gz
gzip a.tar        # 压缩文件
gzip -l a.tar.gz  # 查看压缩比
gzip -d a.tar.gz  # 解压

# bzip2：压缩工具，后缀.bz2。压缩率比gzip高，速度比gzip慢
bzip2 -d a.bz

# xz：压缩工具，后缀.xz。压缩率比bzip2更高，速度最慢

# zip：打包+压缩工具
zip archive.zip *.txt
unzip archive.zip /to/here/
```

杂项

crontab - 定时执行

`mktemp -d` - 创建临时文件夹
