# 简介

https://www.php.net/manual/zh/langref.php

PHP是用于创建网站的服务器端脚本语言，它可以嵌入进HTML。服务器安装了PHP插件后访问此文件，插件会调用php代码执行业务逻辑、渲染网页

```php+HTML
<!DOCTYPE html>
<html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <?php echo "Hello World<br/>" ?>
        <?= "Hello World again<br/>"; ?>
        <? echo "Hello World<br/>" ?>
        <!-- 第一个是普通php标签；第二个是echo标签；第三个是短标签 -->
        <!-- 短标签需要php.ini配置启用short_open_tag -->
    </body>
</html>
```

以下代码以图书管理类`BookManager`为例展示了PHP基础语法

```php
class BookManager {
    private $books = [];

    public function addBook($title, $author, $isbn) {
        $this->books[] = [
            'title' => $title,
            'author' => $author,
            'isbn' => $isbn
        ];
    }

    public function findBook($isbn) {
        foreach ($this->books as $book) {
            if ($book['isbn'] === $isbn) {
                return $book;
            }
        }
        return null;
    }

    // 获取所有书籍
    public function getAllBooks() {
        return $this->books;
    }
}

// 使用示例
$manager = new BookManager();
$manager->addBook("PHP入门", "张三", "123456");
$manager->addBook("MySQL指南", "李四", "789012");
print_r($manager->findBook("123456"));
```

# 语法基础

## 变量

基础类型（整数、浮点数、布尔值等）从略

```php
# 单引号字符串。除了\'和\\之外不会转义
echo 'I\'m here';
# 双引号字符串。有转义字符、字符串插值
$i = 1;
echo "i = {$i}";

# 数组（Array）。即键值对
$arr1 = array("Peter"=>"43", "Brian"=>"7");
$arr2 = ['foo'=>'bar', 1:2];
echo $age['Peter'];

# 数组key缺省时，自动使用递增整数，看上去像其他语言的列表
$arr3 = ['a', 'b', 'c'];

${'var'} = 'name'; # 通过字符串访问变量，相当于$var
$$var = 'Alice';   # 可变变量。相当于$($var)，即$name。这行代码等同于$name = 'Alice'

```

## 运算符

一般运算从略，包括加减乘除、取模`%`、赋值、比较、逻辑（`and`和`&&`等都可以用）、三元。以下仅列出需要注意的运算符

| 运算符   | 名称       | 说明                                                     |
| -------- | ---------- | -------------------------------------------------------- |
| `==`     | 等于       | 值相等。不同类型比较会自动类型转换，如`'0e23' == 0`为真  |
| `===`    | 绝对等于   | 值和类型都相等。作用于数组时，需要键值对顺序和类型都相同 |
| `!=, <>` | 不等于     |                                                          |
| `!==`    | 不绝对等于 |                                                          |
| `.`      | 连接字符串 | `"Hello" . "World"`等于`"HelloWorld"`                    |

## 预定义变量

也叫超级全局变量（Superglobals），由系统预定义，在所有作用域中都可访问。若未额外说明，它们都是Array

| 变量名      | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| `$GLOBALS`  | 全局变量。比如`$GLOBALS['x'] = 1`相当于在函数外写`$x = 1`。无需多言，应该尽量避免使用它 |
| `$_SERVER`  | 服务器信息、当前脚本信息以及当前请求的信息                   |
| `$_POST`    | 请求的POST参数                                               |
| `$_GET`     | 请求的GET参数                                                |
| `$_COOKIE`  | 请求中发送的cookie                                           |
| `$_REQUEST` | 包括了`$_POST, $_GET, $_COOKIE`的内容                        |

## 控制流

```php
# if分支
$t = 10;
if ($t > 0) {
    echo "t is positive";
} elseif ($t < 0) {
    echo "t is negative";
} else {
    echo "t is zero";
}

# switch分支
$color = "red";
switch ($color) {
    case "red":
        echo "It's red";
        break;
    default:
        echo "It's not red";
}

# for循环
$cars = array("Volvo", "BMW", "Toyota");
for($x=0; $x < count($cars); $x++) {
    echo $cars[$x] . "<br />";
}

# foreach循环
foreach ($cars as $car) {
    echo $cars[$x] . "<br />";
}
$age = array("Peter"=>"43", "Brian"=>"7");
foreach ($age as $key=>$value) {
    echo $key . ' ' . $value;
}
```

# 函数

```php
# 定义函数
function make_coffee(&$cnt, $name='Alice', $coffee='espresso') {
    $cnt += 1;   # 此参数是引用传参。类似C++的引用
    echo "Making a cup of $coffee for $name";
    return 0;    #返回值。缺省时返回null
}

# 调用函数
$i = 1;
make_coffee($i, 'Bob');
func1 = "print_name";             # 变量函数，即函数指针
func1($i, coffee:'Coffe Latte');  # 命名参数。8.0.0以上可用

# 匿名函数、箭头函数（Lambda函数）	
$func2 = function ($x) use ($i) {   # 从父作用域继承变量必须用use，继承的是定义时的值
    return $x * $i;
};
$func3 = function ($x) use (&$i) {  # 引用继承以实现闭包
    return $x * $i;
}
$fn = fn($x) => $x * $i;

# 类型声明
function func4(bool $ok, int $x): int {
    return $ok ? $x : 0;
}
```

# 类和对象

```php
# 定义类
class Site {
    # 成员变量
    public $url;
    # 成员函数
    function __construct($url, $title) {  # 构造函数
        $this->url = $url;
    }
    function __destruct() {} # 析构函数
    function set_url($par) {
        $this->url = $par;
    }
}

# 实例化
$taobao = new Site();
$taobao->set_url("taobao.com");
```

## 魔术方法

### 序列化和反序列化

```php
class Connection {
    protected $link;
    private $dsn, $username, $password;

    public function __construct($dsn, $username, $password) {
        $this->dsn = $dsn;
        $this->username = $username;
        $this->password = $password;
        $this->connect();
    }

    private function connect() {
        $this->link = new PDO($this->dsn, $this->username, $this->password);
    }

    # 序列化时保存__sleep指示的属性；反序列化时重新加载属性之后执行__wakeup
    public function __sleep() {
        return array('dsn', 'username', 'password');
    }
    public function __wakeup() {
        $this->connect();
    }

    # 也可以用__serialize和__unseralize完全控制序列化和反序列化行为
    # 定义了__serialize就不会调用__sleep，有__unserialize就不用__wake
    public function __serialize(): array {
        return [
          'dsn' => $this->dsn,
          'user' => $this->username,
          'pass' => $this->password,
        ];
    }
    public function __unserialize(array $data): void {
        $this->dsn = $data['dsn'];
        $this->username = $data['user'];
        $this->password = $data['pass'];
        $this->connect();
    }
}
```

# IO

## 打印到stdout

```php
# echo和print，不是函数，打印字符串和整数（其他东西可能打不全或者报错）
echo 'Hello ', 'World';   # echo可以一次打多个变量。print不行
print 3.14;

# print_r，打印数组。其他东西一般也可以
print_r(['a', 'b', 'c']);

# var_dump，打印变量完整信息
var_dump(true);   # bool(true)，用其他几个函数打印出来是1
var_dump(NULL);   # NULL，其他几个函数什么都打印不出来
```

## 文件读写

基础

```php
# 读写文件
$content = file_get_contents('info.php');
file_put_contents('info_copy.php', $content);

# 用文件指针操作文件
$fp = fopen('test.txt', 'w');
fwrite($fp, 'Hello, World');
fclose($fp);
```

其他

```php
echo highlight_file('info.php');  # 打印源代码
    # 注意：用echo file_get_contents打印的话会被当作代码执行，highlight_file则不会
```



## 封装协议

[PHP封装协议](https://www.php.net/manual/zh/wrappers.php)，俗称伪协议，可把数据、IO流等当作文件处理

```php
$file = 'data://text/plain,<?php phpinfo();?>';
```

以上例子将文本封装为“文件”，使用`fopen, readfile, include, require`等函数打开此“文件”，访问其中内容：`<?php phpinfo();?>`。更多例子有：

```shell
# 数据流
'data://text/plain,<?php phpinfo();?>'
'data://test/plain;base64,PD9waHAgcGhwaW5mbygpOz8='

# 本地文件（主要是为了兼容性，和直接用文件路径效果相同）
'file:///etc/passwd'

# IO流
# 读取src.php，并用base64-encode处理读到的数据。base64编码可以阻止代码执行，从而实现任意文件读取
'php://filter/read=convert.base64-encode/resource=src.php'

# 访问压缩文件。完整列表看文档
'zip://shell.zip'
'phar://shell.phar'
```

封装协议能否使用取决于`allow_url_fopen`和`allow_url_include`配置，`data://`需要两个都设置为True，`file://`和`php://filter`不需要

# 操作系统

## 系统命令

```php
system('ls', $out);       # 输出到stdout，返回值存进$out
exec('ls', $out);         # 输出以Array存进$out
$out = shell_exec('ls');  # 返回输出的str
echo `whoami`;            # 反引号的内容当作指令执行
```

## 文件

```php
print_r(scandir('.'));  # 列出子目录、子文件
print_r(glob('*'));     # 遍历目录

if(preg_match("/[A-Za-oq-z0-9$]+/",$cmd)){
    die("cerror");
}
if(preg_match("/\~|\!|\@|\#|\%|\^|\&|\*|\(|\)|\（|\）|\-|\_|\{|\}|\[|\]|\'|\"|\:|\,/",$cmd)){
    die("serror");
}
```

# 其他

## 命名空间

通常在脚本开头声明命名空间：

```php
namespace MyProject;
```

偶尔也会在一个脚本中定义多个命名空间，用大括号括起来：

```php
namespace MyProject {
    const CONNECT_OK = 200;
}

namespace {  # 没有namespace名，声明为全局代码
    const CONNECT_OK = 200;
}
```

可以用类似目录的格式定义子命名空间：

```php
namespace MyProject\Sub;
const CONNECT_OK = 201;
```

引用命名空间中的变量

```php
namespace MyProject;

echo CONNECT_OK;                # 非限定名称：当前命名空间
echo Sub\CONNECT_OK;            # 限定名称：相对路径
echo \MyProject\Sub\CONNECT_OK; # 完全限定名称：绝对路径
```

## 连接MySQL

常用的有MySQLi和PDO两套接口。其中MySQLi插件针对MySQL设计，支持异步查询等MySQL特有的功能；PDO支持多种数据库。一般项目推荐使用PDO；只用MySQL、且需要做数据库性能优化的项目使用MySQLi

### MySQLi

```php
# 创建连接
$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die('连接失败: ' . $conn->connect_error)
}

# 操作数据库
$result = $conn->query('SELECT name FROM guests WHERE id=1;');
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        echo $row['name'];
    }
}
```

### PDO

```php
# 创建连接
$conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
 
// 操作数据库
$stmt = $conn->prepare("SELECT name FROM guests WHERE id=1;"); 
$stmt->execute();
$result = $stmt->setFetchMode(PDO::FETCH_ASSOC); 
foreach(new TableRows(new RecursiveArrayIterator($stmt->fetchAll())) as $k=>$v) { 
    echo $v;
}
```

## 杂项

```php
@(include('file.php')) or die('FileNotFound');
```

- `@`：[错误控制符](https://www.php.net/manual/zh/language.operators.errorcontrol.php)。在表达式前面加上`@`，表达式中出现的任何错误都被抑制。出错时表达式的值为`NULL`
- `or`：逻辑运算符，若前面没有出错，表达式为真，不会执行后面的表达式；否则就会调用`die`函数
- `die`：`exit`函数的别名，它将参数打印到stdout并退出当前脚本



