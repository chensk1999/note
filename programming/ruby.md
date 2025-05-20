Ruby是面向对象的动态编程语言

```shell
ruby -v
irb      # Ruby交互式Shell
```

它吸收了perl的一部分思想，一件事可以有很多种写法

# 基础语法

## 变量

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

## 控制流

```ruby
```



# 函数

- `=`结尾：赋值方法，相当于其他编程语言的`set`开头的方法，算是一种[语法糖](https://zh.wikipedia.org/wiki/語法糖)。
- `!`结尾：破坏性方法，调用这个方法会修改本来的对象，这种方法通常有个非破坏性的版本，调用非破坏性的版本会回传一个对象的副本。
- `?`结尾：表示这个函数的回传值是个布尔值。

# 类和对象

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

