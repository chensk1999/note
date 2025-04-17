Shell指用户界面，与内核（Kernel）相对。此笔记中，Shell专指操作系统的命令行界面（Command-Line Interface，CLI）

# Bash

Bash是最常见的Unix Shell，它能运行于Linux系统和MacOS；Windows10安装了Linux子系统之后也可以使用Bash

虽然Bash很常见，但Linux系统下运行的命令行界面不一定是Bash。`echo $SHELL`可以看见当前用的Shell，`cat /etc/shells`可以看已安装的Shell。常见的Shell有

| 分类             | Shell                    |
| ---------------- | ------------------------ |
| Bourne Shell家族 | sh, bash, dash, ksh, zsh |
| C Shell家族      | tcsh, csh                |

幸运的是，这些Unix Shell的指令基本一致，语法也只是分为两派，两个家族内部的语法高度相似

## 指令

```bash
# 简单指令
# 管道（Pipeline）
# 指令序列
```

## 变量

bash变量没有类别，一切都是字符串

### 自定义变量

变量基本使用

```bash
a=1       # 定义变量。注意不能加空格
b="str b" # 如果变量值有空格，需要用双引号括起来
c="price is \$100"  # "$"等特殊符号需要反斜杠转义

echo $a           # 访问变量。在变量名前面加上$
echo "a = $a"     # 字符串中的变量也会自动格式化为变量的值
echo "${a}_file"  # 变量名和其他字符连用，可以用花括号
```

数组和关联数组

```bash
# 数组
arr=(1 2 3)
echo ${arr[0]}   # 数组索引
echo ${arr[@]}   # 数组所有元素
echo ${#arr[@]}  # 数组长度
arr+=(4)  # 添加元素

# 关联数组
declare -A dict
dict[apple]=red
dict[banana]=yellow
# 遍历字典
for key in "${!my_dict[@]}"; do
  echo "$key -> ${my_dict[$key]}"
done
```

变量默认值

```bash
echo ${var:-0}    # 若变量不存在，输出默认值（此例子中为0）
echo ${var:=0}    # 若变量不存在，输出默认值，并将变量设为默认值
echo ${var:?undefined}    # 若变量不存在，报错
```

### 环境变量

许多系统配置、应用配置存储在环境变量内，它们一般在脚本中定义，很少需要在shell中更改

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
- 后台异步命令的进程ID`$!`
- 脚本参数数量`$@`；脚本参数值`$#`

## 控制流

```bash
# 遍历当前目录所有文件
for f in *; do
  echo "File -> $f"
done

# 正则表达式替换
# "${src/pattern/rep}"，将src变量中匹配pattern的都替换成rep
a='Hello, world'
f='example.png'
echo "${a/o/O}"       # 匹配第一个，得到HellO, world
echo "${a//o/O}"      # 匹配全部，得到HellO, wOrld
echo "${f/%png/txt}"  # 匹配最后一个，得到example.txt
```

# cmd

cmd也叫命令提示符（Command Prompt），是Windows家族许多操作系统(Windows 2000，XP，Vista等）的默认Shell

## 变量

```cmd
REM 定义、访问变量
set a=1
echo %a%
```





# PowerShell

Powershell主要用于Windows 7及其后续版本，也可以运行于Linux和MacOS

## 基础知识

PowerShell不区分大小写。其指令称作cmdlet（Command-Let），命名一般格式是`verb-noun`。大部分系统cmdlet都有别名，比如，`Write-Output`指令具有别名`echo`

使用参数时可以简化，能唯一识别即可，如，-common参数可以只输入-com（假设没有其他形参含有com），到这一步之后也可以用tab自动补全

**流水线(pipeline)**

```命令1 | 命令2```会将命令1的结果作为命令2的参数

```命令2 (命令1)```也有同样效果

## 语法

### 变量

```powershell
# 标量
$i = 1

# 列表 （Array）
$arr = @(1, 2, 3, 4)    # @()可以省略
# 访问列表元素
$arr[0]
$arr[1, 2]
$arr[2..-1]
$arr.count

# 哈希表
$hash = @{a=1; b=2; c=3}
echo $hash.a

# 对象（Ojbect）
# 大部分指令的返回值都是对象或者对象的列表
$obj = Get-ChildItem
$obj.fullname
Get-ChildItem | Get-Member  # 查看所有属性与方法
Get-ChildItem | Select-Object FullName, Length  # 选择获取的列
```

### 运算符

加减乘除之类的都正常。注意，除法是浮点除法

```powershell
1 -gt 0     # 大于。注意，>是重定向运算符
1 -band 3   # 位运算。类似有-bor, -bxor等
1 -shl 1    # 左移。右移是-shr
```

**重定向**

```powershell
Write-Output "Hello" > script.log   # 写入文件
Write-Output "World" >> script.log  # 追加到文件
Write-Warning "warn" *> script.log  # 将所有流（比如，Error和Warning）重定向到文件
```

用`Out-File` cmdlet有更多参数

**管道**

### 控制流

```powershell
$arr = 1..100

# for循环
$sum = 0
for ($i=0; $i -lt 100; $i++) {
    $sum += $arr[$i]
}

# foreach循环
$sum2 = 0
foreach ($item in $arr) {
    $sum += $item
}

# Foreach-Object指令。$PSItem是默认迭代变量，也可以用$_
$sum3 = 0
$arr | Foreach-Object {
    $sum3 += $PSItem
}

# foreach方法
$sum4 = 0
$arr.foreach({$sum4 += $PSItem})
```

## 常用指令

```powershell
# 输出到文件（以Get-Process为例）
Get-Process | Out-File filename.txt
Get-Process | Export-Csv filename.csv
Get-Process | Export-Clixml filename.xml
```

## 其他

```powershell
# 格式化字符串
$name = "whatever"
$prefix = "a"
$s = [string]::Format("{0}-{1}.png", $prefix, $name)
$s2 = "{0}-{1}.png" -f $prefix, $name

# 转义字符`（反引号）
echo "`"Hello`""
```

### 执行策略

Powershell执行策略控制哪些脚本可以运行。它有以下几个等级

- Restricted：不允许运行脚本（默认策略）
- AllSigned：允许有数字签名的脚本
- RemoteSigned：允许有数字签名的脚本、本地编写的脚本
- Bypass：允许所有脚本且不警告

建议设置为RemoteSigned

```powershell
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned  #可能需要以管理员身份运行
```

# 常用指令

## 文件与目录

| Unix Shell   | cmd        | Powershell    | 说明           |
| ------------ | ---------- | ------------- | -------------- |
| ls, find     | dir        | Get-ChildItem | 列出文件和目录 |
| cat          | type       | Get-Content   | 读取文件内容   |
| cp           | copy       | Copy-Item     | 复制           |
| mv           | move       | Move-Item     | 移动           |
| rm, rmdir    | del, rmdir | Remove-Item   | 删除           |
| mv           | rename     | Rename-Item   | 重命名         |
| touch, mkdir | mkdir      | New-Item      | 新建           |
| pwd          | cd         | Get-Location  | 获取工作路径   |
| cd           | cd         | Set-Location  | 设置工作路径   |

注：Powershell大多数命令都设置了别名，用Unix Shell或者cmd.exe的命令名一般也能运行

## 网络

## curl - Web请求

```shell
curl example.com
```

[Curl指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)，[Curl Cookbook](https://catonmat.net/cookbooks/curl)

## netstat - 网络状态

查询网络状态，如当前建立的连接、路由表

| 选项 | 作用                                                    |
| ---- | ------------------------------------------------------- |
| a    | 显示所有连接                                            |
| b    | 显示各端口对应程序名。需要root权限                      |
| n    | 显示IP地址而非域名/主机名。不加n好像会做反向DNS，很耗时 |
| o    | 显示对应进程PID                                         |
| p    | 指定协议，如`netstat -p "tcp"`                          |
| r    | 显示路由表                                              |

```shell
netstat -ano        # 显示所有连接以及对应进程PID
netstat -nop "tcp"  # 显示所有tcp连接，以及对应进程PID
netstat -r          # 显示路由表
netstat -no | findstr "8080"  # 查找指定端口的连接
```

## nslookup - DNS查询

DNS查询。`nslookup 域名 [DNS服务器]`；也可以不带参数运行，则进入交互式界面

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
