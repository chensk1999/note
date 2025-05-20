# 简介

Java是严格的面向对象语言——除了基本类型之外，一切皆对象，所有代码都放在类中，哪怕是main函数也要写成类的静态方法

Java是编译型语言，但也具有部分解释型语言的特性。Java源代码写在`.java`文件中；源代码经过`javac`编译器编译为字节码写入`.class`文件（如后缀所暗示的，每个文件装一个类，文件名和类名必须相同），编译过程包括了严格的语法检查和静态类型校验；Java虚拟机JVM加载字节码，并翻译为机器码执行（较新版本会将频繁执行的代码编译为机器码，其他代码动态解释为机器码）

```java
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello World");
    }
}
```

# 语法

## 基础语法

```java
public class BankAccount {

    // 类变量，所有示例共享此变量
    private static int totalAccounts = 0;

    // 实例变量，每个实例独有
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

    // 9. getter方法，用于访问私有属性
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

## 控制流

和C基本相同。比C多一个数组的for循环

```java
int [] numbers = {0, 1, 2, 3};
for (int x: numbers) {
    System.out.print(x);
    System.out.print(", ");
}
```

## 包装类

Java为基本数据类型`int`，`double`等提供了`Integer`，`Double`等包装，前者性能更高，后者支持泛型编程

## 字符和字符串

Java提供了若干种字符和字符串。最常用的是`String`，其他很少用到

```java
// 基本字符类型和字符数组
char c1 = 'a';
char[] s1 = {'a', 'r', 'r', 'a', 'y'};
// 包装过的Character和String类
Character c2 = new Character('a');
String s2 = new String("array");
// 可以自动转换，称自动装箱
Character c3 = 'a';
String s3 = "array";
```

[字符串方法](https://www.runoob.com/java/java-string.html)

## 数组

```java
int[] array;            // 声明
array = new int[10];    // 定义
int[] arr = {1, 2, 3};  // 声明的同时定义并初始化
```

Java提供了数组，不代表开发者必须使用它。数组（Array）过于原始了，绝大多数场景使用列表（List）更方便

# 数据结构

