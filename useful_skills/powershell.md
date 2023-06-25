Shell指用户界面，与内核（Kernel）相对。此笔记中，Shell专指操作系统的命令行界面（Command-Line Interface，CLI）

# 常用指令

## 文件与路径操作

| Unix Shell   | cmd.exe    | Powershell    | 说明           |
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

注：Powershell大多数命令都设置了别名，把Unix Shell或者cmd.exe的对应命令名称输进去一般也能运行

## 其他

| Unix Shell | cmd.exe | Powershell   | 说明         |
| ---------- | ------- | ------------ | ------------ |
| man        | help    | Get-Help     | 打印文档     |
| clear      | cls     | Clear-Host   | 清屏         |
| echo       | echo    | Write-Output | 打印到标准流 |

# Bash

Bash是最常见的Unix Shell，它能运行于Linux系统和MacOS；Windows10安装了Linux子系统之后也可以使用Bash

虽然Bash很常见，但Linux系统下运行的命令行界面不一定是Bash。`echo $SHELL`可以看见当前用的Shell，`cat /etc/shells`可以看已安装的Shell。常见的Shell有

| 分类             | Shell                    |
| ---------------- | ------------------------ |
| Bourne Shell家族 | sh, bash, dash, ksh, zsh |
| C Shell家族      | tcsh, csh                |

幸运的是，这些Unix Shell的指令基本一致，语法也只是分为两派，两个家族内部的语法高度相似

# cmd.exe

cmd.exe也叫命令提示符（Command Prompt），是Windows家族许多操作系统(Windows 2000，XP，Vista等）的默认Shell

# PowerShell

Powershell主要用于Windows 7及其后续版本，也可以运行于Linux和MacOS

## 基础知识

PowerShell不区分大小写，指令命名一般格式是verb-noun，同时很多指令都有别名，有的是为了向前兼容，有的是为了缩短指令名字

使用参数时可以简化，能唯一识别即可，如，-common参数可以只输入-com（假设没有其他形参含有com），到这一步之后也可以用tab自动补全

**流水线(pipeline)**

```命令1 | 命令2```会将命令1的结果作为命令2的参数

```命令2 (命令1)```也有同样效果

## 常用指令

```powershell
# 输出到文件（以Get-Process为例）
Get-Process | Out-File filename.txt
Get-Process | Export-Csv filename.csv
Get-Process | Export-Clixml filename.xml

ping /?
nslookup     # 查询域名的地址（DNS记录）
ipconfig
```

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
1 -gt 0     # 大于
1 -band 3   # 位运算
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
