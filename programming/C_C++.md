# 基础

## Hello World

```c++
#include <iostream>

int main()
{
    std::cout << "Hello World!" << std::endl;
    return 0;
}
```

## 简介

声明与定义：待补充

# 数据类型

## 简单变量

### 整型

| type        | length              | max value                        |
| ----------- | ------------------- | -------------------------------- |
| `char`      | 8bit                | 127或255（有无符号取决于编译器） |
| `short`     | $\ge$16bit          | 32767                            |
| `int`       | depend on system    | 2.15e9 (32bit)                   |
| `long`      | $\ge$ min(32, int)  | 2.15e9 (32bit)                   |
| `long long` | $\ge$ min(64, long) | 9.22e18 (64bit)                  |

无符号数前缀`unsigned`，不能存储负数，最大值翻倍。当unsigned溢出时，会去到另一头，有符号类型溢出时不保证。通常情况都用int，超过20亿用long long，存储小数字且必须节省内存时使用short和char。数据的字节数可以用`sizeof(类型/变量)`获得

```c++
// 字面值表示
192;        // 十进制
0b11000000; // 二进制
0300;       // 八进制。以0开头
0x3f;       // 十六进制
```

### 浮点数

| 类型          | 长度   | 表示范围             | 精度        |
| ------------- | ------ | -------------------- | ----------- |
| `float`       | 4字节  | 1.2e-38 ~ 3.4e38     | 6位有效数字 |
| `double`      | 8字节  | 2.3e-308 ~ 1.7e308   | 15位        |
| `long double` | 10字节 | 3.4e-4932 ~ 1.1e4932 | 19位        |

## 字符串

`'x'`为字符常量，`"x"`为字符串常量

| 格式化字符 | 说明                     | 备注                                                         |
| ---------- | ------------------------ | ------------------------------------------------------------ |
| `%d`       | 带符号十进制整数         | `%+d`显示正负号；`%-8d`靠左显示占用8列；`%06d`占用6列，不足的补0 |
| `%u`       | 不带符号十进制整数       |                                                              |
| `%o`       | 八进制整数               |                                                              |
| `%x`       | (%0x) 十六进制整数       |                                                              |
| `%f`       | 小数形式单精度浮点数     | 可以用`%m.nf`表示保留n位小数，占用m列                        |
| `%lf`      | 小数形式双精度浮点数     |                                                              |
| `%e`       | 指数形式单、双精度浮点数 |                                                              |
| `%g`       | 输出%f和%e中较短一个     |                                                              |
| `%c`       | 单一字符                 |                                                              |
| `%s`       | 字符串                   |                                                              |
| `%*`       | 输入数据不予读入         |                                                              |

## 复合类型

### 数组

```c
// 定义数组
int arr[5] = {0, 1, 2, 3, 4};
int arr_2D[3, 3] = {{11, 12, 13}, {21, 22, 23}, {31, 32, 33}};

// 引用数组
arr[0];         // 首个元素
arr_2D[0];      // 首行
arr_2D[2, 1];   // 第三行第二列的元素
```

数据之间用逗号隔开，可以用大括号把数据括起来。二维数组的情形，括起来的自动赋给下一行

```c++
const int SIZE = 4;
int iL[SIZE] = {1, 2, 4, 8};
float fL[] = {0.1, 0.2, 0.3};
```

特别地，char类型数组可以用作C风格字符串

```c++
char s[8] = {'e', 'n', 'd', '\0'};
char t[] = "string literal";
//'c'表示它的值，"c"表示字符串所在地址
```

### 结构体（structure）

```c++
// 声明结构体
struct category {
    char name[20];
    float price;
};

// 定义 & 初始化结构体变量
category c1 = {"stuffed bear", 10.5};
cout << "you can have " << c1.name;
cout << "for $" << c1.price << endl;

// 结构体变量成员赋值(memberwise assignment)
category c2 = c1;

// 访问成员
category* c1 = new category;
c->name = "beer";
(*c).price = 3.5;
```

C++中的结构体可以定义成员函数，与类相似。但区别是，struct的成员默认是public，默认public继承

### 共用体（union）

共用体占用空间是其最大成员的长度，在任意时刻只能存储其中一个成员。当数据可能轮流使用多种数据格式时能够节省空间

```c++
union one_for_all{
    int int_val;
    double double_val;
};

one_for_all pail;
pail.int_val = 15;
cout << pail.int_val;     // 15
pail.double_val = 10.5;
cout << pail.double_val;  // 此时输出int_val的值不确定

// 匿名共用体
struct widget{
    char brand[20];
    int type;
    union{
        long id_num;
        char id_char[20];
    };
};
// 嵌套在widget中间的共用体匿名，id_num与id_char成为widget的成员
// 它们占用相同的地址，每刻只有其中一个作为成员
```

### 枚举（enumeration）

```c++
enum weekdays {Mon, Tue, Wed, Thu, Fri, Sat, Sum};
enum {zero, null=0, one, uno=1};
// Mon, null等值成为符号常量，称枚举量(enumerator)
// 不设置值，枚举量的取值为0，1，……；设置的值必须是整数或者枚举量
// 枚举量可以隐式地转化为int
// 可以定义枚举类的变量，它的值只能是枚举量
```

### 指针（pointer）

常见指针类型

| 定义方式          | 数据类型     | 含义                                                |
| ----------------- | ------------ | --------------------------------------------------- |
| `int a[5]`        | `int [5]`    | 一维数组                                            |
| `int a[5][8]`     | `int [5][8]` | 二维数组                                            |
| `int *p`          | `int *`      | 指针                                                |
| `int **p`         | `int **`     | 指向指针的指针                                      |
| `int int (*p)[5]` | `int (*)[5]` | 指向数组的指针（行指针）                            |
| `int *p[5]`       | `int *[5]`   | 指针数组                                            |
| `int* (*p)(int)`  |              | 指向函数的指针，函数接收一个`int`参数，并返回`int*` |
| `int *p(int)`     | `int *(int)` | 返回值为指针的函数                                  |

2. 指向字符串常量的指针：`char *p="static string"`

3. 空指针`void *p`：`void*`型指针不能用`*`运算符。其他类型指针可以自动类型转换赋值给`void*`型，`void*`型必须通过强制类型转换才能赋给其他类型指针。p+1表示p后面一个字节

```c++
// 声明与初始化
int* p, i;    // p为指针，i为整数
p = &i;       // 取地址运算符&
*p = 5;       // 间接寻址运算符*

// 指针与内存管理
int* p = new int;  // 常规定义的变量在栈中，而使用new定义的内存在堆中
delete p;
    // 释放p指向的内存，不删除p，尝试释放一块不是new来的内存后果不确定
    // 释放空指针是安全的，释放栈空间中的地址会引发错误
int* p_arr = new int[10];  // 使用new生成动态数组(dynamic array)
delete [] p;               // new和delete时的方括号必须匹配

// 指针算数(pointer arithmetic)
int* p = new int[10];
p_arr[3] = 3;
cout << *(p_arr+3);  // 3
```

数组和指针的区别：
1.数组值不能改，指针作为变量可以随意更改
2.`sizeof(int*)` = 指针的长度，`sizeof(int[10])` = `10*sizeof(int)`

### 引用（reference）

```c++
int a;
int& b = a;   // int&是指向int的引用，这样定义的b成为a的别名
// 引用变量必须在声明的同时初始化，且关联之后不能更改

// 引用传参
void increment(int &i)
{
    i++;
}

// 使用const的引用传参
void f(const double & a)
{
    std::cout << a;
}
```

使用引用传参时，被调用函数内的变量和进行调用处的变量是同一个对象。它最大的价值在于引用结构和类：相比于按值传递，它不需要复制，可以节省时间和内存；相比于用指针传参，它更加方便。引用传参的实参必须是一个变量，不能是表达式或常量

如果希望参数值不被改变，最好使用const限定词。const参数的值在函数内部不能被修改，否则会报错（一些老的编译器上会出现一些奇怪结果）。如果实参不是左值/需要隐式转换（比如说，常量），会为它创建一个临时变量。有const才会有临时变量，因为没有const时，如果创建了临时变量，可能我以为我改了某个变量而实际上只有临时变量被改了，原变量没动；有const时，无论如何都不能改原变量，所以就没有歧义了

另外，一般约定需要修改的使用`T*`传参，不修改的用`const T&`传参。尽量不要用`const T*`和`T&`

# 控制流

## 条件判断

```c
// 单行if
int a = 1;
if (a == 0) {
    printf("a is 0");
} else if (a == 1) {
    printf("a is 1");
} else {
    printf("a is not 0 or 1");
}

int b = 1;
switch(b + 1) {
	case 1:
        // do something
        break;
    case 2:
        // do something
        break;
	default :
        break;
}
```

## 循环结构

```c
while (condition) {
    // do something
}

int i;
for ( i=0 ; i<16 ; i++ ) {
    // do something
    // 执行顺序为i=0 -> 检查i<16 -> do something -> i++ -> 检查i<16 -> ...
}

```

## 控制转向语句

1. `break;`：提前结束循环
2. `goto 语句标号;`，其中标号格式为`标识符:`。不建议使用
3. `continue;`

# 函数

## 基本知识

```c++
// 函数原型(prototype)，作用是声明函数，并允许编译器进行静态类型检查(static type checking)
int func(int, double);

int main(){
    // 调用函数
    // 调用时给的输入称作实参(argument)，它被赋值给函数内部的形参(parameter)
    // parameter是函数私有的局部变量，函数结束时被释放
    func(0, 1.5);
}

int func(int a, double b){
    // do something
    return 0;
}
```

## 函数重载(overload)

函数的参数列表（类型、数量、顺序，const、引用变量和返回值类型不算）称作函数的特征标(function signature)，C++允许定义名称相同而特征标不同的函数，称作多态/函数重载，调用时会选择匹配的一个来用。如果有多个完全匹配/可以进行隐式转换的，编译器会通过重载解析(overloading resolution)找出最匹配的，如果找不出一个最匹配的，可能会按照某种规则选一个，或者警告ambiguous

## 函数模板(template)

可以使用模板定义一个泛型的函数，调用时可以用任意类型的参数。在编译时，编译器根据实参类型产生合适的不同版本的函数，称为隐式实例化(implicit instantiation)

```c++
// 声明
template <typename T1, typename T2>
void Func(T1, T2, int);

// 显式实例化(explicit instantiation)
template <> void Func(int, int *, int);

// 也可以在调用的时候显式实例化，如
Func<double>(1.3, pt, 1);

// 定义
template <typename T1, template T2>  // or class T, T could be any valid name
void Func(T1 a, T2 b, int n)
{
    // do something
}

// 模板的重载
template <typename T>
void Func(T a[], T b[], int len)
{
    // do something
}

// 具体化(specialization)
// 以结构体job为例的显式具体化例子
template <> void Func<job>(job &j1, job &j2)
{
    // do something
}
```

对同一个函数名，可以有非模板函数、显式具体化模板函数、常规模板以及它们的重载版本，三者优先级递减
隐式实例化、显式实例化和显式具体化统称具体化

### 自动推断类型

c++11新增的特性

```c++
template <class T1, class T2>
auto Func(T1 x, T2 y) -> decltype(x+y)
{
    decltype(x+y) sum;  // decltype(x+y)即x+y的类型
    sum = x + y;
    return sum;
}
```

### 可变参数模板

```c++
// 定义
template <class... T>
void f(T... args);
```

通常会递归定义模板，每次处理一个参数

```c++
// 递归中止。注意递归中止要在前面声明，否则编译可能不通过
template <class Last>
void print(Last last)
{
    std::cout << last << std::endl;
}

// 模板定义
template <class T, class... Rest>
void print(T t, Rest... rest)
{
    std::cout << t;
    print_types(...rest);
}
```

## 内联函数(inline function)

程序运行期间顺序执行指令（储存在内存中的机器指令）。常规函数调用时，先保护寄存器、跳到该函数的地址，执行完毕后再跳回原来的地址、恢复寄存器，需要消耗一点点时间；使用内联函数，则在编译时直接在调用的位置后面加上这个函数的指令，于是运行时就不用跳来跳去了，可以节省一点时间，但代价是每个调用处都要一份机器码的副本，消耗额外内存

效果类似C语言用宏来计算，但是比宏安全得多

只有被调函数执行时间很短、被调用次数很多时才有较高使用价值。习惯上把内联函数直接定义在最开头一行写完。一般只有10行以内能写完的才会写成内联函数

```c++
inline double square(double x){return x*x;}
```

## 默认参数

可以在函数原型中给出默认参数

```c++
int func(i, j=0, k=0);
```

类似python的位置参数，必须是先有无默认值的、再是有默认值的。不同的是，调用的时候必须按位置传参，而且不允许跳过，比如func(1, , 2)是非法的

一般不推荐使用默认参数，因为当同时有默认参数和函数重载时容易混乱

## 匿名函数

```c++
[](int x, int y) -> int {return x + y;}
```

方括号内定义闭包

# 内存模型与名称空间

## 内存模型

1. 堆空间：在函数内定义的自动变量，作用域是所在的代码块，进入代码块时push，离开代码块时pop

2. 栈空间：从new开始存续到delete为止

3. 静态存储空间：函数外定义的变量以及用static定义的变量，整个程序运行过程中存在
4. 线程持续性存储空间：生命周期和所属线程一样长，用thread_local声明

## 名称空间(namespace)

```c++
//定义
namespace name
{
    int a;
    struct foo(int a);
    int zero() {return 0;};
    namespace nested {int a;}   //名称空间嵌套
    using std::cout;            //在名称空间内使用using声明
    using namespace std;        //在名称空间内使用using编译指令
}

namespace name {double x;}      //名称空间是开放的，可随时添加东西
namespace N = name;             //别名
namespace {double time;}        //unnamed namespace，不能被外部调用，可以充当内部变量

//使用
name::nested::a;    //用解析运算符访问名称空间中的标识符
using name::zero;
zero();             //用using声明访问名称空间中指定标识符
using namespace name;
a;                  //用using指令访问名称空间内全部标识符

/*
使用using声明往往比using namespace更加安全，因为使用using声明时，编译器会自动检查有没有冲突的名称，
而使用using指令时编译器不会（往往也难以）检查
*/
```

### 使用名称空间的一些原则

名称空间的最大价值在大型项目的管理，做项目时应该遵守这些规则，而一个文件的简单程序可以随意一点。但如果考虑以后的代码复用，即使是简单的项目，遵循这些原则也有好处

1. 把全局变量都装进名称空间
2. 把函数库装进名称空间
3. 不要用全局的using指令/声明，尤其不要把using放进头文件
4. using声明优于using namespace指令

## 单独编译

C++允许将源代码分散在多个文件中，分别编译后连接起来，其好处是结构清晰管理方便，并且方便代码复用。一种典型的分割方法是：

* 头文件：写结构体声明和函数原型，在需要使用这些的文件头都include头文件，这样，修改函数时只需要修改头文件中的原型。按照惯例，头文件不要包含函数的定义。同时，头文件需要防止重复include

```c++
// 第一种防止重复include的方法
#pragma once // 最开头加上这个宏，就不会被重复include。不在C++标准中，但是现代编译器广泛支持

// 第二种方法：利用一个自选的宏
#ifndef PROJNAME_FOLDERNAME_FILENAME_H_
#define PROJNAME_FOLDERNAME_FILENAME_H_
// 这里放头文件代码
#endif
```

* 结构：函数的代码
* 调用：调用函数的代码

# 类（class）

## 基本知识

* **声明**

```c++
class Stock   //习惯上类的首字母大写
{
public:       //公有成员
    Stock(const std::string& co = "ERROR", long n = 0, double price_ = 0.0);
    ~Stock();
    void acquire(const std::string &co, long n, double price);
    void buy(long num, double price);
    void sell(long num, double price);
    void show() const;   //const表示方法不会修改对象，const对象只能使用const的方法
    double total() const {return total_val;} //内联方法，直接声明的同时定义
private:      //私有成员，编译器只允许从成员函数访问私有成员，属于数据保护封装。可以省略private
    std::string company;
    long number;
    double price;
    double total_val;
};
```

* **定义成员函数**

```c++
void Stock::show() const
{
    //Stock::show是函数限定名(qualified name)，而show是非限定名，只能在类作用域中使用
    std::cout << company << total_val << std::endl;
}
```

* **构造函数**（Constructor）

构造函数负责初始化类。构造函数没有返回值类型，名称与类名相同。没有参数的构造函数称为默认构造函数。当程序里一个构造函数都没有定义时，编译器会提供一个隐式默认构造函数

形参名要避免和成员名相同。常用的方法有

1. 成员变量前缀`m_`（使用这种方法时通常同时也约定全局变量前缀`g_`)
2. 后缀`_`

```c++
Stock::Stock(const std::string & co, long n, double price_)
{
    company = co;
    number = n;
    price = price_;
    total_val = n * price_;
}
```

* **析构函数**（Destructor）

对象过期时自动调用析构函数（过期判定与编译器有关），一般不会主动调用它。常用来delete掉构造函数里面new出来的内存。可以不显式提供析构函数

```c++
Stock::~Stock()
{
}
```

* **定义与使用类**

```c++
Stock stock;   // 试图使用默认构造函数。但是前面没有定义默认构造函数，会出错
Stock mystock("NanoSmart", 20, 12.5);
Stock *ptstock = new Stock("TI", 18, 19.0);
mystock.show();
```

## this指针

this指针指向自身，只能在类的内部使用

```c++
const Stock& Stock::topval(const Stock & s) const
{
    if (s.totalval > totalval) return s;
    else return *this;  //this指向自己，*this就是自己
}
```

## 运算符重载

```c++
//假设重载+运算符实现时间类Time（时分秒）的运算

//类成员的运算符重载（需要加进类声明的public！）
Time Time::operator+(double m) const
{
    Time result;
    //运算
    return result;
}

//非成员重载运算符
Time operator*(double m, const Time & t)
{
    return t * m;
}

/*
重载之后，t * m将会被理解为t1.operator*(m)，m * t将被理解为operator*(m, t)
复合运算时照一般的结合律来，如t1+t2+t3 = t1.operator+(t2+t3) = ...
重载要求至少一个操作数是自定义类型，并且不能改变原本的语法规则（比如不能把双目运算符重载成单目的）
而且不能修改优先级，不能创建运算符，有的运算符不能重载
*/
```

## 友元(friend)

包括友元函数、友元类、友元成员函数，友元有和类成员函数同等的访问权限（即可以访问private成员），声明方式是在类声明中加入

```c++
friend /*声明*/;
```

### 重载`<<`运算符

std::cout是一个ostream对象，ostream已经重载了<<，ostream << 基本类型变量都能得到输出数据流，因此通过重载<<把自定义的类转换成基本类型，就能实现自定义类的输出。又因为一般想把cout作为左操作数，常使用友元函数来重载

```c++
class Time
{
    //略
    friend ostream& operator<<(std::ostream& os, const time& t);
};

ostream& operator<<(std::ostream& os, const time& t)
{
    /*
    注意！这个函数返回了一个引用，这个引用是它引用传参引过来的东西
    如果返回一个局部变量引用，则退出函数后局部变量消失，引用也就无效了
    */
    os << t.hours << ':' << t.minutes;
    return os;
}
```

## 继承

```c++
// 基类
class Animal
{
    void eat();
    void sleep();
};

// 派生类
class Dog: public Animal    // 以public方式继承Animal
{
    void bark();
};
```

各种继承方式对不同成员的继承

- public：公有成员→公有成员，保护成员→保护成员，私有成员→无（可通过基类的公有、保护方法访问）
- protected：公有成员、保护成员→保护成员，私有成员→无
- private：公有成员、保护成员→私有成员，私有成员→无

# 预处理

```c
#define 宏名 宏体
#define 宏名(形参表) 宏体

#define 标识符 字符序列1
#define 标识符 字符序列2
#undef 标识符
// 可以重复定义，重复定义后的代码中展开后定义的一个

// 条件编译
#ifdef 标识符	// 也可以是#ifndef 标识符, #if 常量表达式
#else
#endif
```


注：宏展开仅仅是简单的字符替换。为避免出错，尽量不要用带形参的宏。如果非用不可，所有形参必须加括弧，形参中每个表达式只能求值一次，不多不少

# 异常处理

```c++
#include <exception>    // 包括std::except类
#include <stdexcept>    // 包括其他派生类
```



```c++
try {
    func(a);
    throw 1;
} catch (std::invalid_argument e) {
    cout << e;
} catch (int i) {
    cout << "1";
}
```



# 标准模板库

标准模板库（Standard Template Library，STL）提供了一系列泛型的容器、迭代器、函数对象和算法的模板

## string

* C语言字符串（以`\0`结尾的`char[]`）
  * string.h（C）
  * cstring（C++）
* C++字符串（`std::string`）
  * string（C++ only）

```c++
#include <string>

int main()
{
    // 构造
    std::string s1("This is a string");  // 用const char*构造
    std::string s2;                      // 构造空字符串
    
    // 用非常符合直觉的方式进行string / C string / char运算
    s2 = "assign";
    s2 += "Concatenate";
    s2 = s2 + s1;
    s2[0];
    
    // IO
    std::cin >> s1;
    getline(cin, s2);
    
    // 类型转换
    std::stoi(s1);  // string to int
}
```

## List

双向链表。据说性能在大多数时候不如vector

```c++
#include <iostream>
#include <list>

int main()
{
    using std::list;
    // 定义列表
    list<int> L1;
    // 迭代列表
    list<int>::iterator it;
    for (it=L1.begin() ; it!=L1.end() : it++) {
        cout << *it << std::endl;
    }
    // 首位元素
    L1.front();
    L1.back();
    // 元素个数
    L1.empty();
    L1.size();
    L1.max_size();
    // 插入与删除
    L1.insert(0, 0);
    L1.erase(0);	
    L1.clear();
    // push & pop
    L1.push_back(5);
    L1.pop_back();
    L1.push_front(1);
    L1.pop_front();
}
```

## Vector

```c++
#include <iostream>
#include <vector>

int main() {
    std::vector<int> vec;
    // 迭代
    for (auto i=vec.begin(); i!=vec.end(); i++){
        std::cout << *i << std::endl;
    }
}
```

# C的常用库函数

头文件按照字母排序，函数按照使用频率、用途等原则排序；函数说明部分按照我看得懂为原则。函数原型也是只要不影响理解和使用，不完全依照其原型（如unsigned int 写成int）

```c
math.h
	abs, fabs			整数、浮点数的绝对值
	exp, log, log10		e^x, lnx, lgx
	pow(x, y), sqrt		x^y, 根号x
	sin, cos, tan		三角函数
	asin, acos, atan		反三角函数
	sinh, cosh, tanh		双曲函数
	double floor(double x)	向下取整
	double ceil(double x)	向上取整

stdio.h
	puts()	输出字符串
	gets()	输入字符串

stdlib.h
	int system(const char *string)      执行一个CMD命令
	void exit(int status)               结束程序。参数为0表示正常退出，不为0表示异常

void srand(unsigned seed)		设置随机种子
int rand(void)			产生0~RAND_MAX的伪随机数

void *malloc(unsigned size)		申请n个字节的内存，返回首地址/NULL（申请失败时）
void free(void)			释放申请的内存
void *calloc(unsigned n, unsigned size)	申请n*size个字节
void *realloc(void *p, unsigned size)	修改分配内存区的大小
//也包含在malloc.h

string.h
	atof()	将字符串数据转换为float型
	atoi()	转换为int型
	atol()	转换为long int型

strlwr()	将大写字符转换为小写
strupr()	将小写字符转换为大写

strcat(char *dest, char *src)		连接，将src连接到dest结尾处
strcpy(char *dest, char *src)		复制，将src复制到dest中
strncpy(char *dest, char *src，int n)	复制n个字符到dest
strcmp(char *s1, char *s2)		比较，返回s1-s2
strlen(char *s)			字符串长度
(src=source, dest=destination)

time.h
	time_t time(time_t *seconds)		自1970/01/01起经过的时间(s)，若*seconds不为NULL则也存储进去。time_t同long
	double difftime(time_t end, time_t begin)	两个时间相差的秒数
```

# Stream

`std::cout`其实是一个`std::ostream`类型的全局变量，它的`<<`运算符被重载，所有输送给它的东西被打印到`stdscr`。用户完全可以自定义输入输出流，实现各种特殊行为

## 重定向输出流

http://wordaligned.org/articles/cpp-streambufs

```c++
class Redirector
{
  public:
    // 写入到src的所有内容会被重定向到dst
    Redirector(std::ostream& dst, std::ostream& src): m_src(src), m_srcbuf(dst.rdbuf())
    {
        m_src.rdbuf(dst.rdbuf());
    }
  private:
    std::ostream& m_src;
    std::streambuf* const m_srcbuf;
}
```

## 文件读写

```c++
#include <iostream>
#include <fstream>

int main()
{
    // 读文件
    std::ifstream ifs;
    ifs.open("filename.txt", std::ios::in);
    if (!ifs.is_open()) {
        // 文件打开失败
        std::cerr << "Cannot open file" << std::endl;
    } else {
        char s[100];
        ifs >> s;           // 也可以用ifs.read(s, len)，读写二进制数据时必须用read
        ifs.eof();          // 判断文件是否结束
        ifs.close();
    }

    // 写文件
    std::ofstream ofs("text.txt", std::ios::out);
    ofs << "Write to file" << std::endl;
    ofs.close()
}
```

`ifstream`内部保存了读指针`get position`，`ofstream`内部则有写指针`put position`，修改此指针可改变读写的位置

```c++
std::ifstream ifs("text.txt", std::ios::in);
std::streampos get_pos = ifs.tellg();        // 获取当前指针位置
ifs.seekg(10);                 // 移动指针
ifs.seekg(0, std::ios::end);   // 把指针移动到文件末尾。类似还有ios::beg指向文件头、ios::cur指向当前位置
```

## 文件读写(C)

结构体类型FILE

```c
FILE *fopen(char *filename, char *mode)
	模式	含义		解释	
	r	read		以读方式打开，若未找到文件，打开失败
	w	write		删除源文件内容，以写方式创建新文件
	a	append		写方式打开，文件读写指针指向文件结束处
使用rb, wb, ab可以以二进制方式打开。此时line feed(\n)和SUB(ASCII码26)不会被辨识
打开成功返回指针，失败返回0

int fclose(FILE *stream)		关闭文件。成功返回0，失败返回EOF

int fscanf(FILE *stream, scanf的参数)
int fprintf(FILE *stream, printf的参数)

int fread(void *buffer, int size, int count, FILE *stream)	从stream读取size*count个字节，装到buffer所指位置
int fwrite(void *buffer, int size, int count, FILE *stream)	同上，写入。返回读/写字节数
//备注

char *fgets(char *str, int count, FILE *stream)	读入至多n-1个字节
int fputs(char *str, FILE *stream)		写

int fgetc(FILE *stream)
int fputc(char c, FILE *stream)

void rewind(FILE *stream)
int fseek(FILE *stream, long offset, int origin)	origin的几个宏定义：SEEK_SET, SEEK_END, SEEK_CUR //注意！！long类型有时不能自动类型转换
long ftell(FILE *stream)
```

# 使用gcc+make编译

## 简单源文件的编译&链接

```
g++ -c main.cpp
g++ -c func.cpp
g++ main.o func.o -o release.exe
```

## 源文件与库的链接

```
gcc main.cpp -I "header directory" -L "lib directory" -lname
```

其中使用的库文件命名为libname.a（好像也不一定？有奇怪的模糊匹配规则），name可以替换成任何合法名字

## make

```
mingw32-make -f Makefile
```

最简单的编译命令由三个部分组成：

1. 目标：相当于标识符，通常用目标文件名
2. 依赖项：用于判断目标构建次序、判断目标是否需要重新构建（如果依赖项的时间戳比目标文件的更新，就需要重新构建）。如果.PHONY作为目标，不会进行检查，总会重新构建
3. 指令：构建目标的指令

```makefile
target: prerequisites    # 注意依赖项最好包括头文件
	commands             # 必须一个tab缩进

# 实例：
test.exe: main.cpp func.cpp func.h
	g++ -g -o test.exe main.cpp func.cpp
```

* 模式匹配

```makefile
%.o: %.c
	gcc -c $< -o $@
```

其中的`%.c`匹配了当前目录下的所有.c文件，`%.o`表示目标是同名.o文件

* 变量

虽然叫做变量，但是实际上更类似于宏，因为只是文本替换

```makefile
HELLO = hello, world!
test:
	@echo $(HELLO)
	# 默认会打印每一条指令，开头加@的不打印
```

命令行参数好像也会变成宏（例：`make -f Makefile DEBUG=Y`）

有一系列特殊的变量，如

* Implicit Variables：`$(CC)`为当前编译器
* Automatic Variables
  * `$@`：当前目标
  * `$<, $^`：第一个依赖项，所有依赖项
  * `$*`：匹配符 % 匹配的部分
  * `$(@D), $(@F)`：当前目标的目录名、文件名
  * `$(<D), $(<F)`：第一个依赖项的目录名、文件名

* 判断与循环

```makefile
ifeq ($(CC), gcc)
	commands
else
	commands
endif
```

# 杂项

## 动态分配内存空间（C）

```c
void *malloc(unsigned);
void free(void *);
// malloc分配失败时返回NULL
```

## 命令行参数

```c
main(int argc, char *argv[]);
// 注：argc = argument count, argv = argument varible
// 在命令行输入 程序名 [参数]
// argv[0]是程序名，argv[i]是参数，argc是参数个数（程序名也被算进去）
```

## 类型转换

```c++
int i = 1;
double d = static_cast<double>(i);  // 最安全的一类转换，错误在编译时就能检查出
```

## 输出格式

```c++
#include <iomanip>

std::cout << std::setw(12) << 'abcd';
std::cout << std::setfill('0') << std::setw(8) << i;
    // 相当于%08d
```

## 显示中文

C++一般默认utf-8编码，但命令行经常是GBK编码

运行命令`chcp 65001`