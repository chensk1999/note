# LISP简介

Cadence SKILL 是 Lisp 方言，其编程与我学过的其他语言都截然不同，因此首先需要学习 Lisp 的基本思想。我主要参考了 ANSI Common Lisp，但只会着重记录 Lisp 区别于命令式编程语言的特点，不会集中于Common Lisp 独有的功能

LISP有以下几种数据类型

- 列表：`(element1 element2 element3 ...)`，底层实现是链表，每个节点包括两个指针：一个指向节点元素，另一个指向下一节点。尾节点的 Next 指针为 Nil
- 原子
  - 符号（Symbol）：可以指向任何对象的指针。是全局变量
  - 字面值，包括数字和字符串

特别地，nil 表示表示逻辑非或者空列表。一般用 t 表示逻辑真（也可以用任何非 nil 对象表示逻辑真）

Lisp 有点像 Python ，所有变量都是对象，同时只有隐式的指针，而且两者的 GC 也非常相似。甚至它的元编程范式在 Python 中都有一定程度的对应（lambda函数、map、reduce等）

## 表达式

表达式从左到右求值。字面值的值是自身，符号的值是它指向的对象，列表的值是将第一个元素作为函数、剩余元素作为实参求得的值

```lisp
5       ; 5
(+ 2 3) ; 5
(/ (* 7 9) (- 5 2))     ; = (7*9) / (5-2) = 21
```

## 操作符

### Quote

```lisp
; quote
; 单位元，(quote arg) -> arg。可缩写为'arg
; 特别地，quote作用的对象不会被求值
nil         ; 求值得到自身
'nil        ; quote单位元性质，得到nil自身
(+ 3 5)     ; 求值得8
'(+ 3 5)    ; 单位元性质，得到原列表。原列表不会再被求值
(defparameter SYMBOL 10)
SYMBOL      ; 10。符号求值得到它指向的对象
'SYMBOL     ; SYMBOL。符号不被求值，得到符号自身（即指向10的指针）
```

简单的说，无 quote 的对象可以是表达式、函数，有 quote 的对象可以当作是数据、变量

### 列表操作

```lisp
; cons
; CONStruct，构建列表。(cons arg1 arg2)
; 如果arg2是原子，表达式值为(arg1, arg2)。如果arg2是列表，将arg1插入到列表开头
(cons 1 2)          ; (1 2)
(cons '(1 2) nil)   ; ((1 2))

; car
; 据传是Contents of the Address part of Register number的缩写
; 有说法认为来自于最早的Lisp实现此功能时使用的的CPU指令
; 取列表的首元素
(car '(1 2 3))      ; 1

; cdr
; 据传是Contents of the Decrement part of Register number的缩写
; 取列表首元素之后的元素，即链表首节点的Next指针
(cdr '(1 2 3))      ; (2 3)
```

### 变量

```lisp
; let，定义局部变量
; (let ((var1 value1) (arg2 value2)) (expression))
(let ((x 1) (y 2)) (+ x y))

; defparameter，定义全局变量
(defparameter GLOB 1)

; setf，变量赋值。可以用setf隐式定义全局变量
(setf GLOB 100 ANOTHER_GLOB t)
```

### 控制流

```lisp
; if
; (if cond value_when_t value_when_nil)
(if (> 5 3) "5>3" (- 5 3))
```

### 函数

```lisp
; lambda：最早的函数定义式
; (lambda (args) (expression))
(lambda (x) (+ x 1))

; defun：定义有名字的函数，可以视作defparameter + lambda
; (defun name (args) (expression))

; sharp quote：函数指针
#'+
```

# SKILL语法

## 符号

```lisp
; 符号 ≈ 指针
; 一般来说，直接使用符号会对符号求值（即取得它指向的对象）
; 用quote操作符作用的符号不会被求值（即依然是指针）
a = 10
b = a       ; b = 10, type(b) = fixnum, type('b) = symbol
c = 'a      ; c = 'a, type(c) = symbol

; 操作指向符号的符号
set(c 5)        ; a = 5
b = symeval(c)  ; b = a

; 作为宏/某些特殊函数的参数时，符号会表示它自己，而不会被求值为它指向的对象
; 此时称作implicitly quoted
setq(c 5)       ; c = 5, 等效于赋值运算
```

```lisp
; 用函数操作符号
gensym("net")       ; 产生符号，会自动加后缀以区分
gensym('net)
get_pname('net)     ; 获取符号的打印名
```

## 运算符

SKILL的所有运算符都有两种写法，Operator形式用中缀表达式进行运算，Function形式用函数调用方式进行运算。一般会使用 Operator 形式，但由于错误信息会用 Function 形式，有必要把两种都记住

| Operator               | Function                                   | Note                                                         |
| ---------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| `<, <=, >, >=, ==, !=` | lessp, leqp, greaterp, geqp, equal, nequal | Returns t or nil                                             |
| `&&, ||`               | and, or                                    | 表达式值为最后一个计算的值。在结果为真时，对于and是最后一个值；对于or，是第一个非nil值 |

## 列表

```lisp
; 定义列表
l1 = '(1 2 3)       ; quote函数获得列表字面值
l2 = list(4 5 6)    ; list函数产生列表
l3 = cons(0 l1)     ; cons函数构建列表元素，并插入到l1开头
l4 = append(l1 l2)  ; append函数连接两个列表

; 引用列表元素
car(l1)     ; 引用列表首元素
cdr(l1)     ; 引用首元素之外的元素（即，链表首节点的Next指针）
nth(2 l1)   ; 引用第n个元素

; 其他列表函数
length(l1)      ; 列表长度
member(2 l1)    ; 是否包含元素（返回nil / 以2为首元素的列表）
```

特别地，可以用二元列表表示坐标，用包含两个二元列表的列表表示方框。SKILL提供了一些特殊方式来操作这种列表

```lisp
; 用冒号定义坐标
coord = 300:400     ;(300 400)

; 提取坐标
x = xCoord(coord)
y = yCoord(coord)

; 用左下角、右上角坐标表示bounding box
bBox = '(300:400 500:450)

; 用car和cdr的复合函数引用四个角的坐标
ll = car(bBox)      ; 左下角（lower left）坐标
ur = cadr(bBox)     ; 右上角（upper right）坐标，cadr = car(cadr(...))
llx = caar(bBox)
lly = cadar(bBox)
urx = caadr(bBox)
ury = cadadr(bBox)
```

## 控制流

```lisp
; if-then-else （注意：if和括号中间不能有空格）
; 控制流其实都是函数，而函数调用当然不允许函数名和括号中间有空格
if( shape == "rect"
  then
    println("Shape is rectangle")
    rectCnt++
  else
    println("Shape is not rectangle")
  )
; 从Lisp的角度看if函数：如果第一个参数为真，计算第二个参数的值并返回；否则，计算第三个参数的值并返回
; 从命令式角度看：if表达式的值是被求值的最后一个表达式的值

; when分支
when( shape == "ellipse"
  println("Shape is ellipse")
  ellipseCnt++
  )
; 如果第一个参数为真，计算第二个参数的值并返回；否则返回nil

; unless分支
unless( shape == "rect" || shape == "ellipse"
  println("Illegal shape")
  )
; 如果第一个参数为真，返回nil；否则计算第二个参数的值并返回

; case分支
case( shape
  ("rect"
    println("Shape is rectangle")
    rectCnt++
    )
  (("label" "line")     ; catches any element in this list
     println("Shape is label or line")
     ellipseCnt++
     )
  (t                    ; catches everything
     println("Illegal shape")
     )
  )
; 如果第一个参数匹配到了某个分支，计算该分支并返回；若未匹配则计算最后一个分支

; for 循环。注意循环变量只能是int
sum = 0
for( i 1 5      ; i从1到5
  sum = sum + i
  )
; 循环变量不影响外部同名变量。for函数总是返回t

; foreach循环
shapes = ("rect" "ellipse" "rect" "line")
foreach( shape shapes
  case(shape
    ("rect"     rectCnt++)
    ("ellipse"  ellipseCnt++)
    ("label"    labelCnt++)
    ("line"     lineCnt++)
    (t          misCnt++)
    )
  )
; 类似for循环，foreach不影响外部同名变量。foreach总是返回被迭代的列表
```

## 函数

- 定义

```lisp
; Lisp style (not recommended)
(defun name (args)
  expression)

; Algebraic style
procedure( name( arg1 arg2
                 @optional (opt1 0) (opt2 0)
                 @rest args)
  expression
)

; 关键字参数。@key和@optional不能同时使用，除此之外参数可以任意组合或者省略
procedure( name2( arg1 arg2
                  @key (key1 0) key2
                  @rest args)
  expression
)

; lambda匿名函数
add = lambda((x y) x+y)
```

还有一种 nlambda 函数，它会将参数不求值直接传入。指导手册不建议使用，但没有说为什么。如果需要未求值的实参，可以用宏

- 调用

```lisp
; Algebraic style (recommended)
func( arg1 arg2 )

; Lisp style
(func arg1 arg2)

; Command style (only in toplevel)
func arg1 arg2

; key arguments
func(?key1 1 ?key2 2)
```

# 数据结构

## Property List

```lisp
; 可以用property list实现类似于其他语言的类的效果
setplist('point '(x 3 y 5))     ; x and y are implicitly quoted
point       ; undefined variable，之后对point赋值不影响property list
point.x     ; = 3

ppoint = 'point
ppoint->x   ; 3
```

property list是全局的，有的时候同名变量（即使一个是局部变量，另一个是全局变量）会共用property list

## String

```lisp
; 连接字符串
strcat("a" "b" "c")             ; "abc"
buildString('("a" "b" "c") ".") ; "a.b.c"

evalstring("1+2")   ; evaluate & return expression
loadstring("procedure(f(n) if(n==0 1 f(n-1)*n))")
                    ; parse & execute expression, return t if success
```



## Defstruct

## Array

```lisp
; 声明数组
declare(arr[3])   ; declare array with 3 elements
arr[0] = 1
arr[1] = 3.14
arr[2] = "whatever"
arr[3]      ; index out of bound
```

# 杂项

右方括号`]`可以作为 super right bracket 匹配任意个左括号，引号+右方括号`"]`能匹配未配对双引号

Comma `,` 和Comma-At `,@` 可以表示求值

```lisp
a = (2 3 4)
'(1 a)      ; (1 a)
'(1 ,a)     ; (1 (2 3 4))
'(1 ,@a)    ; (1 2 3 4)

; boundp 判断变量是否被赋过值。
boundp('var) && var     ; 如果var有值，求其值；否则得到nil
```

# 常用函数

## 文件操作

```lisp
; 判断文件存在
isFile("filename")  ; t or nil
isDir("dirname")

; 判断文件读写权限
isReadable("file_or_dir")   ; permission to read file / list directory
isWritable("file_or_dir")   ; permission to wirte file / update directory
isExecutable("file_or_dir") ; permission to execute file / search directory
; All of them returns nil if specified file/dir does not exist

getDirFiles("dir")          ; list files in directory
simplifyFilename("file")    ; returns absolute path
```

读写文件都要通过 port，它类似于C的文件指针。SKILL预定义的port有`piport, poport, errport, ptport, woport`，前三个相当于C的`stdin, stdout, stderr`，后两个等同于`stdout`，用于输出trace和warning

```lisp
; opening ports
read_port = infile("file")   ; nil if file not exist / not readable
write_port = outfile("file" "w")

; reading ports
fscanf(read_port "%d %f" i d)
gets(str read_port)  ; read a line and stores to variable str
getc(read_port)      ; read a char and returns it

; writing ports
fprintf(write_port "this is a %s message" "log")

; closing ports
close(read_port)
drain(write_port)  ; flush buffer to file
close(write_port)  ; flush & close
```

读取脚本

```lisp
load("myScript.il")     ; load & execute file
loadi("myScript.il")    ; similar to load, but ignores errors

; declaring autoload property
; Will auto load definition when called
fn.autoload = "myScript.il" 

; reads a line, and returns a list of input objects
pi = infile("myScript.il")
lineread(pi)
; e.g. line 1 is "f(a b c)"
; this will return '(f a b c)
```

也可以打开字符串的port

```lisp
s = "Hello World"
pi = instring(s)
fscanf(pi, "%s" a)  ; a = Hello
```

## 字符串操作与输出

```lisp
; println：打印并自动换行（print line，不支持格式化输出）到poport
println("Hello, world")

; pprint：pritty print，打印长列表时比较好看
pprint('(1 2 3 4 5 6 7 8 9 10))

; printf：格式化输出
printf("%.2f" 96.3534)

; fprintf：输出到指定端口，常用于写入到文件
fprintf(port "x = %n" 42)

; sprintf：输出到变量
sprintf(s "%L" (1 2 3))         ; s = "(1 2 3)"
s = sprintf(nil "%L" (1 2 3))   ; same as above
```

格式化字符串的关键字和 C 差不多，特别地可以用`%L, %P, %B`格式化列表、点、方框；`%s`除了格式化字符串之外，还可以格式化 Symbol；用`%n`格式化整形数或者浮点数

# OCEAN

OCEAN（Open Command Environment for Analysis）是SKILL的子集，专门用于仿真

交互文档：`ocnHelp('commandName)`

## 创建与运行OCEAN脚本

最常见且简单的方法是从GUI创建OCEAN脚本

- 方法1：ADE L - Session - Save Ocean Script
- 方法2：Parametric Analysis - File - Save Ocean Script

然后从ocean交互界面（在命令行运行bash615之后执行指令`ocean`打开）或者从CIW运行脚本：`load "script.ocn"`

## Setup Simulation

自动生成的脚本里面已经包含了这一部分。将来哪天自动生成不够用了再补充这部分的笔记

注意：从GUI跑仿真的时候是“netlist and run”，但自动生成的脚本没有 netlist 步骤，因此要先用GUI跑一次，产生了网表再运行脚本。更改了电路之后也要先用GUI跑一次再运行脚本

用脚本生成netlist可以参考[这里](https://community.cadence.com/cadence_technology_forums/f/custom-ic-design/38480/post-layout-simulation-using-ocean-script)，大意是用`design`函数设置被仿真的Cellview、用`envOption`函数设置`switchViewList`，然后调用`createNetlist`函数。之前试过一次，不太成功，以后有必要再学

```lisp
; Design Variables
a = desVar("delay" 50p)     ; set design variable (and returns it)
b = desVar("delay")         ; get design variable

; 变量的值可以是表达式，且顺序无所谓
desVar("a" "b+1")
desVar("b" 1)
; a = 2, b = 1
```

## Run Simulator

这一部分同样被很好地自动生成了，一般没有动的必要

```lisp
; Parametric Analysis
paramAnalysis("var1" ?start 0 ?stop 200p ?step 10p
    paramAnalysis("var2" ?values '(100m 200m 300m))
)
paramRum()

; 使用for循环扫参数（不推荐，但需要在循环体内做特殊操作时不得不这么做）
for(v1 0 20
    desVar("var1" v1*20p)
    foreach(v2 '(100m 200m 300m)
        desVar("var2" v2)
        run()
    )
)
```

## Access Data

仿真结束之后，数据被存在`~/simulation/<testSchemName>/spectre/schematic/psf`文件夹内。可以用 CIW - Tools - ADE L - Results Browser - File - Open Result 选择打开（但是不建议，因为这里面包括了所有 net 的仿真数据，在GUI里面很难找想要的东西）

下一次仿真时，仿真结果会自动被删除。在此之前随时都可以打开

```lisp
; 打开仿真结果
openResults("~/simulation/testcell/spectre/schemetic/psf")

; 选择仿真类型
results()           ; 查看可选结果类别，比如tran，ac等
selectResult('tran) ; 也可以是selectResults

; 处理数据，绘制波形、打印数据
VIN = v("/VIN")
IIN = i("/IIN")

; cautious: v & i works in mysterious ways
getData("/VIN")    ; equivalent to VIN
i("/VIN")          ; equivalent to VIN
getData("/IIN")    ; equivalent to IIN

; 关闭仿真
ocnResetResults()
```

Parametric Analysis的数据获取略有区别。如果打开数据点的psf文件，那就和单次仿真相同；打开schematic文件夹下面的psf文件，可以选择被扫参数

```lisp
openResults("~/simulation/testcell/spectre/schemetic/psf")
selectResult('tran)
; 按照文档，可以用selectResult(result sweep_value)选择参数的值。但是实测第二个参数不影响选中结果

VIN = v("/I0/VIN")      ; 假设有两个被扫参数，那么VIN类似于三维数组，前两维是被扫参数，第三维是时间
IOUT = i("/I0/IOUT")

; 查看被扫参数。如果参数缺省就会返回当前选中结果的参数
var = sweepNames(VIN)               ; 返回被扫参数列表
val = sweepValues(VIN)              ; 第一个参数取值列表
sweepVarValues(VIN  nth(var 2))     ; 第n个参数取值列表
v0 = value(val car(var) car(val))   ; 大概可以把waveform当成数组，value当成[]。但是value能够插值
```

## Plot & Print Data

OCEAN的绘图没有面向对象的形式，只能用面向过程的绘图

```lisp
; 打开窗口
win_id = newWindow()    ; 打开新窗口。win_id是一个vtype对象
clearAll()              ; 或者不开新窗口，而是清除上次绘制的图，在原窗口重新绘图
; 又或者，什么都不做，直接绘图，和之前的图叠起来

; 绘图
plot(VIN IOUT ?expr '("VIN" "IOUT"))

; 窗口与子窗口操作
sub0 = currentSubwindow()   ; 获取当前活动的子窗口
currentSubwindow(sub0)      ; 切换子窗口
currentWindow()             ; 获取/设置当前绘图窗口
sub1 = addSubwindow()       ; 创建并切换到新的子窗口
```

