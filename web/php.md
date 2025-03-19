# 简介

PHP是用于创建网站的服务器端脚本语言

```php+HTML
<!DOCTYPE html>
<html>
  <body>

    <h1>My first PHP page</h1>

    <?php
    echo "Hello World!";
    ?>

  </body>
</html>
```

# 变量

## 数据类型

```php
# 整数、浮点数、布尔从略
$s = 'abc';  # 字符串。也可以用双引号

# 数值数组。即一般的数组
$arr = array('a', 'b', 'c');    # 定义数组
echo $arr[0];                   # 访问数组
echo count($arr);

# 关联数组。即字典
$dict = array("Peter"=>"43", "Brian"=>"7");
echo $age['Peter'];
```

## 运算符

一般运算从略，包括加减乘除、取模`%`、赋值、比较、逻辑（`and`和`&&`等都可以用）、三元。以下仅列出需要注意的运算符

| 运算符   | 名称       | 说明                                                    |
| -------- | ---------- | ------------------------------------------------------- |
| `==`     | 等于       | 值相等。不同类型比较会自动类型转换，如`5=='5'`为真      |
| `===`    | 绝对等于   | 值和类型都相等                                          |
| `!=, <>` | 不等于     |                                                         |
| `!==`    | 不绝对等于 |                                                         |
| `.`      | 并置       | 连接两个字符串，如`"Hello" . "World"`等于`"HelloWorld"` |

## 超级全局变量

超级全局变量（Superglobals）是系统预定义的变量，在所有作用域中都可访问。若未额外说明，它们都是关联数组

| 变量名      | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| `$GLOBALS`  | 全局变量。比如`$GLOBALS['x'] = 1`相当于在函数外写`$x = 1`。无需多言，应该尽量避免使用它 |
| `$_SERVER`  | 服务器信息、当前脚本信息以及当前请求的信息                   |
| `$_POST`    | 请求的POST参数                                               |
| `$_GET`     | 请求的GET参数                                                |
| `$_COOKIE`  | 请求中发送的cookie                                           |
| `$_REQUEST` | 包括了`$_POST, $_GET, $_COOKIE`的内容                        |

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

# 类

```php
# 定义类
class Site {
    # 成员变量
    public $url;
    # 成员函数
    function __construct($url, $title) {  # 构造函数
        this->url = $url;
    }
    function __destruct() {} # 析构函数
    protected function set_url($par) {
        $this->url = $par;
    }
}

# 实例化
$taobao = new Site("taobao.com");
```

# 控制流

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
foreach ($cars as $car) { # 迭代数组元素
    echo $cars[$x] . "<br />";
}
$age = array("Peter"=>"43", "Brian"=>"7");
foreach ($age as $key=>$value) { # 迭代字典元素
    echo $key . ' ' . $value;
}
```

# 函数

```php
# 定义函数
function print_name($name) {
    echo "My name is " . $name;
}

print_name();         # 调用函数
func = "print_name";  # 变量函数，即函数指针
func();
```

# 连接MySQL

常用的有MySQLi和PDO两套接口。其中MySQLi插件针对MySQL设计，支持异步查询等MySQL特有的功能；PDO支持多种数据库。一般项目推荐使用PDO，只用MySQL、且需要做数据库性能优化的项目使用MySQLi

## MySQLi

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

## PDO

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

