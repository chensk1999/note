# 语法

## 脚本结构

脚本包括以下几个部分：

1. 自动执行段：脚本运行时，自动从头开始执行，直到遇到return，exit，或者一个 hotkey / hotstring 标签
2. 子程序：以一个标签（可以是普通标签，hotkey标签或者hotstring标签）作为开头，return 作为结束。使用`gosub label`的方式调用。行为不同于函数，更相似于汇编语言的过程
3. 函数：类似于一般编程语言的函数

脚本运行时，首先运行自动执行段；然后，键盘/鼠标每捕捉到一个hotkey / hotstring，就执行相应子程序；在子程序内部，可以调用其他的子程序或者其他的函数、执行命令

```assembly
GLOB_VAR := 0

lbl:
    MsgBox, 这是自动执行段
    return

function(param, ByRef ref_param, optional:="") ; 普通参数、引用传参、默认参数
{
    gosub lbl
    return "result"
}
```

AHK里面其实有两套语法，分别是和旧版本兼容的Legacy Syntax，以及新版的语法。本笔记中，除了必须使用Legacy Syntax的部分（主要是“命令”一节介绍的语法），均使用新版的语法

## 表达式

ahk的变量没有严格类型概念。一个表达式可以包含以下内容：

```assembly
; 字符串
; 空白符的转义字符是`n`r等，双引号的转义字符是两个双引号
"this is a string"

; 变量
; 不需要先声明再定义，用赋值运算符 := 赋值
; 注意：=, +=, ++等运算符都是Legacy Syntax，最好只用:=
var := 1

; 变量可以通过连接表达式组合成字符串
"the value is " var     ; 隐式连接
"the value is " . var   ; 显示连接
format("the value is {0}", var)  ; 格式化字符串
```

有若干内置变量（通常都以`A_`开头，如`A_TimeIdle`，这类变量只读）。另外，可以用`global`和`static`声明全局变量和静态变量，用法同C

## 命令

命令是一系列预定义的操作。命令语句由命令名称和参数组成，如

```assembly
MsgBox, 4, , Hello`, World
; 命令与第一个参数之间的逗号可以省略，参数之间的逗号不可省略
```

参数分为以下几种：

```assembly
; InputVar, OutputVar
; 传入变量名或者dynamic variable reference，效果类似C++的引用传参
MouseGetPos, x, y

; 文本参数
; 传入文本。不需要双引号，变量需要用如%var%的形式引用
; 文本中包含逗号、百分号需要用`转义（部分命令有smart comma handling，不转义仍能执行，但为了可读性建议都转义）
MsgBox, Mouse at %x% `, %y%
; 百分号可以强制文本参数接受表达式
MsgBox % "New mouse position at " . x + 100

; 数字参数
; 数字文本或者表达式。文档中描述为"This parameter can be an expression"的是数字参数
MouseMove, x + 100, %y%   ; 两个参数分别是表达式和数字文本
```

## 对象

**简单数组**（Simple Array）：**索引从1开始**

```assembly
arr := [1, 2, 3]  ; 定义数组
value := arr[1]   ; 访问数组
arr[2] := 3       ; 赋值

arr.Length()
arr.InsertAt(Index, Value, Value2, ...)
arr.Push(Value, Value2, ...)
removed := arr.RemoveAt(Index)
removed := arr.Pop()

; 枚举
loop % arr.Length() {
    MsgBox % arr[A_Index]
}

for index, value in array{
    MsgBox % "Item " index " is " value
}
```

**关联数组**（Associative Array）：键值对

```assembly
; 定义关联数组
asso_arr := {key:value, key2:value2, ...}
asso_arr := Object("key", value, "key2", value2)
; 访问关联数组：同简单数组

; 删除键值对
asso_arr.Delete(key)

; 枚举
for key, value in asso_array {
    MsgBox %key% = %value%
}
```

## 控制流

```assembly
; if分支
; 注意，必须用括号括起条件，否则会使用Legacy Syntax。其他控制流同理
if (x < 100) {
    x := x + 100
} else if (x > 2000) {
    x := 2000
} else {
    x := x
}

; loop循环
loop %count%
; while循环
while (expression)
; for循环
for key , value in expression
```

可以用continue，break和until语句跳出/继续循环。循环可以用标签命名，能够直接跳出指定循环

内置变量`A_Index`标识循环次数（从1开始）

* 跳转：goto跳转，gosub跳转执行子程序

* 错误：try - catch

# Hotkeys & Hotstrings

## Hotkey

```assembly
; 基本hotkey。当该按键被按下时跳转执行此过程
q::
    send, You pressed a key.
    return

; 特殊按键的hotkey。另外，如果过程体只有一行，可以和标签放在同一行，并省略return
Esc:: pause

; 修饰键+普通按键的hotkey。在按下Ctrl + a时触发。修饰键列表见后文Hotkey Modifier
^a::
    send, You pressed Ctrl and A.
    return

; 多个按键触发的hotkey
a & b::
    send, You pressed A and B.
    return

; 特殊效果的修饰键。$前缀的按键不会被Send指令触发。详细修饰键列表见后文Hotkey Modifier
; 假如去掉$，前面Ctrl + a以及a + b热键的send指令中的A会触发这一个热键
$A::
    Send, You pressed A. Send command won't trigger this.
```

## Hotstring

```assembly
; 定义hotstring。输完内容后按空格、回车、tab、括号、分号等EndChars触发
; 触发后将会退格清除hotstring，然后运行后面的代码
; EndChars可以用Hotstring("EndChars", "-()[]{}:;")动态更改
::btw::
    MsgBox You typed "btw".
    return

; 不需要EndChars直接转换
:*:hello:: Send, hello world

; hotstring中包含空白符。`n`t分别表示enter、tab
:*:hello`n:: Send, hello world

; 即使hotstring前面是字符也能触发
:?:fine::
    Send, I'm fine  ; 假如输入define也会触发fine
    return

; 不自动退格
:B0:1+1=:: Send, 2
```

## Hotkey Modifier（修饰键）

用修饰键作为Hotkey前缀，可实现特殊功能

```assembly
<!a:: send, You pressed Left Alt + A.
~b:: send, Do something without blocking keystroke
```

| 符号 | 按键  | 备注                                                         |
| ---- | ----- | ------------------------------------------------------------ |
| #    | Win   | 如果发送的按键中包含L，等到Win键松开才会发送，以防止锁定电脑 |
| !    | Alt   |                                                              |
| ^    | Ctrl  |                                                              |
| +    | Shift |                                                              |
| &    |       | 两个按钮                                                     |
| <, > |       | 成对按键左边/右边的一个，如`<+`表示左shift                   |
| *    |       | 任意Modifier，如`*a`可以被Ctrl + a，Shift + a等组合触发      |
| ~    |       | 不会阻挡原本的键盘事件                                       |
| $    |       | 强制使用keybord hook，不会被send指令触发                     |

## Key Names（特殊按键）

在Send函数使用大括号括起来表示输出特殊符号（如`{Esc}, {Space}, {BackSpace}`、转义字符（如`{{}, {+}, {<}`）、Hotkey Modifier（如`{Ctrl}, {Alt}`）都如此

```assembly
Send Esc        ; 输出"Esc"
Send {Esc}      ; 输出键盘上的Esc键
Send {Esc down} ; 按下Esc键
Send {Esc up}   ; 松开Esc键

; 用作Hotkey标签时不需要大括号
Esc:: Send You pressed Esc.

; Modifier单独输出
Send +a         ; 输出Shift + a（变成大写A）
Send {Shift}a   ; 输出shift，然后输出a
```

| 按键   | 字符                                          |
| ------ | --------------------------------------------- |
| 方向键 | Up, Down, Left, Right                         |
| 鼠标   | LButton, RButton, MButton, WheelDown, WheelUp |

特别地，`%A_ThisHotkey%`表示被按下的按键

# 鼠标

* Click

```assembly
click [up/down], [key], [x, y], [count], [Relative]

click 2                      ; 在当前位置点击两次
click up, right, 100, 200    ; 移动到(100, 200)然后松开右键
click %x%, %y%, 0, Relative  ; 移动到相对当前位置(x, y)处然后不点击
```

* 使用send指令发送Click

```assembly
send ^{click 100, 200}       ; 移动到(100, 200)进行Ctrl + LeftClick
```

* 坐标模式

```assembly
CoordMode, TargetType [, RelativeTo]
```

TargetType：要作用的目标类型

1. ToolTip：作用于 ToolTip
2. Pixel：作用于 PixelGetColor，PixelSearch 和 ImageSearch
3. Mouse：作用于 MouseGetPos，Click 以及 MouseMove/Click/Drag
4. Caret：作用于内置变量 A_CaretX 和 A_CaretY
5. Menu：作用于为 Menu Show 命令指定坐标的时候.

RelativeTo：TargetType 要关联的区域。如果省略, 则默认为 Screen

1. Screen：坐标相对于桌面(整个屏幕)
2. Relative：坐标相对于活动窗口
3. Window [v1.1.05+]：与 Relative 效果相同，含义更清晰
4. Client [v1.1.05+]：坐标相对于活动窗口的工作区，其中不包括标题栏，菜单栏(如果它含有标准菜单栏) 和边框。Client 坐标模式较少依赖于操作系统版本和主题

# 窗口操作

```
#ifWinActive/ifWinExist 窗口名称
语句序列
#ifWinActive/ifWinExist
只再特定窗口作用的指令
注：后一个不带窗口名称的#ifWinActive/ifWinExist是标志了contest sensitivity的结束
```



# 其他指令

sleep, 毫秒
Run, 文件路径/网址
Msgbox, 字符串
SoundBeep

# 示例

```assembly
; 植物大战僵尸的控制脚本（部分）

; 全局设置 & 全局变量
CoordMode Mouse, Client
mode := "pool"

; 点击cnt次泳池的(i, j)格子
PoolField(i, j, cnt=1) {
    x := j * 80 + 80
    y := i * 85 + 140
    Click %x%, %y%, %cnt%
    Sleep 50
    Return 0
}

; 切换模式
$Esc::
    if ("off" = mode) {
        Send {Esc}
    } else {
        mode := "off"
        MsgBox Current Mode: %mode%
    }
    Return

; 种植植物
~1::
~2::
~3::
~4::
~5::
~6::
~7::
~8::
~9::
~0::
    num := SubStr(A_ThisHotkey, 2)
    index := (0 = num) ? 9 : num - 1
    MouseGetPos x, y
    if ("pool" = mode || "garden" = mode) {
        Plants(index)
        Sleep 50
        Click %x%, %y%, 1
    } else if ("zen" = mode) {
        Zen_tool(index)
        Sleep 100
        Click %x%, %y%, 0
        Sleep 100
        Click 1
    }
    Return
```

```assembly
; 滑稽纪元2魔改版自动砍滑稽
; 滑稽碎片放物品栏第8格，斧子放第九格，指针指着滑稽碎片黑色部分
; 使用方法：u开始，i暂停

u::
    send 9
    loop {
        ; 检测有没有滑稽碎片
        mouseGetPos x, y
        pixelGetColor cur_color, x, y

        if (cur_color < 0xEEEEEE) {
            ; 放滑稽碎片
            send 8
            sleep 100
            click right
            sleep 100
            send 9
        }

        ; 砍
        sleep 1200
        click
    }
    return

i::
    pause
    return
```

```assembly
; 按s反复移动鼠标，Esc停止
~s::
    flag := 1
    while (flag == 1) {
        MouseMove, 0, -80, 70, R
        Sleep, 100
        MouseMove, 0, 80, 70, R
        Sleep, 100
    }
    return

Esc:: flag := 0
```

