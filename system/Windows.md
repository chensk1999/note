# PowerShell

Shell指用户界面，与内核（Kernel）相对。它通常专指操作系统的命令行界面（Command-Line Interface，CLI）。Windows系统的Shell主要有命令提示符（Command Prompt，`cmd.exe`）和Powershell。前者是Windows祖传的Shell，可追溯至DOS时代，已经过时，但因为历史包袱仍然有很大作用；Powershell是自Windows 7推出的命令行界面，功能比CMD强大

## 基础知识

与其他Shell相同，PowerShell采用`指令 参数`的方式调用命令。不过，它也可以像现代变成语言一样把指令当作表达式使用

```powershell
Get-ChildItem .          # 列出子目录、子文件
$files = Get-ChildItem   # 将子目录、子文件存入变量$files
    # $files的类型为 Array[DirectoryInfo | FileInfo]
Select-Object FullName -InputObject (Get-ChildItem .)[0] # 甚至可以把指令结果当作变量
```

PowerShell不区分大小写。其指令称作cmdlet（Command-Let），命名一般格式是`verb-noun`。大部分系统cmdlet都有别名，用其他Shell的指令名一般也能运行，比如，`Write-Output`指令具有别名`echo`

使用参数时可以简化，能唯一识别即可，如，-common参数可以只输入-com（假设没有其他形参含有com），到这一步之后也可以用tab自动补全

**重定向与流水线**

和Bash差不多，参见[Linux笔记](./linux.md#重定向与管道)的“重定向与管道”一节。两者区别在于Powershell更接近现代编程语言，把各种东西当作变量和对象处理

```powershell
Get-ChildItem . 2>$null               # /dev/null -> $null
Get-Process | Out-File "process.txt"
```

## 变量

```powershell
# 数值、字符串、布尔值
$i = 1
$s = "Hello, `$i = $i"  # 双引号中的$i会格式化，特殊符号用反斜杠`转义
$s = "$s, $($i + 1)"    # $()会执行其中的语句，并格式化为字符串
$s2 = '$s is $s'        # 单引号中的变量不会格式化。与Bash类似
$b = $true

# 列表 (Array)
$arr = @(1, 2, 3, 4)    # @()可以省略
# 访问列表元素
$arr[0]
$arr[1, 2]
$arr[2..-1]
$arr.count

# 哈希表
$hash = @{a=1; b=2; c=3}
echo $hash.a
```

变量作用域

```powershell
$Global:ip_addr = "192.168.0.1"   # 全局变量，在当前Powershell会话全局可用
$Script:port = "80"               # 脚本变量，当前脚本可用
$Local:username = "admin"         # 本地变量，当前代码块中可用
```

## 对象

```powershell
# 对象 (Ojbect)
# 大部分指令的返回值都是Object或者Array[Object]
$files = Get-ChildItem -File
$file = $files[0]
$file | Get-Member -MemberType Property  # 查看属性名
$file.GetType()    # 访问方法。此方法返回对象类别
$file.FullName     # 访问属性

# 定义对象
$uri = [System.Uri]::new('https://example.com')  # 用类的new方法定义
$my_obj = [PSCustomObject]@{                     # 用哈希表定义
    "name" = "Alex"
    "age" = 1
}
```

## 运算符

加减乘除之类的都正常。注意，除法是浮点除法

```powershell
1 -gt 0     # 大于。注意，>是重定向运算符
1 -band 3   # 位运算。类似有-bor, -bxor等
1 -shl 1    # 左移。右移是-shr
```

## 控制流

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

## 执行策略

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

## Profile

Profile脚本在每次启动Powershell时执行

```powershell
$PROFILE | Select-Object *   # 查看PROFILE文件
```

# 常用指令

```powershell
# 输出到文件
Get-Process | Out-File filename.txt
Get-Process | Export-Csv filename.csv
Get-Process | Export-Clixml filename.xml
```

## 文件

```powershell
# 创建硬链接
New-Item -ItemType HardLink -Name CoverageCount.cs -Value ..\..\OPIAspnet5\Models\CoverageCount.cs

# 查看文件的硬链接
fsutil hardlink list yourfile.txt
(Get-Item yourfile.txt).LinkType
(Get-Item yourfile.txt).Target
```

## 网络

### 综合

**ipconfig**

**netsh** - 网络配置与管理，包括网络接口、防火墙、路由等

### 应用层

```shell
# Web请求。别名：curl，wget
Invoke-Webrequest -Uri http://example.com
```

[Curl指南](https://www.ruanyifeng.com/blog/2019/09/curl-reference.html)，[Curl Cookbook](https://catonmat.net/cookbooks/curl)

```shell
# DNS查询
nslookup www.baidu.com
nslookup www.google.com "8.8.8.8"  # 使用指定DNS服务器
```

### 传输层

**netstat** - 网络状态

查询网络状态，如当前建立的连接、路由表

```shell
netstat -ano        # 显示所有连接以及对应进程PID
netstat -nop "tcp"  # 显示所有tcp连接，以及对应进程PID
netstat -r          # 显示路由表
netstat -no | findstr "8080"  # 查找指定端口的连接
```

常用选项如下：

| 选项 | 作用                                                    |
| ---- | ------------------------------------------------------- |
| a    | 显示所有连接                                            |
| b    | 显示各端口对应程序名。需要root权限                      |
| n    | 显示IP地址而非域名/主机名。不加n好像会做反向DNS，很耗时 |
| o    | 显示对应进程PID                                         |
| p    | 指定协议，如`netstat -p "tcp"`                          |
| r    | 显示路由表                                              |

### 网络层

```shell
# ARP缓存
arp -a   # 显示arp记录
arp -d   # 清空arp记录

# ping
ping www.baidu.com

# 路由表
route print

# 追踪路由转发
tracert www.baidu.com
```

# Windows 10

## 关闭网络搜索

使用注册表编辑器，在`HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Search`新建一个DWORD值，命名为`BingSearchEnabled`，并将数值设为0，重启

## 右键菜单栏

右键菜单，也叫做Context Menu，相关注册表项参考[这里](http://up.houheaven.com/Regedit/Reg_03.htm)

### 移除软件的右键菜单

可能的注册表位置（注：若不注明，一般放在该路径的`shell`，`background\shell`，`ShellEx\ContextMenuHandlers`等文件夹内）：

```bash
# 文件夹
\HKEY_CLASSES_ROOT\Folder
\HKEY_CLASSES_ROOT\Directory
# 文件
\HKEY_CLASSES_ROOT\*
\HKEY_CLASSES_ROOT\AllFilesystemObjects
# 桌面
\HKEY_CLASSES_ROOT\DesktopBackground

# 删的时候发现了，但是删完看不到效果的
\HKEY_CLASSES_ROOT\YunShellExt.YunShellExtContextMenu
```

### 添加自定义右键菜单

1. 创建项`<somewhere>\shell\<prompt>\command`
   - 特定文件类别的菜单：`<somewhere>`位于`HKEY_CLASSES_ROOT\SystemFileAssociations\.zip`
   - `<prompt>`为菜单中显示的文字
   
2. 将command的值设为指令，如`notepad.exe %1`
