# Shell

Shell指用户界面，与内核（Kernel）相对。此笔记中，Shell专指操作系统的命令行界面（Command-Line Interface，CLI）

## cmd

cmd也叫命令提示符（Command Prompt），是Windows家族许多操作系统(Windows 2000，XP，Vista等）的默认Shell

```cmd
REM 定义、访问变量
set a=1
echo %a%
```

## PowerShell

Powershell主要用于Windows 7及其后续版本，也可以运行于Linux和MacOS

### 基础知识

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

### 变量

```powershell
# 数值、字符串、布尔值
$i = 1
$s = "Hello, `$i = $i"  # 双引号中的$i会格式化，单引号不会；用反斜杠`转义
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

变量作用域

```powershell
$Global:ip_addr = "192.168.0.1"   # 全局变量，在当前Powershell会话全局可用
$Script:port = "80"               # 脚本变量，当前脚本可用
$Local:username = "admin"         # 本地变量，当前代码块中可用
```



### 运算符

加减乘除之类的都正常。注意，除法是浮点除法

```powershell
1 -gt 0     # 大于。注意，>是重定向运算符
1 -band 3   # 位运算。类似有-bor, -bxor等
1 -shl 1    # 左移。右移是-shr
```

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

### Profile

Profile脚本在每次启动Powershell时执行

```powershell
$PROFILE | Select-Object *   # 查看PROFILE文件
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

```powershell
# 输出到文件
Get-Process | Out-File filename.txt
Get-Process | Export-Csv filename.csv
Get-Process | Export-Clixml filename.xml
```

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

1. 创建项`<somewhere>\shell\<prompt>\command`，其中`<somewhere>`具体路径见后文，`<prompt>`为菜单中显示的文字
2. 将command的值设为指令，如`notepad.exe %1`

`<somewhere>`具体是哪里：

1. 特定文件类别的菜单：`HKEY_CLASSES_ROOT\SystemFileAssociations\<.ext>`，其中`<.ext>`为文件扩展名，比如`.zip`
