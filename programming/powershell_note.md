# 基础知识

## 指令调用

PowerShell不区分大小写，指令命名一般格式是verb-noun，同时很多指令都有别名，有的是为了向前兼容，有的是为了缩短指令名字

一个调用指令的简单例子：

```powershell

```

使用参数时可以简化，只输入参数可以唯一识别的一部分的一部分，如，-common参数可以只输入-com（假设没有其他形参含有com），到这一步之后也可以用tab自动补全

## 流水线(pipeline)

```命令1 | 命令2```会将命令1的结果作为命令2的参数

```命令2 (命令1)```也有同样效果

# 常用指令

## 文件

```powershell
# 显示文件、文件夹
Get-ChildItem
dir

# 打开文件夹
Set-Location
cd  # 别名，change directory
cd -LiteralPath "path with * or ? in it"

# 创建文件
New-Item filename

# 创建文件夹
New-Item folder -type Directory
mkdir folder    # 用函数实现，mkdir调用new-item创建文件夹

# 删除项目
Remove-Item

# 输出到文档
Out-File

# 输出到文件（以Get-Process为例）
Get-Process | Export-Csv filename.csv
Get-Process | Export-Clixml filename.xml

cls         # 清屏
ren         # 重命名（可以结合通配符批量进行）
move        # 移动文件
tree [/f]   # 文件夹树[文件树]
```

## 网络

```powershell
ping /?
nslookup     # 查询域名的地址（DNS记录）
ipconfig
```



# 杂项

## 通配符

?匹配一个字符，*匹配任意个（包括0个）字符

## 快捷键

| hotkey           | effect                              |
| ---------------- | ----------------------------------- |
| win + r          | 运行程序                            |
| up/down arrow    | 上一个/下一个指令                   |
| tab, shift + tab | 自动补全指令/参数（可以用通配符?*） |
| esc              | 清除当前行                          |
| ctrl + c         | 取消命令并返回到shell               |

## 不常用指令

```powershell
# 查看版本
$PSVersionTable

# 查看帮助
help <command>

# 查看指令列表
Show-Command
```

