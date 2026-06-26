# 数据类型

## 字符串

```python
# 定义
s1 = 'this is a string'
s2 = "this is also a string"
r = r'\string without escape character'
b = b'this is bytes, not string'

s1 + s2   # 字符串拼接
s1 == s2  # 比较是否相等

# 格式化字符串
pi = 3.1415926
f'pi = {pi:.2f}'
```

方法：

| method  | description      |
| ------- | ---------------- |
| title   | 首字母大写       |
| upper   | 大写             |
| lower   | 小写             |
| rstrip  | 去除结束空白     |
| lstrip  | 去除开头空白     |
| strip   | 去除两侧空白     |
| split   | 按照指定序列分割 |
| encode  | 编码             |
| replace | 文本替换         |

对字符串的函数：

| function | description            |
| -------- | ---------------------- |
| ord      | 获取字符的整数表示     |
| chr      | 把编码转换为对应的字符 |

## 列表

```python
# 定义
chars = ['a', 'b', 'c', 'd', 'e']
nums = list(range(20))
squares = [x**2 for x in range(16) if x % 2 == 0] # list comprehension / 列表解析 / 列表推导

# 索引
a = chars[0]
middle = nums[5:15:-1]   # 切片（slicing），[start, stop, step]，它会复制列表内容
even_slice = slice(None, None, 2)
start, stop, step = s.start, s.stop, s.step
even = nums[even_slice]  # 用Slice实例进行切片

# 列表的方法
nums.append(21)       # 在末尾插入元素
nums.insert(0, -1)    # 指定位置插入元素
nums.extend([22, 23]) # 末尾插入多个元素
nums.index(3)         # 寻找指定元素的索引
nums.remove(0)        # 删除指定位置的元素
nums.push(nums.pop()) # 入栈、出栈
nums.sort()           # 排序
```

## 元组

类似列表，不过使用圆括号`()`，且不能改变存储的值。只有一个元素的tuple要写成`(elecment1 , )`以和普通的括号区分

## 字典

```python
# 定义
d1 = {'a':1, 'b':2}
d2 = {str(i):i**2 for i in range(0, 10)}

# 访问
d1['a'] += 1
d1.pop('2')  # 删除
d1.get('2', default=None)        # 返回这个键对应的值；如果没找到这个键会返回None
d1.setdefault('x', default='24') # 如果没有这个键就设置d1['x'] = 24

# 遍历
for key, value in d1.items():  # d1.items遍历键值对。也可以用keys遍历键，values遍历值
    pass

# 判断key在不在字典中
'c' in d1
```

## 集合

无序的不重复元素序列

```python
# 定义集合
s1 = set([1, 2, 3])   # 参数是任意iterable
s2 = {'a', 'b', 'c'}  # 空集合不能用大括号定义，否则会初始成dict
s3 = {x for x in 'this is a set' if x not in 'abc'}

# 集合运算
s1 & s2    # 交集。也可用set.insertion
s1 | s2    # 并集。也可用set.union
s1 - s2    # 差集。也可用set.difference
s1 ^ s2    # 异或，即并集 - 交集。也可用set.symmetric_difference
s1.issubset(s2)   # 判断s1是不是s2子集
s1.issuperset(s2) # 判断s1是不是s2父集

# 添加/删除元素
s1.add(4)      # 添加一个元素
s2.update(s1)  # 添加多个元素
s2.remove('a') # 移除一个元素
s3.discard(1)  # 移除一个元素，并且尝试移除不存在的元素时不报错
s3.clear()     # 清空集合
```

## 字节

```python
# 定义字节
bytes(3)   # 长度为3的空字节
b'abc'

# 其他对象转为字节
'abc'.encode('utf-8')
int.to_bytes(0x616263)
bytes.fromhex('616263')

# 字节转其他对象
b'abc'.decode('ascii')
int.from_bytes(b'abc')
b'abc'.hex()
```

# 控制流

```python
# for 循环
for char in "Hello, World":
    print(char, end='')

# while 循环
in_str = ""
while in_str != "答案":
    in_str = input("请输入答案：")

# if 分支
# 例子中用海象运算符（walrus operator）在判断的同时给变量赋值
if match1 := pattern1.match(data):
    return match1
elif match2 := pattern2.match(data):
    return match2
else:
    return None

# 单行条件语句
b = a if a > 0 else 0
```

# 函数

## 基础

```python
def increment(n: int, reverse: bool = False) -> int:
    """返回n+1。若reverse=True，返回n-1"""
    return n + 1 if not reverse else n - 1

# 匿名函数。它只能有一个表达式
square = lambda x: x**2
```

例子`increment`函数中的`n: int`和`reverse: bool`提示参数应该是什么类型，形参列表后的`-> int`提示这个函数会返回什么类型。它们是函数注解（Annotation）。函数第一行的字符串称作文档字符串（Docstring），用于说明函数作用

函数注解和文档字符串对函数运行没有影响，但用`help(函数)`可以查看它们，并且代码编辑器也可以根据它们进行提示。写好注解、文档字符串能大大提高写代码效率



- `*args`：任意参数列表（Arbitrary Argument List），调用时可以传入任意个位置参数，存入`args`元组中
- `**kwargs`：官方文档中没有给名字，或许该叫任意参数字典，调用时传入任意个关键字参数，存入`kw`字典中。注意如果前面有过的关键字不能再当作kw的关键字，可以把前面的关键字参数写成仅限位置参数来避免冲突

## 闭包

闭包（Closure）是引用了自由对象的函数，被引用的对象将和函数一同存在

```python
def cmp(x, y):
    return lambda: True if x==y else False

def cmp_closure(arg):
    return lambda: True if arg[0]==arg[1] else False

arg = [1, 2]
func = cmp(*arg)
# func里面的x, y是固定对象int，外面的arg改变不影响它们
# 没有引用外部变量，不是闭包
clos = cmp_closure(arg)
# clos里面引用的arg和外面的指向同一个对象，因此是闭包
# 外面对arg的修改会反映到clos的结果
# 闭包把arg的生存期增加到至少和闭包生存期一样长
func()   # False
clos()   # False

arg[1] = 1
func()   # 仍然为False
clos()   # True
```

另外给一个不是闭包的例子

```python
x, y = 1, 2
cmp = lambda: True if x==y else False

x, y = 1, 1
cmp()       # True

del x, y
cmp()       # NameError
```

cmp中引用的x和y不是自由对象，而是非局域变量，如果只需要x和y当前的值，当x和y改变了就会出错误

可以用默认参数的方式改正，因为默认参数在函数定义时被计算，此后不再改变

```python
x = 2
x_times = lambda a: a*x
x_times_fixed = lambda a, y=x: a*y

x = 3
x_times(2)         # x*2 = 6
x_times_fixed(2)   # 2*2 = 4
```

## 装饰器

### 简单的装饰器

装饰器（Decorator）是一种特殊的函数，它接受一个函数作为参数，并返回一个函数，它可以用来扩展函数功能。注意，本节展示的装饰器仅用于说明原理，实用写法应参考下一节

```python
# 定义装饰器
def log_decorator(func):
    def decorated(*args, **kw):
        print(f'calling {func.__name__}')
        return func(*args, **kw)
    return decorated

# 使用装饰器
@log_decorator
def f():
    return 0
```

### 保留函数元信息的装饰器

用上一节的方式使用装饰器，函数`f`被“包裹”了一层，看不到函数的元信息（形参列表、注解、文档字符串等）。应使用`functools.wraps`进行装饰

```python
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def decorated(*args, **kw):
        print(f'call {func.__name__}')
        return func(*args, **kw)
    return decorated

@log_decorator
def f():
    return 0

help(f)    # 看到的是f的信息
```

# 类

## 定义与使用

```python
class Example(object):

    class_attr = 1   # 定义类属性

    def __init__(self, attr_):  # 初始化的魔术方法，创建实例时调用
        self.a = attr_  # 实例属性
        self._a = 1     # 私有变量惯例用一个下划线开头（并不会阻止从外部访问它，仅作为提示）
        self.__a = 1    # 两个下划线开头，解释器解释时会把它变成别的名字，外部不能直接访问
            # 其实还是可以通过__dict__属性等方式访问，python中没有真正的私有变量
            # 主要是为了继承时不覆盖掉父类的属性。仅当涉及子类、并且需要对子类隐藏属性时有必要使用

    def method(self, *args, **kw):   # 定义类方法
        print(self.attr)
        # 第一个变量self是特殊的变量，指代该实例自身，原则上名字可以是任意的，习惯上都用self
        # 调用函数时会自动传入实例自身作为self的实参

ex = Example(1)   # 定义类的实例
ex.a              # 引用类属性
ex.method()       # 引用类方法
```



## 子类(subclass)与继承

子类继承了父类的全部方法，在子类中定义与父类重名的方法将会覆盖掉父类方法

```python
class Child(Parent):
    def __init__(self, arg):
        super(Child, self).__init__(arg)
        # 用super()引用被覆盖掉的父类(super class)的方法
```

**多重继承**
`class Dog(Animal, MammalMixIn)`
常采用MixIn的方法，使类的继承具有一个主线+附加功能

**继承内建类**

```python
class myint(int):
    def __new__(cls, value, payload):
        x = int.__new__(cls, value)
        x.payload = payload
        return x

i = myint(5, 'payload')
```

## 静态方法与类方法

```python
class Book(object):
    @staticmethod
    def foo():
        return 0

    @classmethod
    def bar(cls):
        return 0

b = Book()
```

静态方法就是与其他类属性、实例属性都没有关系的方法，通过装饰器`@staticmethod`定义，定义时不需要`self`，调用时可以用`b.foo()`也可以用`B.foo`，没有参数被自动传进去

类方法是仅与类属性有关、与实例属性无关的方法，通过装饰器`@classmethod`定义。调用时，类自动被作为第一个参数传入

## 通过字符串操纵对象

| name      | usage            |
| --------- | ---------------- |
| `hasattr` | 判断有没有某属性 |
| `getattr` | 获得属性         |
| `setattr` | 设置属性         |

## 魔术方法

1. **构造和析构**：
   1. `__init__`：创建并初始化实例
   2. `__new__`：创建但是不初始化实例。如果同时定义了`__init__`和`__new__`，只会运行`__new__`。主要用在各种魔术，比如继承内建类（子类与继承一节）、实例化为其他类（杂项的未分类魔术）
   3. `__del__`析构方法，定义垃圾回收时的行为（注意：它不实现`del obj`，而是垃圾清除时的额外工作）
2. **字符串显示**：`__str__` ，`__repr__`，`__format__`，对象的字符串输出和格式化，当用`str, repr, format`函数作用于对象时执行
3. **上下文管理**：`__enter__`，`__exit__`，进入和退出with语句时分别执行
4. **比较**：
   1. `__cmp__(self, other) -> Union[int, float]`：所有的比较，当返回值大于0时`self > other`，等于0时相等，小于0时小于
   2. `__eq__(self, other) -> bool, __ne__, __lt__, __le__, __gt__, __ge__`：等于，不等于，小于，小于等于，大于，大于等于。或者也可以用`functools.total_orderging`装饰整个类，然后只需要定义eq和lt/gt就会自动产生完全比较
5. **一元操作符**：
   1. `__pos__(self), __neg__`：正负
   2. `__abs__(self)`：`abs()`函数
6. **算数、逻辑与移位**：
   1. `__add__(self, right_op: Any) -> Any, __sub__, __mul__, __floordiv__, __truediv__`：加减乘除（除法分地板除与真除，前者对应`//`，后者对应`/`。python2没有真除法，用`__div__`表示传统除法；python3没有传统除法）
   2. `__mod__`：取模，`%`
   3. `__pow__`：指数，`**`
   4. `__rshift__, __lshift__`：移位，`>>`和`<<`
   5. `__and__, __or__, __xor__`：位运算，`&, |, ^`
   6. `__radd__(self, left_op: Any) -> Any`：self做右操作数的运算，其他运算同理
   7. `__iadd__(self, inc) -> Any`：增量赋值，比如`obj += 1`会被解释为`obj = obj.__iadd__(1)`，其他运算同理
7. **类型转换**：`__int__(self) -> int, __float__, __complex__, __bool__`
8. **属性访问**
   1. `__getattr__(self, name: str)`：试图获取不存在的属性
   2. `__getattribute__(self, name)`：获取属性的值
   3. `__setattr__(self, name, value)`：属性赋值
9. **容器**：
   1. `__len__(self) ->int`：`len(obj)`，容器长度
   2. `__getitem__(self, key)`：`obj[key]`，注意slice的处理
   3. `__setitem__(self, key, value)`：`obj[key] = value`
   4. `__delitem__(self, key)`：`del obj[key]`
   5. `__reversed__(self)`：`reversed(obj)`
   6. `__contains__(self, item)`：`item in obj`
10. **调用**：`__call__(self, [*args])`：`obj(*args)`
11. **迭代**：`__iter__, __next__`，详见迭代器与生成器部分
12. `__slots__`：如果有这个属性，不在slots列表中的属性不允许被添加。定义之后能减小类的内存占用。如果子类没有slots,则父类的slots不起作用；如果有，则子类的限制是两个slots的并集
13. 只读魔术属性：模块名`__module__`、类名`__class__`、类属性的字典`__dict__`（有`__slots__`的类没有此属性），属性、方法名列表`__dir__`

## 描述器

描述器（Descriptor）是一种特殊对象，将类的属性绑定到描述器，则这个属性的获取、设置和删除行为将被描述器的`__get__, __set__, __delete__`方法重载。注意：这个例子只是展示原理，实用的写法参照下一节的property装饰器

```python
import os

class DirectorySize:
    def __get__(self, obj, objtype=None):
        return len(os.listdir(obj.dirname))

class Directory:

    size = DirectorySize()              # Descriptor instance

    def __init__(self, dirname):
        self.dirname = dirname          # Regular instance attribute

b = Directory('./books')
b.size   # 调用__get__方法计算
```

描述器协议如下。其中`obj`是描述器绑定到的对象实例

```python
descr.__get__(self, obj, type=None) -> value
descr.__set__(self, obj, value) -> None
descr.__delete__(self, obj) -> None
```

描述器有很多用处，比如类型检查、动态计算

### property装饰器

property装饰器是最简单的产生描述器的方式

```python
@property
def score(self):
    return self._score

@score.setter
def score(self, value):
    self._score = value

@score.deleter
def score(self):
    raise AttributeError('cannot delete attribute')
```

尝试访问score属性时，实际上会通过这三个函数对`_score`进行操作。效果相当于给类“添加”了一个属性score。property装饰器的是最简洁的描述器写法。当然，可以直接访问`_score`绕开这些函数，不过随便的突破限制不是好事

用途举例：

1. 在setter中做类型检查
2. 不设置setter，成为只读属性（赋值时抛出AttributeError）
3. 动态计算属性（例如，在向量类中只存储直角坐标，长度是在property中计算的）

注意，property的setter, getter和deleter是一个整体，继承时要一起重载，或者用如`@父类.属性名.setter`的装饰器重载

# 模块与包

每个python脚本都可以作为模块（module）被其他脚本导入；若干模块组合起来就构成一个包（package）

## 导入模块与包

最主要的方式是用import语句，也可以用importlib模块等方式进行更复杂的导入。导入模块和包时，从`sys.path`以及脚本所在目录寻找

```python
import module
import module as m
from module import func
from module import func as f
```

## 创建包

在每个文件夹都放一个`__init__.py`文件，就构成了包。导入时`__init__.py`会先被执行，一般用它自动加载子包。子包导入其他子包时可以用**相对路径导入**，例如`from .. import other_sub_pkg`

运行解释器时，带上`-m`参数就可以把运行一个包

```bash
python -m my_pkg  # 将my_pkg/__main__.py作为Package运行
python my_pkg     # 将my_pkg/__main__.py作为脚本运行（其中的相对路径导入会报错）
```

包的标准结构。`my_project`为项目名，`app`为包名。`import`时包名的横杠要替换为下划线，例如包名是`my-pkg`，则需要`import my_pkg`

```
my_project/
├── pyproject.toml
├── src/
│   └── app/
│       ├── __init__.py
│       └── main.py
└── tests/
```

这是当前（2026）的主流标准。pyproject.toml的写法可以参考[Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)。示例：

```toml
[project]
name = "workbench"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "playwright>=1.58.0",
    "requests>=2.34.2",
]

[build-system]
requires = ["setuptools >= 77.0.3"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]
```


# IO

```python
fp = open(file, 'r')
fp.read()
# 其他读取方法：readline, readlines
fp.close()

with open(file, 'w') as fp:
    fp.write(string)
```

python把和文件类似的对象（能打开，能读能写）称作file-like，都用相同的方法处理

# 错误处理与调试

```python
try :
    do_something()
except (KeyError, ValueError) as e:
    # 当运行try语句时遇到错误，运行此处语句
    # 会捕获错误的子类；不写错误类型则捕获任何错误
    print(repr(e))
    raise RuntimeWarning('message')  # 抛出错误
else :
    # 当没有遇到错误时进入这里
    pass
finally :
    # 以上处理完毕后，不管有没有错误，运行finally的语句
    pass
```

# 并发编程

并发编程通常有以下三种方式：

- **多进程**：开辟多个新进程执行任务
  - 优点：进程间相互独立，稳定性高；能跑满CPU
  - 缺点：创建进程的开销大；操作系统支持的进程数有限；进程间通信复杂

- **多线程**：在当前进程下开辟多个线程执行任务。线程之间共享内存。额外性能消耗主要来自在进程间切换，以及多线程锁
  - 优点：异步IO效率

- **协程**：同一个线程内交替执行多个任务。没有额外开销，但也不能利用多核CPU

## 多进程

Unix/Linus系统可采用`os.fork()`，Windows系统下使用`multiprocessing`模块

```python
from multiprocessing import Process, Pool, Queue

def f(x):
    return x ** 2

process = Process(target=f, args=(3.5, ))
process.start()       # 开始子进程
process.join()        # 等待子进程结束
process.terminate()   # 终止进程
```

需要开启多个子进程时可用`multiprocessing.Pool`；进程间通信可用`multiprocessing.Queue`

## 多线程

```python
import threading
from threading import Thread

# Some tasks for multithreading
def task(wait=1):
    from time import sleep
    sleep(wait)
    return 0

# 创建线程
th1 = Thread(target=task, name='wait1', args=(10,))
th2 = Thread(target=task, name='wait2', args=(10,))
# 开始运行
th1.start()
th2.start()
# 查看线程状态
th1.is_alive()         # 是否在运行
threading.enumerate()  # 所有活动的Thread
# 等待线程结束
th1.join()
th2.join()
```

多个线程共享进程内的变量，变量可能被不同线程修改。而且，如果若干个线程几乎同时修改一个变量，有可能造成难以预估的错误。这种情况要使用`threading.Lock`锁住变量，当一个线程锁住变量之后，其他线程将被暂停，等待到这把锁解开为止

ThreadLocal可以帮助参数在不同线程中传递

好像不能直接获得返回值，要手动把结果存到某个容器里（比如OOP，把某个对象的方法设为target，结果存为该对象的属性）

## 协程

通常使用`asyncio`模块配合`async`和`await`关键字实现。使用`async`定义的函数称作协程函数，直接调用它并不会执行函数，而是返回一个协程对象。`await`语句则执行协程对象并等待它完成。注意：`await`语句只能在`async`函数中使用

```python
import asyncio
import requests

async def fetch_quote(page: int) -> bytes:
    # 此函数从网络下载数据，耗时不固定，若网络差可能要等很久
    url = f'https://quotes.toscrape.com/page/{page}/'
    return requests.get(url).text

# 所有协程函数必须在一个async主函数中调用
async def main():
    # 基础使用。调用async函数返回一个协程对象，"await 协程对象"等待执行结果
    text_1 = await fetch_quote(1)

    # 并行运行多个协程
    await asyncio.gather(fetch_quote(2), fetch_quote(3))

    # 使用task对象进行更精细的管理，如取消任务
    task = asyncio.create_task(fetch_quote(1))
    task.cancel()
    try:
        text_4 = await task
    except asyncio.CancelledError:
        print('Cancelled')

# 启动主函数
asyncio.run(main())
```

异步生成器、异步上下文管理器可以用`async for`还有`async with`

```python
async def fetch_many_quotes(max_pages):
    # 异步生成器，返回一个async_generator对象，无法直接迭代
    for page in range(max_pages):
        quote = await fetch_quote(page)
        yield quote

async def main():
    async for quote in fetch_many_quotes(10):
        # 等待异步生成器返回结果
        print(quote)

    async with asyncio.TaskGroup as tg:
        # 等待全部任务结束，然后关闭TaskGroup
        tasks = [tg.create_task(fetch_quote(page)) for page in range(10)]
```

# 杂项

## 内建功能

### 运算符

`+-*/%`加减乘除取余

`**`乘方（甚至可以是小数次方）

`//`整除

### del语句与垃圾回收

`del var`

python中的回收策略以引用计数为主，当一个对象的引用数为0时将其回收（可以用`id`看对象的标识符，`sys.getrefcount`看引用计数）。del语句并不删除对象，而是删除了一个变量名、同时解除了它对对象的引用

### 逻辑

`True, False`, 大于小于等于et cetera判断对象的值（注意nan和任何数判断都是False）。`A is B`判断是否同一个对象（特别的，`A is None`判断是否是None），与或非`and or not`，括号分组

### 其他

```python
# 空值
None

# 解压iterable object
it = [1, 2, 3, 4]
a, b, c, d = it       # 个数必须匹配
first, *middle, last  # *middle匹配多个元素
```

## 内建函数

### 基础

| name  | description                      |
| ----- | -------------------------------- |
| len   | 求长度                           |
| input | 接受输入，输入内容被理解为字符串 |
| type  | 变量类型                         |

### 聚集函数

`min, max, sum, any, all`

### 迭代相关

```python
range(start，end，step)
# 到达end时结束，实际最后一个元素为end前一个，而不是end
for i in range(0, 10, 2):
    print(i)

# 同时迭代多个序列
zip([1, 2, 3], ['a', 'b', 'c'])
    # 获得一个生成器，(1, 'a'), (2, 'b'), (3, 'c')。最短序列结束时，zip也结束
transposed = list(zip(*matrix))  # 矩阵转置

# 过滤元素。只留下函数返回值为True的元素
filter(lambda x: x>0, range(-10, 10))

# map。将函数作用于每一个元素上
map(abs, range(-10, 10))
```

## 变量作用域

每个模块、类、函数都构成作用域。和C不同，if-else，for，try-except等语句不构成作用域。作用域从小到大分别是Local - Enclosing - Global - Built-in，python在引用变量时，先在局部变量表中找，找不到就到嵌套作用域，然后是嵌套的嵌套，不断向上；在定义/修改变量时，只在局部变量中找，找到就修改，找不到就定义一个新变量。因此，内部可以直接*访问*外部变量，但是不能直接*修改*外部变量，除非使用了`nonlocal`和`global`声明

```python
# 声明非局域变量和全局变量
nonlocal a
global MAX_SIZE

# 直接访问作用域内的变量
locals()
globals()
```

## 文档字符串（docstring）

```python
# Google风格的文档字符串
"""Example Google style docstrings

Parameters:
    param1: this is the first param
    param2: this is a second param

Returns:
    This is a description of what is returned

Raises:
    KeyError: raises an exception
"""
```

## 可迭代对象

可迭代对象（Iterable）是能够逐个返回数据元素的对象，列表、字典、字符串等都是可迭代对象。也可以用生成器（Generator）自定义可迭代对象

```python
# 定义
def gen_square():
    # 将return替换为yield，执行到yield时自动生成一个值，下次执行时从上一次的yield处继续
    # 此函数返回值是生成器
    for i in range(100):
        yield i ** 2

# 用类似列表解析方法定义生成器
gen_square2 = (i**2 for i in range(100))

# 使用生成器
total = 0
for sq in gen_square():
    total += sq

# 判断是否可迭代
from collections.abc import Iterable
isinstance(gen_square, Iterable)
```

也可以手动实现Iterable协议、Iterator协议。Iterable对象需要实现`__iter__() -> Iterator`；其返回的Iterator对象要实现`__next__() -> Any|StopIteration`方法，逐个返回元素，并在迭代结束时抛出`StopIteration`

## 其他

实例化为其他类（摘录自pathlib。例子中，`PurePath()`会根据操作系统返回一个`PureWindowsPath`或者`PurePosixPath`实例）

```python
class PurePath(object):
    def __new__(cls, *args):
        if cls is PurePath:
            cls = PureWindowsPath if os.name == 'nt' else PurePosixPath
        return cls._from_parts(args)

    @classmethod
    def _from_parts(cls, args):
        self = object.__new__(cls)
        # 初始化各属性。略
        return self
```

**检测中文**

```python
def is_cjk(char):
    # CJK Unified Ideographs
    # https://www.unicode.org/charts/PDF/U4E00.pdf
    return ord(u'\u4e00') <= ord(char) <= ord(u'\u9fff')
```

其他unicode范围：

- `3040~30FF`平假名和片假名
- `3000~303F`：CJK标点
- `FF00~FFEF`：全角标点、全角英数、半角片假名和半角谚文等
