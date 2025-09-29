# 简介

Java是严格的面向对象语言——除了基本类型之外，一切皆对象，所有代码都放在类中，哪怕是main函数也要写成类的静态方法

Java是编译型语言，但也具有部分解释型语言的特性。Java源代码写在`.java`文件中；源代码经过`javac`编译器编译为字节码写入`.class`文件（如后缀所暗示的，每个文件装一个类，文件名和类名必须相同），编译过程包括了严格的语法检查和静态类型校验；Java虚拟机JVM加载字节码，并翻译为机器码执行（较新版本会将频繁执行的代码编译为机器码，其他代码动态解释为机器码）

```java
public class HelloWorld {
    public static void main(String[] args) {  // main方法，程序执行入口
        System.out.println("Hello World");
    }
}
```

编译运行过程如下：

```shell
javac Main.java   # 编译为字节码
java Main         # 用JVM运行

# 打包
jar -cvf Main.jar Main.class
java -jar Main.jar
```

# 基础语法

## 流程控制

和C基本相同。比C多一个数组的for循环

```java
int [] numbers = {0, 1, 2, 3};
for (int x: numbers) {
    System.out.print(x);
    System.out.print(", ");
}
```

# 数据类型

Java的数据类型分两类：

- 基本类型：`byte`，`short`，`int`，`long`，`boolean`，`float`，`double`，`char`
- 引用类型：`class`，`interface`等

## 数值

整数有`byte, short, int, long`四种，浮点数有`float, double`两种。此外还有布尔值`bool`因为篇幅较少，并入这一节

```java
// 整数
byte b = 97;
short s = 32767;
int i = 0;
long lng = 1L;
// 浮点数
float f = 3.2f;
double d = 3.2D;
```

彼此兼容的变量进行赋值时，进行隐式类型转换，变成精度较高的那个；无法自动转换时可以强制类型转换

```java
i = s + 1;   // short隐式转换为int
i = (int)d;  // 将double强制转换为int
```

## 包装类

Java为基本数据类型`int`，`double`等提供了`Integer`，`Double`等包装，基本类和包装类之间可以自动转换，称作Auto Boxing和Auto Unboxing

```java
int i = 100;
Integer n = i;  // Auto Boxing

n.equals(i);    // 包装类的比较
```

包装类提供了大量方法，并支持泛型编程。但其执行效率更低，尽量不要用

## 字符和字符串

Java用单引号表示字符，双引号表示字符串。字符可以隐式转换为整数

```java
// 字符
char c = 'a';
int i = c + 1;

// 字符串
String s = "Hello";
```

[字符串方法](https://www.runoob.com/java/java-string.html)

## 数组

```java
int[] arr1 = new int[10];  // 定义长度为10的空数组
int[] arr2 = {1, 2, 3};    // 定义并初始化
int[][] arr2d = new int[3][3];  // 二维数组
```

数组（Array）过于原始了，大多数场景使用列表（List）更方便

# 类和对象

## 基础

```java
public class BankAccount {

    // 类变量，所有实例共享此变量
    private static int totalAccounts = 0;

    // 实例的成员变量，每个实例独有
    private String accountHolder;
    private double balance;
    private final String accountNumber;  // final变量，不能重新赋值
    
    // 构造方法。名字和类名相同，没有返回值，创建对象时自动调用
    public BankAccount(String accountHolder) {
        this.accountNumber = "ACC" + (++totalAccounts);
        this.accountHolder = accountHolder;
        this.balance = 0.0;  // 属性和参数重名时用this加以区分。没重名的时候不需要写this
    }

    // 实例方法
    public void deposit(double amount) {
        balance += amount;
    }
    public void withdraw(double amount) {
        if (amount > balance) {
            System.out.println("余额不足");
            return;
        }
        balance -= amount;
    }

    // getter方法，用于访问私有属性
    public String getAccountHolder() {
        return accountHolder;
    }
    public double getBalance() {
        return balance;
    }

    // 重写（Override）父类方法。注意和重载（Overload）不同
    // 重写覆盖父类方法，重载则是两个方法同时存在，根据实参类型选择调用
    @Override
    public String toString() {
        return String.format("账户[%s] 户主: %s 余额: %.2f",
            accountNumber, accountHolder, balance);
    }
    
    // main方法，代码运行的入口
    public static void main(String[] args) {
        BankAccount account = new BankAccount("张三");
        account.deposit(500);
        account.withdraw(200);
        account.withdraw(2000);  // 测试余额不足
        System.out.println(account);  // 调用toString()
    }
}
```

## 抽象类

多个类有通用功能时，可以把通用部分“提取”出来构成抽象类，通过继承抽象类复用通用的成员变量、成员方法

```java
abstract class Vehicle {
    protected String name;
    // 具体方法，所有子类共用
    public Vehicle(String name) {
        this.name = name;
    }
    // 抽象方法：只有方法签名，没有方法体。子类必须自己实现
    public abstract void move();
}
```

抽象类不可实例化。须**继承**抽象类，并实现其中所有抽象方法，才能得到一个可以实例化的类

```java
class Truck extends Vehicle {
    public Truck(String name) {
        super(name);
    }
    @Override
    public void move() {
        System.out.println(name + " 正在沿公路运输货物...");
    }
}

```

## 接口

接口是比抽象类更高一层的抽象。抽象类包含了类的属性和方法，它说明了具体类“是什么”；接口则只是规定类实现特定的方法，规范了具体类“能做什么”

接口中定义方法签名。其中方法都是`public absctract`，且只能是`public absctract`

```java
public interface Movable {
    void move();
}
```

不同于抽象类，接口不被继承，而是由具体类**实现**。一个类可以实现多个接口

```java
public class Truck implements Movable {
    private String name;

    public Truck(String name) {
        this.name = name;
    }

    @Override
    public void move() {
        System.out.println(name + " 正在沿公路运输货物...");
    }
}

```

# IO

## 控制台IO

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("请输入数字：");
        int num = scanner.nextInt();   // 其他读取方法还有nextLine，nextDouble等
        System.out.println("输入的数字是" + num);
    }
}
```



## 字节流

`java.io.InputStream, OutputStream`的各种子类提供了读写字节流的功能。以文件读写的`FileInputStream, FileOutputStream`为例：

```java
buffer = new byte[1000];

// 读
try (InputStream input = new FileInputStream("readme.txt")) {
    input.read(buffer);
}
// 写
try (OutputStream output = new FileOutputStream("out/readme.txt")) {
    output.write(buffer);
}
```

注意，文件读写都有可能抛出`IOException`

## 字符流

`java.io.Reader, Writer`的各种子类提供了读写字符流的功能。以文件读写的`FileReader, FileWriter`为例：

```java
char[] buffer = new char[1000];

// 读
try (Reader reader = new FileReader("readme.txt", StandardCharsets.UTF_8)) {
    reader.read(buffer);
}
// 写
try(Writer writer = new FileWriter("out/readme.txt")) {
    writer.write(buffer);
}
```

## 文件对象

```java
import java.io.File;

public class Main() {
    public static void main(string[] args) {
        // 文件 / 目录对象
        File f = new File('~/myDir');
        // 方法
        f.getPath();
        f.isFile();
        f.list();
    }
}
```

# 异常处理

使用`try-catch`语句处理异常，用`throw`语句抛出异常

```java
try {
    int[] a = {1, 2};
    a[3] = 3;
} catch (java.lang.ArrayIndexOutOfBoundsException e) {
    e.printStackTrace();
    throw new java.lang.RuntimeException("Exception")
}
```

可以用`throws`关键字指定方法**可能抛出**的异常，交给调用者处理。编译时会检查可能抛出的异常，若没有得到处理就通不过编译。一种取巧的做法是在main后面声明`throws Exception`从而通过编译

```java
import java.util.Arrays;

public class Main {
    // throws关键词说明此方法可能抛出UnsupportedEncodingException
    static byte[] toGBK(String s) throws java.io.UnsupportedEncodingException {
        return s.getBytes("GBK");
    }
    // main可以抛出任何异常。可以通过编译，但遇到异常程序直接崩溃
    public static void main(String[] args) throws Exception {
        byte[] bs = toGBK("中文");
        System.out.println(Arrays.toString(bs));
    }
}
```

# Web编程

```java
import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.util.*;

public class SimpleHttpServer {
    public static void main(String[] args) throws IOException {
        // 创建服务器，监听 8080 端口
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        // 注册处理器
        server.createContext("/", new IndexHandler());
        // 启动服务
        server.setExecutor(null); // 使用默认线程池
        server.start();
        System.out.println("服务器已启动，访问：http://localhost:8080/");
    }

    static class IndexHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            // 构造响应体
            String response = "<h1>Hello, World</h1>";
            // 设置响应头和内容类型
            exchange.getResponseHeaders().add("Content-Type", "text/html; charset=UTF-8");
            exchange.sendResponseHeaders(200, response.getBytes(StandardCharsets.UTF_8).length);
            // 设置响应体
            try (OutputStream os = exchange.getResponseBody()) {
                os.write(response.getBytes(StandardCharsets.UTF_8));
            }
        }
    }
}
```

