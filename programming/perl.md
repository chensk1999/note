Perl是一个解释型动态编程语言家族，Linux、MacOS等操作系统中默认安装Perl

Perl语言的中心思想是

> There's More Than One Way To Do It.

与Python的思想（There should be one – and preferably only one – obvious way to do it）正好相反。它给了很多灵活性，但是让语法冗余、不易读

```bash
# 检查是否安装Perl
perl -v
# 命令行直接运行Hello World
perl -e 'print "Hello World\n"'
# 运行脚本
./hello.pl
```

hello.pl的内容如下：

```perl
#!/usr/bin/perl
use strict;
use warnings;

print("Hello World\n");
```

注意，Perl调用函数并不靠括号——把函数名写出来就是调用了，函数名后面跟的一个表达式自动成为参数，括号在这个例子中没有语法作用

# 变量与表达式

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

## 上下文

Perl会根据左值判断上下文，右值在不同上下文计算得到不同结果

```perl
@arr = 1..10;

$n = @arr;      # 标量上下文，对数组求值得到数组长度10
@arr2 = @arr;   # 数组上下文，求值得到数组本身

$n = scalar(@arr);  # 显式使用标量上下文
```



## 特殊变量

| 变量名 | 全名   | 说明                                                         |
| ------ | ------ | ------------------------------------------------------------ |
| `$_`   | `$ARG` | 默认迭代变量；默认输入（许多函数和部分运算符在不指定输入输出变量时使用它） |

使用全名需要在程序开头添加`use English`

[其他特殊变量](https://www.runoob.com/perl/perl-special-variables.html)

## 字符串

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

## 引用

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

# 控制流

## 分支

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

## 循环

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

# 函数

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

# 文件与目录

## 读写文件

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

## 目录操作

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

# 正则表达式

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

