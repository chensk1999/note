Cadence SKILL是Virtuoso以及部分Cadence公司的软件使用的语言。它是一种Lisp方言

# 数据结构

## 数字

```lisp
; 整数
'(15 0b1111 017 0xf)

; 浮点数。可以用国际单位制的词头作为后缀
'(0.015 1.5e-2 15m)
```

## 符号

符号 ≈ 指针；一般来说，直接使用符号会对符号求值（即取得它指向的对象），因此也经常用符号指变量

```lisp
; 用quote操作符作用的符号不会被求值（即依然是指针）
a = 10
b = a       ; b = 10, type(b) = fixnum, type('b) = symbol
c = 'a      ; c = 'a, type(c) = symbol

; 操作指向符号的符号
set(c 5)        ; a = 5
b = symeval(c)  ; b = a

; 作为宏/某些特殊函数的参数时，符号会表示它自己，而不会被求值
; 此时称作implicitly quoted
setq(c 5)       ; c = 5, 等效于赋值运算

; 用函数操作符号
gensym("net")       ; 产生符号，会自动加后缀以区分
gensym('net)
get_pname('net)     ; 获取符号的打印名
```

**Property List**

每个符号都有一个Property List，其效果类似其他语言的结构体。符号的默认Property List都是nil

```lisp
; 定义属性
a.x = 100
putprop('a 200 'y)
setplist('b '(x 100 y 200))

; 访问属性
plist('a)
b.x
get('b 'y)
b.z     ; 访问不存在的属性，返回nil

; 用->运算符访问属性
c = 'a
c->x
```

注意：property list是全局的，有的时候同名变量（即使一个是局部变量，另一个是全局变量）会共用property list

## 列表

列表（List）是SKILL最核心的数据类型。其底层实现是链表

```lisp
; 定义列表
a = '(1 2 3)
b = list(1 2 3)

c = cons(1 a)       ; 在列表头添加元素
d = append(a b)     ; 拼接列表

; 访问列表
car(a)      ; 访问列表首元素(Contents of the Address part of Register)
cdr(a)      ; 引用首元素之外的元素，即链表首节点的Next指针(Contents of the Decrement part of Register)
nth(0 a)    ; 访问第n个元素（下标从0开始）
length(a)   ; 列表长度

member(1 '(0 1 2))  ; 寻找列表元素
; 若没找到，返回nil；找到时，返回从该元素开始的子列表
; 此例子中，返回'(1 2)
```

特别地，可以用二元列表表示坐标，用包含两个二元列表的列表表示方框。SKILL提供了一些特殊方式来操作这种列表

```lisp
; 用冒号定义坐标
coord = 300:400     ; (300 400)

; 提取坐标
x = xCoord(coord)
y = yCoord(coord)

; 用左下角、右上角坐标表示bounding box
bBox = '(300:400 500:450)

; 用car和cdr的复合函数引用四个角的坐标
ll = car(bbox)     ; 左下坐标
ur = cadr(bbox)    ; car(cdr(bbox))，右上坐标
llx = caar(bbox)   ; car(car(bbox))，左下x坐标
lly = cadar(bbox)  ; car(cdr(car(bbox)))，左下y坐标
urx = caadr(bbox)  ; car(car(cdr(bbox)))，右上x坐标
ury = cadadr(bbox) ; car(cdr(car(cdr(bbox))))，右上y坐标
```

## 字符串

```lisp
; 连接字符串
strcat("a" "b" "c")             ; "abc"
buildString('("a" "b" "c") ".") ; "a.b.c"

evalstring("1+2")   ; evaluate & return expression
loadstring("procedure(f(n) if(n==0 1 f(n-1)*n))")
                    ; parse & execute expression, return t if success
```

## Array

```lisp
; 声明数组
declare(arr[3])   ; declare array with 3 elements
arr[0] = 1
arr[1] = 3.14
arr[2] = "whatever"
arr[3]      ; index out of bound
```

## 运算符

SKILL的所有运算符都有两种写法，Operator形式用中缀表达式进行运算，Function形式用函数调用方式进行运算。一般会使用 Operator 形式，但由于错误信息会用 Function 形式，有必要把两种都记住

| Operator               | Function                                   | Note                                                         |
| ---------------------- | ------------------------------------------ | ------------------------------------------------------------ |
| `<, <=, >, >=, ==, !=` | lessp, leqp, greaterp, geqp, equal, nequal | Returns t or nil                                             |
| `&&, ||`               | and, or                                    | 表达式值为最后一个计算的值。在结果为真时，对于and是最后一个值；对于or，是第一个非nil值 |

### Quote

```lisp
; 单位元，(quote arg) -> arg。可缩写为'arg，quote作用的对象不会被求值
nil         ; 求值得到自身
'nil        ; quote单位元性质，得到nil自身
(+ 3 5)     ; 求值得8
'(+ 3 5)    ; 单位元性质，得到原列表。原列表不会再被求值
(defparameter SYMBOL 10)
SYMBOL      ; 10。符号求值得到它指向的对象
'SYMBOL     ; SYMBOL。符号不被求值，得到符号自身（即指向10的指针）
```

简单的说，无 quote 的对象可以是表达式、函数，有 quote 的对象可以当作是数据、变量

## 表达式

表达式从左到右求值。字面值的值是自身，符号的值是它指向的对象，列表的值是将第一个元素作为函数、剩余元素作为实参求得的值

```lisp
5       ; 5
(+ 2 3) ; 5
(/ (* 7 9) (- 5 2))     ; = (7*9) / (5-2) = 21
```

# 控制流

```lisp
; if-then-else （注意：if和括号中间不能有空格）
; 控制流其实都是函数，而函数调用当然不允许函数名和括号中间有空格
; 从Lisp的角度看if函数：如果第一个参数为真，计算第二个参数的值并返回；否则，计算第三个参数的值并返回
if( shape == "rect" then
    println("Shape is rectangle")
    rectCnt++
else
    println("Shape is not rectangle")
)

; when分支和unless分支
; 略

; case分支
; 如果匹配到了某个分支，计算该分支并返回；若未匹配，则计算最后一个分支
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

; for 循环。注意循环变量只能是int
; 循环变量不影响外部同名变量。for函数总是返回t
sum = 0
for( i 1 5      ; i从1到5
    sum = sum + i
)

; foreach循环
; 类似for循环，foreach不影响外部同名变量。foreach总是返回被迭代的列表
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
```

# 函数

**定义函数**

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

**调用函数**

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

# IO

```lisp
print("Hello")         ; 用默认打印格式打印
println("World")       ; 比print多一个换行符
printf("%.3f\n" a)     ; 用自定义格式输出
fprintf(port "%n" 42)  ; 输出到指定端口，常用于写入到文件
pprint('(1 2 3))       ; pretty paint，打印长列表时比较好看
s = sprintf(nil "%L" '(1 2 3))  ; 输出到指定端口，然后返回该字符串（此例子中端口为nil，格式化字符串仅返回到s，没有输出）
```

格式化字符串的关键字和 C 差不多，特别地可以用`%L, %P, %B`格式化列表、点、方框；`%s`除了格式化字符串之外，还可以格式化 Symbol；用`%n`格式化整形数或者浮点数

## 文件操作

```lisp
; 判断文件存在
isFile("filename")  ; t or nil
isDir("dirname")

; 判断文件读写权限
isReadable("file_or_dir")
isWritable("file_or_dir")
isExecutable("file_or_dir")

getDirFiles("dir")          ; list files in directory
simplifyFilename("file")    ; returns absolute path
```

读写文件都要通过 port，它类似于C的文件指针。SKILL预定义的port有`piport, poport, errport, ptport, woport`，前三个相当于C的`stdin, stdout, stderr`，后两个用于输出trace和warning

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

反斜杠表示续行

```lisp
s = "this is a long \
string"
```



# 常用函数

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

; sprintf：数字转字符串
sprintf(s "%L" (1 2 3))         ; s = "(1 2 3)"
s = sprintf(nil "%L" (1 2 3))   ; same as above

; 字符串转数字
atof("2.5e-3")
atoi("13.0")
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

## 运行仿真

从GUI界面要容易得多，而且没什么是必须用OCEAN脚本做的，强烈不建议用脚本运行仿真。此部分笔记略过

## 访问数据

仿真数据默认存在`~/simulation/`目录下的`psf`文件夹内（存储位置可以在`.cdsenv`文件中设置）。可以用 CIW - Tools - ADE L - Results Browser - File - Open Result 选择打开（但是不建议，因为这里面包括了所有 net 的仿真数据，在GUI里面很难找想要的东西）

用ADE L仿真时，每次仿真开始时自动删除之前的仿真结果；ADE XL则保存最近的10个结果（可以在Options - Save设置）

```lisp
; 打开仿真结果
openResults("~/simulation/testcell/spectre/schemetic/psf")

; 选择仿真类型
results()           ; 查看可选结果类别，比如tran，ac等
outputs()           ; 查看所有器件和net名
selectResult('tran)
; 在ADE XL的Output Setup添加的脚本不需要这两步

; 处理数据，绘制波形、打印数据
VIN = v("/VIN")
IIN = i("/IIN")

; 仿真参数
vgs = desVar("vgs")  ; Design Variable
W = VAR("W")         ; Global Variable

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
var = sweepNames()        ; 返回被扫参数列表
sweepVarValues("vb")      ; 参数"vb"的取值列表
v0 = value(val "vb" 400m) ; 当vb取值为400m的波形
```

**底层数据结构**

用前文方法读取到的数据是`srrWave`对象，用起来很方便，但是有时候仍需要直接访问底层的`srrVec`对象：

```lisp
xvec = drGetWaveformXVec(VT("/VOUT"))   ; 获取X轴向量（通常是时间）
xlen = drVectorLength(xvec)             ; 向量长度
x_last = drGetElem(xvec xlen-1)         ; 访问向量元素
```

## Plot & Print Data

OCEAN的绘图没有面向对象的形式，只能用面向过程的绘图

```lisp
; 打开窗口
win_id = newWindow()    ; 打开新窗口
clearAll()              ; 或者不开新窗口，而是清除上次绘制的图，在原窗口重新绘图
; 又或者，什么都不做，直接绘图，和之前的图叠起来

; 窗口与子窗口操作
sub0 = currentSubwindow()   ; 获取当前活动的子窗口
currentSubwindow(sub0)      ; 切换子窗口
currentWindow()             ; 获取/设置当前绘图窗口
sub1 = addSubwindow()       ; 创建并切换到新的子窗口

; 绘图
plot(VIN IOUT ?expr '("VIN" "IOUT") ?strip 1)

; log scale
ocnSetAttrib(?XScale 'log)

; 打印结果
ocnPrint(VOUT ?output "out.csv" ?precision 6 ?from 0 ?to 1 ?step 0.01 ?numberNotation 'scientific)
```

## ADE XL的ocean script

```lisp
vin = VT("/VIN")
vout = VT("/VOUT")

axlAddOutputs('("VIN")) ; 用脚本添加Output
axlOutputResult(vin "VIN")
axlOutputResult(vout)   ; Script本身的Output，不需Output名

calcVal("outputName" "test_name")   ; 获取其他test的Output
```

在GUI选择Plot任何一个脚本输出，都会把整个脚本跑一遍（不过Plot标量时不会。估计标量被存储起来，数组就不会）
