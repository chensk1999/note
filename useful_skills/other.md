# Windows 10

## hotkeys

- win + R：运行。建立一个文件夹，把它加入系统环境变量PATH中，再把想要的东西的快捷方式放进去，就能够直接从win + R启动
- win + Tab：虚拟桌面

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

# 7-Zip

7-zip命令行界面：`7z.exe <command> <archive_name> [arguments]`

常用指令有`l` (List), `x` (eXtract with full path)；mcp参数可以指定[code page](https://en.wikipedia.org/wiki/Code_page#Microsoft_code_pages)，Shift-JIS代码页是932，GBK代码页为936

使用例：

```powershell
"C:\Program Files\7-Zip\7z.exe" x "shift-jis.zip" -mcp=932
```

# Github

## SSH Authentication (Windows)

若未特别说明，以下操作在git bash内完成

1. 检查有没有SSH密钥：`C:\Users\<user>\.ssh\`文件夹内有没有密钥文件（一般是`id_rsa`和`id_rsa.pub`）
2. 如果没有，在电脑上生成SSH密钥对
3. `eval "$(ssh-agent -s)"`（应该会输出Agent pid）
4. `ssh-add <私钥文件>`
5. 添加到账户：[settings](https://github.com/settings/profile) - SSH and GPG keys - New SSH key - title是给自己看的，key是公钥文件的内容（以文本格式打开然后复制粘贴）
6. 测试能否连接：`ssh -T git@github.com`，成功会输出 You've successfully authenticated。

如果安装了Cadence，由于Cadence设置了环境变量HOME，git无法正确找到密钥，需要将密钥复制到Cadence安装目录下的.ssh文件夹（删除或者更改HOME的值好像使cadence的软件出问题）。或者用git bash `ssh -vT git@github.com`看看git去哪里找密钥来找问题

## Timed out

出现`Failed to connect to github.com port 443 after 20000 ms: Timed out`错误大概率是因为代理设置

首先关闭系统代理；然后执行`git config --global --unset http.proxy`和`git config --global --unset https.proxy`

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

# 开源许可证

几种常用许可证（顺序从宽到严）

1. BSD、MIT：可以自由使用、复制、分发、修改，分发时必须包含版权提示。简洁，适合大部分中小规模的项目
2. Apacache：作者保留专利，比较容易转向商用
3. GPL：使用了GPL代码的项目都必须开源。适合传播开源福音

## GPL

[中文翻译](https://jxself.org/translations/gpl-3.zh.shtml)

1. 持有者可以运行、复制、分发、修改软件
2. 分发原始版本时不得修改GNU GPL声明；发布修改版时必须声明修改日期，并且除非版权所有者（所有贡献者）允许，必须使用GNU GPL许可证
3. 分发时，可以对分发服务、技术支持收费，但不能收版税、授权费、专利费等费用。而且分发时必须提供源码
4. 接收者自动获得来自初始授权人的授权，获得前述的权利
5. 软件输出结果不受GPL限制

有几个变种，限制从宽到严分别是

1. LGPL：闭源软件可以把LGPL代码作为库调用
2. GPL：如果项目包含GPL代码，整个项目都必须用GPL许可证
3. AGPL：使用AGPL代码的云服务也必须开源

# 药物

**药物分类**

- 非处方药（Over-the-Counter，OTC）：效果明确，副作用小的药物，可以自行购买服用
  - 甲类：红色OTC标志，仅在药店出售
  - 乙类：绿色OTC标志，可在一般商店出售，安全性更高
- 处方药：需要医生的处方才能购买

**家庭常用OTC药物成分**

| 名称         | 药效                         | 备注       |
| ------------ | ---------------------------- | ---------- |
| 布洛芬       | 消炎止痛、退热               |            |
| 对乙酰氨基酚 | 止痛、退热                   |            |
| 氯苯那敏     | 治疗过敏性疾病、晕车、流鼻涕 | 抗组胺药物 |

**常用OTC感冒药**

- 布洛芬
- 复方药：以乙酰氨基酚、咖啡因、氯苯那敏作为主要有效成分。对乙酰氨基酚和氯苯那敏能够缓解发热、头痛、流鼻涕、鼻塞等症状，同时咖啡因削弱嗜睡的副作用
  - 复方氨酚烷胺片
  - 氨酚咖那敏片

顺带一提，头孢、阿莫西林等抗生素也可用于治疗感冒，它们属于处方药

# 字幕

中文字幕每行不超过20字，英文字幕不超过40字符

## 时间轴

参考[Netflix指南](https://partnerhelp.netflixstudios.com/hc/en-us/articles/360051554394-Timed-Text-Style-Guide-Subtitle-Timing-Guidelines)。这个指南以0.5秒作为标准，两个吸引观众注意的事件（比如对话开始与字幕出现、前一句话字幕消失到后一句话字幕切入）要么同时发生，要么相隔0.5秒以上

根据个人经验，影响力从大到小排序是`画面 > 字幕 > 语音`。因此具体规则是：

- 字幕于音频开始的同时切入，于音频结束0.5秒（或者下一句话的开始）后消失
- 两段字幕之间的间隔应要么等于2帧，要么大于0.5秒
- 如果对话跨越镜头变化，字幕要么与镜头同时切换，要么错开至少0.5秒