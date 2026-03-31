本笔记记录仅仅略微接触过的语言

# Go

Go是Google开发的一种静态强类型、编译型、并发型，并具有垃圾回收功能的编程语言。它的并发性能较好，常用于服务器后端

Go语言的语法类似C

```go
package main

import "fmt"

func main() {
    fmt.Println("Hello, World!")
}
```

https://www.runoob.com/go/go-structures.html

## 变量

```go
// 声明变量。类型可以省略，省略时自动推断
var i int = 0
var s string = "Hello"

func f(){
    b := false   // 隐式声明变量。会自动推断类型。只能在函数内使用
}

// 常量
const LENGTH int = 10

// 数组与指针
var balance = [5]float32{1000.0, 2.0, 3.4, 7.0, 50.0}
var arr = [...]int{0, 1, 2, 3, 4}  // 自动判断长度
var pointer *int = &i
if pointer != nil {
    fnt.Printf("i = %d\n", *pointer)
}

// 切片。切片是对数组的引用，它可以实现变长数组
var slice []int = arr[0:3];
```

## 运算符

和C基本一致

## 控制流

和C基本一致，区别是条件不需括起来。以下记下不同之处

```go
strings := []string{"google", "runoob"}
for i, s := range strings {
    fmt.Println(i, s)
}
```

## 函数

```go
func swap(x, y string) (string, string) {
   return y, x
}
```

# Perl

Perl是一个解释型动态编程语言家族，Linux、MacOS等操作系统中默认安装Perl

Perl语言的中心思想是

> There's More Than One Way To Do It.

与Python的思想（There should be one, and preferably only one, obvious way to do it）正好相反。它给了很多灵活性，但是让语法冗余、不易读

```bash
# 检查是否安装Perl
perl -v
# 命令行直接运行Hello World
perl -e 'print "Hello World\n"'
# 运行脚本
./hello.pl
```

`hello.pl`的内容如下：

```perl
#!/usr/bin/perl
use strict;
use warnings;

print("Hello World\n");
```

注意，Perl调用函数并不靠括号——把函数名写出来就是调用了，函数名后面跟的一个表达式自动成为参数，括号在这个例子中没有语法作用

## 变量与表达式

```perl
# 标量（Scalar）
$a = 123;
print("a = $a\n");

# 数组（Array）
@arr = ('x', 'y', 'z');
print("arr[0] = $arr[0]\n");
# 数组序列
@var_10 = (1 .. 10);
@var_alphabet = ('a' .. 'z');
# 数组大小：标量上下文中的数组为其大小
print scalar @array, "\n";
# 添加和删除数组元素
push(@arr, 'w');     # 在末尾添加元素
pop(@arr);           # 弹出末尾元素
shift(@arr);         # 移除第一个元素
unshift(@arr, 'w')   # 在开头添加元素
splice(@var_10, 5, 3, 1..10);   # 将var_10[5]开始的3个元素替换为1..10
# 切割数组
@arr[1, 2, 3];
@arr[1..3];

# 关联数组（Associative Array / Hash）
%data = ('a', 1, 'b', 2, 'c', 3);
print "data{'a'} = $data{'a'}\n";
```

Perl是无类型语言，并且变量不需要声明。所有变量默认为全局变量

**上下文**：Perl会根据左值判断上下文，右值在不同上下文计算得到不同结果

```perl
@arr = 1..10;

$n = @arr;      # 标量上下文，对数组求值得到数组长度10
@arr2 = @arr;   # 数组上下文，求值得到数组本身

$n = scalar(@arr);  # 显式使用标量上下文
```

**特殊变量**

| 变量名 | 全名   | 说明                                                         |
| ------ | ------ | ------------------------------------------------------------ |
| `$_`   | `$ARG` | 默认迭代变量；默认输入（许多函数和部分运算符在不指定输入输出变量时使用它） |

使用全名需要在程序开头添加`use English`

[其他特殊变量](https://www.runoob.com/perl/perl-special-variables.html)

**字符串**

```perl
# 双引号字符串，内部的转义字符、变量会被转义
$a = 100;
print("$a\n");  # 打印100并换行
# 单引号字符串，不转义
print('$a\n');  # 打印$a\n四个字符

# 分割字符串、连接字符串
$text = "some random text";
@words = split(' ', $text);
$new_text = join(' ', @words);

# V字符串：以数字编码表示文本(.用于连接字符串)
$martin = v77.97.114.116.105.110; 
print($martin);

# 引号运算
$a = 10;
$b = q{a = $a};     # 单引号
print("$b\n");      # 输出a = $a
$c = qq{a = $a};    # 双引号
print("$c\n");      # 输出a = 10
```

**引用**

```perl
$foo = 1;
$foo_ref = \$foo;
$$foo_ref += 1;
print("$foo\n");
```

其他数据类型的引用同理。如`\@`引用数组，`\%`引用哈希表

```perl
# 引用函数
sub func {
    return 0;
}

$fref = \&func;
&$fref();
```

## 控制流

**分支**

```perl
$a = 10;

# if块
if ($a >= 0) {
    print($a);
} elsif ($a > 100) {
    print("$a > 100\n");
} else {
    print("a < 0\n");
}

# if语句
print("a == 10\n") if $a == 10;

# unless块和unless语句
# 同上

# given-when块和given-when语句，类似于switch
given ($foo) {
    print("foo = 1") when 1;
    when 2 {print("foo = 2")}
    default {print("not match")}
}

# 无关键字的分支
($a > 0) ? $a : -$a;    # 三目运算符
open(DATA, '<', "text.txt") or die("cannot open file");
# 利用or运算符的特性，只有前一个表达式为假，才会计算第二个表达式
```

**循环**

```perl
@arr = 1 .. 10;

# C的循环
$sum = 0;
for ($i=0; $i<10; $i++) {
    $sum += $arr[i];
}

# Perl循环（for和foreach可以互换）
for (@arr) {
    $sum += $_;
}

# 指定循环变量名称（指定之后，$_好像会变成未定义）
for $a (@arr) {
    print("$a\n");
}

# while循环、do...while循环、until循环、do...until循环

# continue语句：每次条件判断之前执行。可以和while以及for搭配
for (@arr) {
    $sum += $_;
} continue {
    print("$sum\n");
}

# 循环语句
# next: 跳转到continue块
# last: 跳出循环
# goto, redo: Make some spaghetti
```

## 函数

```perl
# 定义函数。函数定义没有形参列表，传入参数为@_
# 传入的全部参数被按顺序塞进一个数组，如果需要列表或关联数组参数，要引用传参
# 需要返回多个值的时候同理
sub average {
    my $n = scalar(@_);	     # my操作符定义私有变量
    my $sum = 0;
    for $item (@_) {
        $sum += $item;
    }
    return $sum / $n;
}

# 调用函数。函数右边的表达式以列表上下文求值作为参数
average(1, 2, 3);
average 1, 2, 3;
average (abs -1), 2, 3;
```

## 文件与目录

### 读写文件

```perl
# 读文件
open($fp, "<", "file.txt") or die("Couldn't open file file.txt, $!");
# $fp为文件句柄；<表示读文件

# 尖括号操作符读取文件
@lines = <$fp>;         # 列表上下文，读取整个文件
for $line (<$fp>) {     # 标量上下文，读取一行
    print($line)
}

close($fp);

# 写文件
open($fp, ">>", "file.txt") or die("Couldn't open file file.txt, $!");
print $fp "This line is added in the file1.txt\n";
# 注意：$fp和文字中间没有逗号。调用关系应该是print($fp("text"))
# 但是$fp("text")会报错，无法理解发生了什么
close($fp);
```

| 访问模式 | C-equivalent | 说明   |
| -------- | ------------ | ------ |
| `<`      | r            | read   |
| `>`      | w            | write  |
| `>>`     | a            | append |

### 目录操作

```perl
# 获取目录下的文件
@files = glob(./*.pdf);
# 创建与删除目录
$dir = "/tmp/perl"
mkdir($dir) or die("Couldn't create $dir, $!");
rmdir($dir) or die("Couldn't remove $dir, $!");
# 切换目录
chdir("/home") or die("Couldn't switch to /home, _!");
```

## 正则表达式

```perl
# 匹配表达式。返回匹配成功与否
$text = "foo foo";
$pattern = m/foo/;
if ($text =~ $pattern) {
    print("Matched\n");
}

# 数组上下文，并且有分组，返回匹配到的内容
$time = "Jan 1, 13:10:02";
($hour, $minute) = ($time =~ m/(\d+):(\d+):\d+/);

# 正则的特殊变量
"The food is in the salad bar" =~ m/foo/;
print("Before:  $`\n");
print("Matched: $&\n");
print("After:   $'\n");

# 替换(Substitution): s/PATTERN/REPLACEMENT/
$string = "The cat sat on the mat";
$string =~ s/cat/dog/;  # 将cat替换为dog

# 转化(Translation): tr/SEARCHLIST/REPLACEMENTLIST/
$string = 'The cat sat on the mat';
$string =~ tr/a/o/;     # 将字母a转化为字母o
$string =~ tr/a-z/A-Z/; # 将小写字母转化为大写字母
```

# Ruby

Ruby是面向对象的动态编程语言，其定位和Python类似。2000年代后期为Ruby的全盛期，出现许多用Ruby编写的项目，许多网站使用Ruby on Rails框架（如当年的Github和推特都使用RoR）。2010年代中期开始，由于性能劣势（和python坐一桌），又没赶上大数据和AI浪潮，逐渐式微

它还吸收了perl的部分设计思想，包含大量语法糖，一件事可以有很多种写法，这也是许多人诟病的点

```shell
ruby -v
irb      # Ruby交互式Shell
```

## 基础语法

变量

- 一般小写字母、下划线开头：变量（Variable）。
- `$`开头：全局变量（Global variable）。
- `@`开头：实例变量（Instance variable）。
- `@@`开头：类变量（Class variable）类别变量被共享在整个继承链中
- 大写字母开头：常量（Constant）和类名

```ruby
# 字符串
puts 'That\'s right'   # 单引号字符串，只会转义\'和\\
puts "1 + 1 = #{1+1}"  # 双引号字符串，支持反斜杠转义和字符串格式化

# 数组
arr = [1, 'a', 'b']

# 哈希
```

控制流

```ruby

```

## 函数

- `=`结尾：赋值方法，相当于其他编程语言的`set`开头的方法，算是一种[语法糖](https://zh.wikipedia.org/wiki/語法糖)。
- `!`结尾：破坏性方法，调用这个方法会修改本来的对象，这种方法通常有个非破坏性的版本，调用非破坏性的版本会回传一个对象的副本。
- `?`结尾：表示这个函数的回传值是个布尔值。

## 类和对象

```ruby
class Customer
    @@total = 0

    def initialize(id, name)  # 构造函数
        @id = id
        @name = name
        @@total += 1
    end
end

obj = MyClass.new
```

# Tcl

Tcl是一种脚本语言，它无类型，全部东西都可被解释为字符串。常用Tcl解释器有[TclKits](https://tclkits.rkeene.org/fossil/wiki/Downloads)，ActiveTcl，Linux的tcsh、tclsh

## 基本语法

```tcl
# 单行命令
command arg1 arg2 arg3
# 一行内运行多个命令，用;隔开
cmd1 arg1; cmd2 arg2

# 变量以及引用变量
set name Chen
puts $name

# 方括号运算
puts [expr 1+1]

# 转义字符
puts \$name
```

## 数据类型

```tcl
# 双引号字符串。双引号会发生变量替换
puts "My name is $name"     # result: My name is Chen

# 大括号字符串。内部不发生替换
puts {My name is $name}     # result: My name is $name

# 列表
set l1 {1 2 3}
set l2 [list 1 2 3]
puts [lindex $l1 0]

# 关联数组
set  marks(english) 80
puts $marks(english)
```

## 运算符

四则运算、取余、关系、位运算、布尔算符从略；乘方`**`，三目运算符`?:`

| Operator | Usage      |
| -------- | ---------- |
| eq, ne   | 字符串比较 |
| in, ni   | 列表包含   |

## 控制流

```tcl
set a 0

# if-else
if no then {
    puts "yes/no are boolean. then is optional"
} elseif {$a == 0} {
    puts "use \{\} instead of \(\)"
} else {
    puts "It's like C, but you must use \{\}"
}

# switch
set domain us
switch $domain {
    us { puts "United States" }
    de { puts "Germany" }
    default { puts "Unknown" }
}

# while loop
set i 0
set sum 0
while {$i < 100} {
    incr i
    incr sum $i
}
puts $sum

# for loop
set sum 0
for {set i 0} {$i < 100} {incr i} {
    incr sum $i
}

# foreach loop
set days {Mon Tue Wed Thu Fri Sat Sun}
foreach day $days {
    puts $day
}

# continue & break
set i 0
set sum 0
while {true} {
   incr i
   if {$i%2 == 0} {
       continue
   } elseif {$i > 100} {
       break
   }
   incr sum $i
}
```

## 过程

```tcl
# 定义过程
proc maximum {x y} {
    return {$x > $y} ? $x : $y
}

# 调用过程
puts [maximum 1 2]

# 参数默认值
proc plus {a {b 1}} {
    return [expr $a + $b]
}

# 特别地，args作为参数名可以接收任意个参数，接收到的东西组成一个list
proc sum {args} {
    set s 0
    foreach arg $args {
        incr s $arg
    }
    return $s
}

# 外部变量与全局变量
set x 1
set y 2
proc test {} {
    upvar x
    global y
    puts "x = $x, y = $y"
}
test
```

