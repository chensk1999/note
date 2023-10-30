Tcl是一种脚本语言，它无类型，全部东西都可被解释为字符串

# 基本语法

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

# 数据类型

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

# 运算符

四则运算、取余、关系、位运算、布尔算符从略；乘方`**`，三目运算符`?:`

| Operator | Usage      |
| -------- | ---------- |
| eq, ne   | 字符串比较 |
| in, ni   | 列表包含   |

# 控制流

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

# 过程

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

