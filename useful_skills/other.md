# Windows

## hotkeys

win + R：运行。建立一个文件夹，把它加入系统环境变量PATH中，再把想要的东西的快捷方式放进去，就能够直接从win + R启动

win + Tab: 虚拟桌面

## windows 10关闭网络搜索

使用注册表编辑器，在`HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Search`新建一个DWORD值，命名为`BingSearchEnabled`，并将数值设为0，重启

# mingw编译&make

## 简单源文件的编译&链接

```
g++ -c main.cpp
g++ -c func.cpp
g++ main.o func.o -o release.exe
```

## 源文件与库的链接

```
gcc main.cpp -I "header directory" -L "lib directory" -lname
```

其中使用的库文件命名为libname.a（好像也不一定？有奇怪的模糊匹配规则），name可以替换成任何合法名字

## make

```
mingw32-make -f Makefile
```

最简单的编译命令由三个部分组成：

1. 目标：相当于标识符，通常用目标文件名
2. 依赖项：用于判断目标构建次序、判断目标是否需要重新构建（如果依赖项的时间戳比目标文件的更新，就需要重新构建）。如果.PHONY作为目标，不会进行检查，总会重新构建
3. 指令：构建目标的指令

```makefile
target: prerequisites    # 注意依赖项最好包括头文件
	commands             # 必须一个tab缩进

# 实例：
test.exe: main.cpp func.cpp func.h
	g++ -g -o test.exe main.cpp func.cpp
```

* 模式匹配

```makefile
%.o: %.c
	gcc -c $< -o $@
```

其中的`%.c`匹配了当前目录下的所有.c文件，`%.o`表示目标是同名.o文件

* 变量

虽然叫做变量，但是实际上更类似于宏，因为只是文本替换

```makefile
HELLO = hello, world!
test:
	@echo $(HELLO)
	# 默认会打印每一条指令，开头加@的不打印
```

命令行参数好像也会变成宏（例：`make -f Makefile DEBUG=Y`）

有一系列特殊的变量，如

* Implicit Variables：`$(CC)`为当前编译器
* Automatic Variables
  * `$@`：当前目标
  * `$<, $^`：第一个依赖项，所有依赖项
  * `$*`：匹配符 % 匹配的部分
  * `$(@D), $(@F)`：当前目标的目录名、文件名
  * `$(<D), $(<F)`：第一个依赖项的目录名、文件名

* 判断与循环

```makefile
ifeq ($(CC), gcc)
	commands
else
	commands
endif
```

# 解压日语压缩包

用7zip命令行解压，可以用mcp参数指定[code page](https://en.wikipedia.org/wiki/Code_page#Microsoft_code_pages)，shift-jis的code page是932

语法：`7z.exe <command> <archive_name> [arguments]`

常用指令：l (List), x (eXtract with full path)

使用例：

```powershell
"C:\Program Files\7-Zip\7z.exe" x "shift-jis.zip" -mcp=932
```

# Github SSH Authentication (Windows)

若未特别说明，以下操作在git bash内完成

1. 检查有没有SSH密钥：`C:\Users\<user>\.ssh\`文件夹内有没有密钥文件（一般是`id_rsa`和`id_rsa.pub`）
2. 如果没有，在电脑上生成SSH密钥对
3. `eval "$(ssh-agent -s)"`（应该会输出Agent pid）
4. `ssh-add <私钥文件>`
5. 添加到账户：[settings](https://github.com/settings/profile) - SSH and GPG keys - New SSH key - title是给自己看的，key是公钥文件的内容（以文本格式打开然后复制粘贴）
6. 测试能否连接：`ssh -T git@github.com`，成功会输出 You've successfully authenticated。


如果安装了Cadence，由于Cadence设置了环境变量HOME，git无法正确找到密钥，需要将密钥复制到Cadence安装目录下的.ssh文件夹（删除或者更改HOME的值好像使cadence的软件出问题）。或者用git bash `ssh -vT git@github.com`看看git去哪里找密钥来找问题

# 知网下载pdf文档

1. 复制下载链接
3. 将url中的`dflag=cajdown`参数改为`dflag=pdfdown`。如果没有dflag参数，就自己加上
3. 如果还是不能下载，尝试删掉其他不必要的参数

例：
原下载链接（caj文件）：  https://kns.cnki.net/KNS8/download?filename=XXX&tablename=YYY&dflag=cajdown
下载pdf的链接：https://kns.cnki.net/KNS8/download?filename=XXX&dflag=pdfdown

或者，更简单地，使用[油猴脚本](https://greasyfork.org/zh-CN/scripts/390733-%E7%9F%A5%E7%BD%91pdf%E4%B8%8B%E8%BD%BD%E5%8A%A9%E6%89%8B)

2021年9月25日可用

# 二进制文件和文本文件转换

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

以上在是Unix指令。windows可以用WSL，或者git bash也可以