# Windows hotkeys

win + R：运行。建立一个文件夹，把它加入系统环境变量PATH中，再把想要的东西的快捷方式放进去，就能够直接从win + R启动

win + Tab: 虚拟桌面

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

# Word

## 页眉与页脚

插入 - 页眉和页脚

不同部分的页眉页脚不同，比如说从第三页开始标页码：首先在分节处插入布局 - 分隔符 - 分节符，然后选中页眉页脚，设计 - 导航 - 取消链接到前一节

调整页眉的横线：选中页眉 - 开始 - 段落 - 边框 - 无边框

## 公式行宽

如果想要公式不比平常的行宽，选中公式，右键，段落-取消“如果定义了文档网格，则对齐到文档网格”

# 解压日语压缩包

用7zip命令行解压，可以用mcp参数指定[code page](https://en.wikipedia.org/wiki/Code_page#Microsoft_code_pages)，shift-jis的code page是932

语法：`7z.exe <command> <archive_name> [arguments]`

常用指令：l (List), x (eXtract with full path)

使用例：

```
"C:\Program Files\7-Zip\7z.exe" x "shift-jis.zip" -mcp=932
```
