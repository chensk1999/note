# 语法

## 脚本结构

1. 自动执行段：脚本运行时，自动从头开始执行，直到遇到return，exit，或者一个 hotkey / hotstring 标签
2. 子程序：以一个标签（可以是普通标签，hotkey标签或者hotstring标签）作为开头，return 作为结束。使用`gosub label`的方式调用。行为不同于函数，更相似于汇编语言的过程
3. 函数：类似于一般编程语言的函数

```
; 定义函数
function(param, ByRef ref_param, optional:="")
{
    ; 普通参数、引用传参、默认参数
    return "a value"
}
```

可以用`Func("func_name")`的方式引用函数对象

脚本运行时，首先运行自动执行段；然后，键盘/鼠标每捕捉到一个hotkey / hotstring，就执行相应子程序；在子程序内部，可以运算、调用其他的子程序或者其他的函数、执行命令

## 表达式

ahk的变量没有严格类型概念。一个表达式可以包含以下内容：

* 字符串

```
"this is a string"
"%和,不需要转义`r`n""双引号“”的转义字符是两个双引号"
```

* 变量

不需要先声明再定义，用赋值运算符赋值

```
var := 1
; 注意AHK的等号非常奇怪，既可以用于赋值也可以判断相等，为了避免歧义，请总是使用赋值运算符
; 另外，AHK的增量赋值(包括但不仅限于+=, ++)都有奇怪的特性。最好只用:=
```

变量可以通过连接表达式组合成文本

```
"the value is " var     ; 隐式连接
"the value is " . var   ; 显示连接
format("the value is {0}", var)  ; 格式化字符串
```

有若干内置变量（通常都以`A_`开头，如`A_TimeIdle`，这类变量只读。另外，可以用`global`和`static`声明全局变量和静态变量，用法同C

* 运算符

加减乘除，`?:`，etc.

## 对象

* 简单数组（Simple Array）：<span style="color:red;font-weight:bold">索引从1开始</span>

```
arr := [1, 2, 3]  ; 定义数组
value := arr[0]   ; 访问数组
arr[2] = 2        ; 赋值

arr.Length()
arr.InsertAt(Index, Value, Value2, ...)
arr.Push(Value, Value2, ...)
removed = arr.RemoveAt(Index)
removed = arr.Pop()
```

* 关联数组（Associative Array）：键值对

```
; 定义关联数组
asso_arr := {key:value, key2:value2, ...}
asso_arr := Object("key", value, "key2", value2)
; 访问关联数组：同简单数组

; 删除键值对
asso_arr.Delete(key)

; 枚举
for key, value in asso_array {
    ; do something
}
```

## 类

```
class ClassName extends BaseClassName
{
    InstanceVar := Expression		; 实例变量(实例属性)
    static ClassVar := Expression	; 静态变量(类属性)

    class NestedClass			; 嵌套类
    {
        ...
    }

    Method()				; 方法, 类定义中的函数称作方法
    {
        ...
    }

    Property[]  			; 属性定义, 方括号是可选的
    {
        get {
            return ...
        }
        set {
            return ... := value		; value 在此处为关键字, 不可用其他名称
        }
    }
}
```

## 命令

命令是一系列预定义的操作，可以执行特定的指令。一条命令语句由以下部分组成：

* 命令名称
* 文本：不是表达式，不需要括在双引号中，直接使用。前后的空白符被忽略
* 变量引用：`%Var%`表示变量 Var 的值。可以用诸如`I am %Var%`甚至`%Var%00`（Var后接两个0，表示Var x 100）的方式组合文本和变量引用
* 符号
  * `%`：括起变量，表示变量的值
  * `,`：分隔命令参数
  * 重音符：转义字符

```
MsgBox, The year is %A_Year%.`n
; 命令名与参数之间的逗号是可选的。但是参数之间的逗号不可省略
```

命令的参数分为四种：

1. InputVar，OutputVar：动态变量（变量的值是另一个变量的变量名），效果类似C++的引用传参
2. 文本参数：文本（字面值，变量引用或者两者的组合）。使用`% `开头可以强制一个参数接受表达式
3. 数字参数：可以是数字（字面值，变量引用或者两者的组合）或者表达式。注意有的参数既可以接受数字又可以接受文本，是文本参数

## 控制流

* 分支：if - else，switch，使用方法同C。不要忘记括号括起条件表达式，否则可能运行的就不是if而是某个历史遗留的分支命令

* 循环

```
loop count
while (expression)
for key , value in expression
```

可以用continue，break和until语句跳出/继续循环。循环可以用标签命名，能够直接跳出指定循环

内置变量`A_Index`标识循环次数（从1开始）

* 跳转：goto跳转，gosub跳转执行子程序

* 错误：try - catch

# Hotkey & Hotstring

```
; 定义hotkey
; 按键组合可以是多个按键（同时按下就生效）
; 也可以是按键1 & 按键2（此时按住&前按键不放，并按下&后的键生效）
按键组合::
    指令
    return

; 另一种定义方式
按键组合::指令

; 定义hotstring。输完内容后按空格、回车、tab、括号、分号等EndChars进行转换
按键序列::
    指令
    return
```

# 按键

```
{特殊符号}能打出它们原本的意思，如
{按键 down}, {按键 up}按下/放开某个按键
~按键	按键效果不会被屏蔽	
```

| 符号               | 说明                                                |
| ------------------ | --------------------------------------------------- |
| `#`                | win                                                 |
| `!`                | alt                                                 |
| `^`                | ctrl                                                |
| `+`                | shift                                               |
| `<, >`             | 左边 / 右边的按键，如`<^`指左ctrl                   |
| `*`                | 通配符                                              |
| `$`                | `$`作前缀时强制使用keybord hook，阻止被send指令触发 |
| `LButton, RButton` | 鼠标                                                |

例

```
F1:: send F1 pressed.
~Esc:: send Esc pressed, and it will still function
~$Space:: send Space pressed, it is neither triggered by send nor blocked
```



# 指令

## Send

```
send, 按键序列
send,
(
按键序列
)
```

## 鼠标

* Click

```
click [up/down], [key], [x, y], [count], [Relative]

click 2                      ; 在当前位置点击两次
click up, right, 100, 200    ; 移动到(100, 200)然后松开右键
clkck %x%, %y%, 0, Relative  ; 移动到相对当前位置(x, y)处然后不点击
```

* 使用send指令发送Click

```
send ^{click 100, 200}       ; 移动到(100, 200)进行Ctrl + LeftClick
```

* 坐标模式

```
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

## 其他

sleep, 时间（单位：ms）
Run, 文件路径/网址
Msgbox, 字符串
SoundBeep

```
#ifWinActive/ifWinExist 窗口名称
语句序列
#ifWinActive/ifWinExist
只再特定窗口作用的指令
注：后一个不带窗口名称的#ifWinActive/ifWinExist是标志了contest sensitivity的结束
```

# 示例

```
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



```
; 我的世界滑稽纪元2自动砍滑稽脚本


```

<span style="background-color:#c7d1f0">abc</span>