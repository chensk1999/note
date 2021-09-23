# 数据类型

## 整型

int
占用4字节，取值范围大约在±2.15e8
还有short/long, signed/unsigned之分

十进制：不以0开头
八进制：以0开头
十六进制：以0x或0X开头（字母均不区分大小写）

## 浮点型

| 类型        | 长度   | 表示范围             | 精度        |
| ----------- | ------ | -------------------- | ----------- |
| float       | 4字节  | 1.2e-38 ~ 3.4e38     | 6位有效数字 |
| double      | 8字节  | 2.3e-308 ~ 1.7e308   | 15位        |
| long double | 10字节 | 3.4e-4932 ~ 1.1e4932 | 19位        |

## 字符串

(signed/unsigned) char
char有没有正负号取决于编译器
占用1个字节，表示-128~127或者0~255
‘x'为字符常量，"x"为字符串常量

变量类型
auto	可以省略
register	寄存器变量。存取速度快
static	静态变量。在编译时赋初值，生存期为运行期间
extern	声明外部变量时使用

格式化字符串

| 格式化字符 | 说明                     |
| ---------- | ------------------------ |
| `%d`       | 带符号十进制整数         |
| `%u`       | 不带符号十进制整数       |
| `%o`       | 八进制整数               |
| `%x`       | (%0x) 十六进制整数       |
| `%f`       | 小数形式单精度浮点数     |
| `%lf`      | 小数形式双精度浮点数     |
| `%e`       | 指数形式单、双精度浮点数 |
| `%g`       | 输出%f和%e中较短一个     |
| `%c`       | 单一字符                 |
| `%s`       | 字符串                   |
| `%*`       | 输入数据不予读入         |

可以用`%m.nf`表示保留n位小数（四舍五入），占用m列（含小数点）
如%+d形式可以强制显示正负号，%-[数字]d可以靠左显示（即空列留在右边，%0[数字]d可以补0
数据的字节数可以用sizeof(类型/变量)获得

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

do {语句} while (表达式)

for ( 循环变量初始化 ; 条件判断 ; 循环变量改变 ) 语句
执行顺序为1->( 2->语句->3)
```

## 控制转向语句

1. `break;`：提前结束循环
2. `goto 语句标号;`，其中标号格式为`标识符:`
3. `continue;`

# 数组

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

# 预处理

#define 宏名 宏体
#define 宏名(形参表) 宏体
注：宏展开仅仅是简单的字符替换
为避免出错，所有形参必须加括弧，且所有表达式仅被求值一次，不多不少

#define 标识符 字符序列1
#define 标识符 字符序列2
#undef 标识符
（可以重复定义，重复定义后的代码中展开后定义的一个

条件编译
#ifdef 标识符	(#ifndef 标识符, #if 常量表达式)
#else
#endif

# 指针

1. 常见指针类型

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

2. 指向字符串常量的指针：`char *p="static string";`

3. 空指针`void *p;`
   `void*`型指针不能用`*`运算符。其他类型指针可以自动类型转换赋值给`void*`型，`void*`型必须通过强制类型转换才能赋给其他类型指针
   p+1表示p后面一个字节

# 动态分配内存空间

```c
void *malloc(unsigned);
void free(void *);
// malloc分配失败时返回NULL
```

# 命令行参数

```c
main(int argc, char *argv[]);
// 注：argc = argument count, argv = argument varible
// 在命令行输入 程序名 [参数]
// argv[0]是程序名，argv[i]是参数，argc是参数个数（程序名也被算进去）
```

# 结构体

```c
struct student {
	int num;
	char name[16];
    char sex;
};
struct student s1={20141221, "chen", 'M'), s2;
s2 = s1;    // 注：可整体赋值，不可比较
```




结构变量.成员名
结构体指针->成员名



类型定义符
typedef struct [类型名] {
……
} 新类型名;

typedef int *P	P为int *型变量

## 文件

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





# 常用库函数

（头文件按照字母排序，函数按照使用频率、用途、心情等原则排序）

```c
函数说明部分按照我看得懂为原则。函数原型也是只要不影响理解和使用，不完全依照其原型（如unsigned int 写成int）
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

​```
void srand(unsigned seed)		设置随机种子
int rand(void)			产生0~RAND_MAX的伪随机数

void *malloc(unsigned size)		申请n个字节的内存，返回首地址/NULL（申请失败时）
void free(void)			释放申请的内存
void *calloc(unsigned n, unsigned size)	申请n*size个字节
void *realloc(void *p, unsigned size)	修改分配内存区的大小
//也包含在malloc.h
​```

string.h
	atof()	将字符串数据转换为float型
	atoi()	转换为int型
	atol()	转换为long int型

​```
strlwr()	将大写字符转换为小写
strupr()	将小写字符转换为大写

strcat(char *dest, char *src)		连接，将src连接到dest结尾处
strcpy(char *dest, char *src)		复制，将src复制到dest中
strncpy(char *dest, char *src，int n)	复制n个字符到dest
strcmp(char *s1, char *s2)		比较，返回s1-s2
strlen(char *s)			字符串长度
(src=source, dest=destination)
​```

time.h
	time_t time(time_t *seconds)		自1970/01/01起经过的时间(s)，若*seconds不为NULL则也存储进去。time_t同long
	double difftime(time_t end, time_t begin)	两个时间相差的秒数
```

