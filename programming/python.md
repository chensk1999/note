# 基本语法

## 循环，条件

```python
for var in it:
    do_something(var)

while condition1:
    do_something()

    if condition2 and condition3:
        break
    elif condition4 or condition5:
        continue
    else:
        pass

# 单行条件语句
a = 1
b = a if a > 0 else 0
```

## 赋值表达式

assignment expression是3.8版本新增特性，有时也叫Named Expressions。其格式是`NAME := expr`，其中的运算符`:=`被非正式地称为海象运算符（walrus operator）

赋值表达式同时实现赋值和表达式的功能。同时，所有能够使用`=`赋值的地方都不允许用`:=`赋值，以防止混乱

赋值表达式是为了让代码更简洁而引入的。千万不要为了使用赋值表达式反而让代码更复杂更难看懂

```python
# 不使用:=
foo = bar()
if foo:
    return foo

# 使用:=
if foo := bar():
    return foo

# 不使用:=
match1 = pattern1.match(data)
if match1:
    return match1
else:
    match2 = pattern2.match(data)
    if match2:
        return match2
    else:
        return None

# 使用:=
if match1 := pattern1.match(data):
    return match1
elif match2 := pattern2.match(data):
    return match2
else:
    return None
```

# 数据类型

## 字符串(string)

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

### 方法

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

### 对字符串的函数

| function | description            |
| -------- | ---------------------- |
| ord      | 获取字符的整数表示     |
| chr      | 把编码转换为对应的字符 |



## 列表(list)

```python
# 定义
L1 = [1, 2, 3]
L2 = list(iterable_obj)
L3 = [x **2 for x in range(1, 11) if x % 2 == 0]
L4 = [m + n for m in 'ABC' for n in 'XYZ']
    # 3、4称作list comprehension，列表解析，列表推导

# indexing
first = L1[0]
last = L1[-1]

# slicing，切片
# 切片会复制列表内容，切片和原本列表不是同一个东西
middle = L1[1:-1]    # [start:stop:step]，注意实际的最后一个元素是stop的前一个
reversed = L1[::-1]  # start, stop缺省则一直到头
s = slice(1, -1)
middle = L1[slice]   # 先创建slice实例，之后直接引用它，合理使用能提高可读性
start, stop, step = s.start, s.stop, s.step
s.indices(len(L1))   # 自动调整长度，截掉超出范围的

# delete
del L1[1]
L1.remove(2)
L1.pop()
```

### 方法

| mothod  | description            |
| ------- | ---------------------- |
| append  | 在末尾添加元素         |
| insert  | 在指定位置插入元素     |
| extend  | 在末尾添加多个元素     |
| remove  | 删除指定位置元素       |
| pop     | 删除指定位置元素并返回 |
| sort    | 排序                   |
| reverse | 反序                   |
| index   | 寻找元素的index        |

### 对列表的函数

```python
# 排序（原列表不变）
L = [('name', 2), ('foo', 3), ('bar', 1)]
s = sorted(L, key=lambda x: x[1], reverse=True )
# key是一个callable，通过它的结果来排序
# 使用collections.itemgetter或operator.attrgetter运行速度更快，而且支持多关键字排序
```

## 元组(tuple)

同列表，不过使用圆括号()，且不能改变存储的值
只有一个元素的tuple要写成`(elecment1 , )`以和普通的括号区分

## 字典(dict)

```python
# 定义
d1 = {'1':1, '2':2}
d2 = {i:i**2 for i in range(0, 10)}

# 访问
d1['1']
d1.get('2')

# 添加，修改
d1['3'] = 3
d1['3'] = 'c'

# 删除
del d1['1']
d1.pop('2')

# 遍历
for key, value in d1.items():
    	pass
# 类似的，有dict.keys()和dict.values()
# 也可以直接for key in dict

# 判断key在不在字典中
'3' in d1
```

### 方法

```python
# 如果原本没有这个键，就设置为default，并返回default
# 否则，返回键对应的值
d = {}
d.setdefault('a', []).append(1)
```

## 集合(set)

无序的不重复元素序列

```python
# 定义集合
s1 = set([1, 2, 3])   # 必须用一个iter
s2 = {'a', 'b', 'c'}  # 空集合不能这样，否则会初始成dict
s3 = {x for x in 'this is a set' if x not in 'abc'}
    # Set comprehension

# 交并补
s1 & s2    # 交集
s1 | s2    # 并集
s1 - s2    # 差集
s1 ^ s2    # 不重复的元素，即并集 - 交集

# 添加/删除元素
s1.add(4)      # 添加一个元素
s2.update(s1)  # 添加多个元素
s2.remove('a') # 移除一个元素
s3.discard(1)  # 移除一个元素，并且尝试移除不存在的元素时不报错
s3.clear()     # 清空集合
```

除了用运算符之外，还可以用方法来进行集合运算

| method               | description  |
| -------------------- | ------------ |
| intersection         | 交集         |
| union                | 并集         |
| difference           | 差集         |
| symmetric_difference | 不重复的元素 |
| issubset             | 判断是否子集 |
| issuperset           | 判断是否超集 |

# 函数(function)

## 函数定义

```python
def func(pos, /, pos_or_kwd, *, kwd):
    pass     # 没有return时返回None

def complicated_func(pos, /, pos_or_kwd, default=None, *args, *, kwd, **awargs):
    return pos, kwd    # 可以一次返回多个值，实际上是返回了一个dict
```

* `pos`：仅限位置参数（Positional-Only Parameters），在`/`之前的都是位置参数，只能按位置调用。斜杠缺省时没有位置形参

* `pos_or_kwd`：位置或关键字参数（Positional-or-Keyword Arguments），可以用位置调用也可以用关键字调用

* `kwd`：仅限关键字参数（Keyword-Only Arguments），在*之后的都是关键字参数，只能用关键字方法调用

* `default`：有参数默认值（Default Argument Value）的参数，调用时可以省略。默认值是**在函数定义过程中计算**的，所以如果用可变对象（如list, dict等）当作默认值，在后续运行中的修改会被保留

```python
temp = list()
def f(a, L=temp):
    L.append(a)
    return L

f(1)    # [1]
f(2)    # [1, 2]
temp    # [1, 2]
```

* `*args`：任意参数列表（Arbitrary Argument List），调用时可以传入任意个位置参数，存入`args`元组中

* `**kwargs`：官方文档中没有给名字，或许该叫任意参数字典，调用时传入任意个关键字参数，存入`kw`字典中。注意如果前面有过的关键字不能再当作kw的关键字，可以把前面的关键字参数写成仅限位置参数来避免冲突


## 函数调用

```python
func(1)      # 位置调用
func(arg=1)  # 关键字调用
```


python的调用，是**通过对象引用调用**，传递的始终是对象

## 注解(annotation)

```python
def add(x:int, y:int=0) -> int:
    return x + y
```

注解不会被类型检查，对运行没有影响，仅作为文档的一部分。注解储存在`func.__annotations__`中，可以通过help查看

## 匿名函数(lambda)

`lambda variable: expression`

以下两种方法定义的函数等价

```python
f1 = lambda x: x*x

def f2(x):
    return x * x
```

lambda只能有一个表达式，不能有循环，分支等结构（可以用单行if，如`lambda x: x if x >= 0 else -x`）

## 闭包(closure)

闭包指引用了自由对象的函数，被引用的对象将和函数一同存在

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



## 装饰器(decorator)

### 简单的装饰器

装饰器是一种特殊的函数，它接受一个函数作为参数，并返回一个函数。常用装饰器包装一个函数来扩展它的功能

```python
# 定义装饰器
def log_decorator(func):
    def docorated(*args, **kw):
        print('call {0}'.format(func.__name__))
        return func(*args, **kw)
    return decorated

# 使用装饰器
@log_decorator
def f():
    return 0
# 这样定义，相当于f = log(f)，函数被log包装为decorated
# 但是f就消失了。f.__name__，形参表等都变成了decorated

help(f)    # 看到的是decorated的帮助
```

### 保留函数元信息的装饰器

使用`functools.wraps`可以保留函数元信息

```python
from functools import wraps

def log_decorator(func):
    @wraps(func)
    def decorated(*args, **kw):
        print('call {0}'.format(func.__name__))
        return func(*args, **kw)
    return decorated

@log_decorator
def f():
    return 0

help(f)    # 看到的是f的信息
```

### 带参数的装饰器

```python
from functools import wraps

def log(logfile):
    def log_decorator(func):
        @wraps(func)
        def decorated(*args, **kw):
            with open(logfile, 'a') as fp:
                fp.write('call {0}'.format(func.__name__))
            return func(*args, **kw)
        return decorated
    return log_decorator

@log('D:\\out.log')
def f():
    return 0
```

### 利用装饰器的强制类型检查

```python
from inspect import signature
from functools import wraps

def typeassert(*ty_args, **ty_kwargs):
    def decorate(func):
        # If in optimized mode, disable type checking
        if not __debug__:
            return func

        # Map function argument names to supplied types
        sig = signature(func)
        bound_types = sig.bind_partial(*ty_args, **ty_kwargs).arguments

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_values = sig.bind(*args, **kwargs)
            # Enforce type assertions across supplied arguments
            for name, value in bound_values.arguments.items():
                if name in bound_types:
                    if not isinstance(value, bound_types[name]):
                        raise TypeError(
                            'Argument {} must be {}'.format(name, bound_types[name])
                            )
            return func(*args, **kwargs)
        return wrapper
    return decorate

@typeassert(int, z=int)
def spam(x, y, z=42):
    print(x, y, z)
```

# 类(class)

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

**继承int**

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

## 魔术属性

`__slots__`：如果有这个属性，不在slots列表中的属性不允许被添加。定义之后能减小类的内存占用。如果子类没有slots,则父类的slots不起作用；如果有，则子类的限制是两个slots的并集

不能改的魔术属性：

```python
__module__   # 模块名
__class__    # 类名
__dict__     # 对象的{属性名:值}字典，但是有__slots__的类没有__dict__
__dir__      # 对象或类的属性、方法名列表
__mro__      # 对象的继承顺序
__doc__      # 对象或函数的描述信息
__file__     # 文件的名字，其包含路径信息。
```

## 描述器（Descriptor）

描述器是一种特殊对象，将类的属性绑定到描述器，则这个属性的获取、设置和删除行为将被描述器的`__get__, __set__, __delete__`方法重载。例如（注意：这个例子只是展示原理，实用的写法参照下一节的property装饰器）：

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

描述器有很多用处，比如

1. 托管属性。依托于其他属性的东西，比如某个列表中的最大值
2. 动态计算。偶尔才会用到的属性写成描述器，可以在需要用到的时候才计算

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

尝试访问score属性时，实际上会通过这三个函数对`_score`进行操作。效果相当于给类“添加”了一个属性score。property装饰器的是最简洁的描述器写法。当然，可以直接访问_score绕开这些函数，不过随便的突破限制不是好事

用途举例：

1. 在setter中做类型检查
2. 不设置setter，成为只读属性（赋值时抛出AttributeError）
3. 动态计算属性（例如，在向量类中只存储直角坐标，长度是在property中计算的）

### property装饰器的继承

```python
class Master(object):
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if type(name) != str:
            raise TypeError
        else:
            self._name = name

class Slave(Master):
    @property
    def name(self):
        # property的setter, getter和deleter是一个整体
        # 这样定义就会把它们全部覆盖掉
        # 在这个例子中，Slave类的name就没有getter了
        return super().name

class Sub(Master):
    @Master.name.getter
    def name(self):
        # 这样写就只会覆盖掉三者之一，不改变另两个
        print('getting name')
        return super().name
```

## 元类(metaclass)

元类创建出类，类创建出实例

# 迭代器与生成器

## 迭代器

iterator是一个具有`__next__`方法的对象，调用此方法能得到下一个迭代值，并且在迭代结束时抛出`StopIteration`

iterable是一个具有`__iter__`方法的对象，并且这个方法要返回一个iterator

使用for循环时，底层会自动获得对应iterator并且重复获取下一个元素，直到`StopIteration`

```python
class Node(object):
    def __init__(self, value):
        self._value = value
        self._children = []

    def add_child(self, node):
        self._children.append(node)

    def __iter__(self):
        return DepthFirstIterator(self)
        # 另外一种做法是__iter__返回self，同时自己实现__next__方法
        # 也可以直接写成生成器，在这里yield，这样最为简洁

    def depth_first(self):
        return DepthFirstIterator(self)


class DepthFirstIterator(object):
    def __init__(self, start_node):
        self._node = start_node
        self._children_iter = None
        self._child_iter = None

    def __next__(self):
        # Return myself if just started; create an iterator for children
        if self._children_iter is None:
            self._children_iter = iter(self._node)
            return self._node
        # If processing a child, return its next item
        elif self._child_iter:
            try:
                nextchild = next(self._child_iter)
                return nextchild
            except StopIteration:
                self._child_iter = None
                return next(self)
        # Advance to the next child and start its iteration
        else:
            self._child_iter = next(self._children_iter).depth_first()
            return next(self)
```

## 生成器

生成器(generator)是一种特殊的迭代器，它简化了定义的方法。定义及使用方法如下

```python
# 定义
gen1 = (i**2 for i in range(0, 2))

def gen2():
    # generator function
    # 将return替换为yield，函数返回的就会是一个生成器
    # 执行到yield时自动生成一个值，下次执行时从上一次的yield处继续
    for i in range(0, 100):
        yield i

class Node(object):
    def __init__(self, value):
        self.value = value
        self.children = []

    def __iter__(self):
        for child in self.children:
            yield child

# 使用
next(gen1)  # 0
next(gen1)  # 1
next(gen1)  # StopIteration

for item in gen2():
    print(item)

n = Node(2)
next(iter(n))
```

## 判断是否可迭代

```python
from collections.abc import Iterable, Iterator, Generator

g = (i**2 for i in [1, 2])
isinstance(g, Iterable)    # True
```

# 模块与包

## 导入模块/包

最主要的方式是用import语句，也可以用importlib模块等方式进行更复杂的导入

```python
import module
import module as m
from module import func
from module import func as f
from module import *    # 不建议使用，可能导致命名空间污染
```

## 构建层级包

在包的每个文件夹都放一个`__init__.py`文件，就构建了分层模块构成的包（没有`__init__`就是命名空间包）。导入时`__init__.py`会先被执行，一般用它自动加载子模块

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

## try-except

```python
try :
    do_something()
except (KeyError, ValueError) as e:
    # 当运行try语句时遇到错误是被捕获，运行此处语句
    # 如果有as 变量，相应的错误报告存进变量里
    # 会捕获错误的子类
    # 不写错误类型则捕获任何错误。这通常是不好的
    print(repr(e))
else :
    # 当没有遇到错误时进入这里
    pass
finally :
    # 以上处理完毕后，不管有没有错误，运行finally的语句
    pass
```

## assert

```python
assert flag == 1, 'print this if True, else raise AssertionError'
```

启动解释器时用-O(大写字母O)关闭assert

## raise

抛出错误。例：

```python
raise ValueError('message')
```

# 并发编程

并发编程通常有以下三种方式：

- **多进程**：用多个进程同时进行任务。每个进程有独立的内存空间。**适合计算密集型任务**
- **多线程**：在一个进程下启动多个线程，线程之间共享内存空间。由于python的全局解释器锁（GIL），不同线程无法同时执行。**适合可以并行执行、且受限于IO的任务**（其实没想明白有什么任务属于这一类）
- **协程**：在一个进程内切换执行任务。**适合需要等待IO的任务**，比如等待用户输入、等待设备响应

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

pool = Pool(5)    # 最多放5个子进程的pool
pool.apply_async       # 向池中添加一个进程
pool.close()           # 关闭池子，同时开始进程
pool.join()            # 等待到所有进程结束

queue = Queue  # 用于子进程之间通信
queue.put
queue.get
```

注意：主进程的全部数据都是通过pickle序列化传入子进程，故很多时候multiprocessing失败是因为pickle失败了

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

python解释器的GIL(Global Interpreter Lock)锁导致多线程无法利用多核，想有效利用必须要多进程

ThreadLocal可以帮助参数在不同线程中传递

好像不能直接获得返回值，要手动把结果存到某个容器里（比如OOP，把某个对象的方法设为target，结果存为该对象的属性）

## 协程

通常使用async和await关键字声明协程。使用`async`定义的函数称作协程函数，直接调用它并不会执行函数，而是返回一个协程对象。`await`语句则执行协程对象并等待它完成。注意：`await`语句只能在`async`函数中使用

```python
import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'world')
    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
```

上述例子中虽然使用了协程，但是两次等待没有并发进行。

# 内建模块

## argparse（命令行参数）

```python
import argparse

# 创建解析器
parser = argparse.ArgumentParser(
    prog='ProgramName',
    description='What the program does',
    epilog='Text at the bottom of help')

# 添加参数
# 添加顺序不影响结果，因此多于一个位置参数时很可能出现不正确的捕获结果
parser.add_argument(
    'a0'                  # 位置参数
    help='initial value'  # 提示信息
    required=True,        # 是否必选参数
    type=float            # 类型转换
)
parser.add_argument(
    '--max_iter', '-m',   # 关键字参数。可以有多个名字
    default=16,           # 默认值
    nargs=1,              # 接收多少个参数，可以是int, ?,, *, +。指定之后传入参数存为列表
)
parser.add_argument(
    '--verbose',
    action='store-true'   # 开关参数。传入这个参数时为真，否则为假
)

# 解析参数
# 假设在命令行输入：file.py 1 -m 20
args = parser.parse_args()
args.a0       # = 1
args.max_iter # =20
```

## code（自定义python解释器）

```python
import code

ic = code.InteractiveConsole()

need_more_input = False
while True:
    if need_more_input:
        need_more_input = ic.push(input('... '))
    else:
        need_more_input = ic.push(input('>>> '))

# 查看InteractiveConsole中的变量
ic.locals['a']
```

## collections（容器）

### 队列

`deque([iterable[, maxlen]]) --> deque object`

在队列两端插入或删除元素时间复杂度都是o(1)，而在列表的开头插入或删除元素的时间复杂度为O(N)

### defaultdict

将字典的值默认初始化为指定类型

```python
from collections import defaultdict

d = defaultdict(list)
d['a'].append(1)

# 其实可以用dict.setdefault实现相同的功能
```

### OrderDict

迭代、序列化时维持插入的顺序。修改不会改变顺序。内部用一个链表保存数据，所以大小是普通dict的两倍

### Counter

```python
from collections import Counter

count = Counter(hashable_iter)
a_count = count['a']         # 查看元素出现次数
top3 = count.most_common(3)  # 返回出现最多的元素和其出现次数
count.update(some_more_elements)   # 增加计数

# 计数求和求差
count2 = Counter(whatever)
count + count2
count - count2  # 好像不会减出负数
```

### 命名元组

```python
from collections import namedtuple

Stock = namedtuple('Stock', ['name', 'shares', 'price'])
s = Stock(name='MHRD', shares=100, price=12.4)
s[1]      # = 100
s.shares  # = 100
s._replace(price=13.2)  # 创建一个新的实例，用新值替代原本的
```

namedtuple性能并不高，需要考虑性能时最好利用类的`__slots__`方法

### 逻辑上合并字典

```python
from collections import ChainMap

a = {'a':1, 'z':1}
b = {'b':2, 'z':2}
chain = ChainMap(a, b)
# chain在逻辑上相当于多个字典的并，对chain进行查找相当于在所有children中进行查找
chain['a']  # = 1
chain['z']  # = 1，有重复键时只对第一个进行操作
```

注意：进行修改和删除时只作用于第一个字典，遍历时重复键也只有第一个。如果不需要保留原本字典，或许用dict.update更好

## configparse（配置文件）

一般建议把配置（比如说登录的端口，etc.）单独放进一个文件而不是硬编码在程序里面，此模块就是专门用来解析config.ini文件的

### 配置文件格式

```ini
[Simple Values]
key=value
spaces in keys=allowed
spaces in values=allowed as well
spaces around the delimiter = obviously
you can also use : to delimit keys from values

[All Values Are Strings]
values like this: 1000000
or this: 3.14159265359
are they treated as numbers? : no
integers, floats and booleans are held as: strings
can use the API to get converted values directly: true

[Multiline Values]
chorus: I'm a lumberjack, and I'm okay
    I sleep all night and I work all day

[No Values]
key_without_value
empty string value here =

[You can use comments]
# like this
; or this

# By default only in an empty line.
# Inline comments can be harmful because they prevent users
# from using the delimiting characters as parts of values.
# That being said, this can be customized.

    [Sections Can Be Indented]
        can_values_be_as_well = True
        does_that_mean_anything_special = False
        purpose = formatting for readability
        multiline_values = are
            handled just fine as
            long as they are indented
            deeper than the first line
            of a value
        # Did  I mention we can indent comments, too?
```

### 使用例

```python
import configparser

config = configparser.ConfigParser()
config.read('example.ini')

# get a list of all sections
config.sections()

# you can treat config as dict
config['Simple Values']['key']

# get int/float/boolean values
# boolean value from 'yes'/'no', 'on'/'off', 'true'/'false' and '1'/'0'
# 可以自定义converter
config['All Values Are Strings'].getint('values like this')
config.getfloat('All Values Are Strings', 'or this')

# edit config
config['DEFAULT'] = {'ServerAliveInterval': '45',
                     'Compression': 'yes',
                     'CompressionLevel': '9'}

# write config file
with open('example.ini', 'w', encoding='utf-8') as fp:
    config.write(fp)
```

## csv（读写CSV文件）

```python
import csv

# 读csv文件
with open('whatever.csv', 'r') as fp:
    reader = csv.reader(fp)
    for line in reader:
        print(reader.line_num, line)   # 字符串列表

# 读取为字典
with open('whatever.csv', 'r') as fp:
    dict_reader = csv.DictReader(fp)
    for line in dict_reader:
        print(line)  # 字典，用第一行内容作为键

# 写csv文件
with open('whatever.csv', 'w', newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow([1, 2, 3])
    rows = [(i, i+1, i**2) for i in range(0, 10)]
    writer.writerows(rows)
```



## datetime（时间）

有两个时间的库：time和datetime，前者更接近操作系统层面，而datetime做了一定的封装，功能更丰富，用起来更容易

```python
from datetime import datetime, timedelta

# 指定时间
some_time = datetime(year=2020, month=2, day=2)
# 当前时间
now = datetime.now()
# 时间偏移量
tomorrow = now + timedelta(days=1)

# 时间戳(float, in seconds)
timestamp = now.timestamp()
now_fromstamp = datetime.fromtimestamp(timestamp)
now_utc = datetime.utcfromtimestamp(timestamp)

# 时间字符串
# %Y, %m, %d, %H, %M, %S 时分秒
# %a, %A  简化/完整星期名称（如：Sun, Sunday）
# %b, %B  简化/完整月份名称（如：Jan, January）
# %c	例：Sun May 20 17:01:14 2018
format_s = '%Y.%m.%d %H:%M:%S'
time_str = now.strftime(format_s)
fromstr = datetime.strptime('2020.02.02', '%Y.%m.%d')
```

## hashlib

包括sha256, sha512等哈希算法

```python
import hashlib
h = hashlib.md5(b'some bytes')
h.update(b"update this hash object's state")
b = h.digest()         #得到bytes类型的hash
x = b.hexdigest()      #得到16进制字符串
```

## heapq

### 最大/最小元素

`nlargest(n, iterable, key=None)`
Find the n largest elements in a dataset. Equivalent to:  sorted(iterable, key=key, reverse=True)[:n]

`nsmallest(n, iterable, key=None)`
Find the n smallest elements in a dataset.

弹出堆的前N个元素，复杂度NlogM，M为堆大小。查找最大/最小，用min/max较快；N比较小时用nlargest/nsmallest较快；N几乎和M一样大时，排序再切片比较快

### 合并排序序列

`from heapq import merge`

## http.server - http服务器

```shell
# 打开简单的文件服务器。可以用127.0.0.1:8000访问
# 注意：性能和安全性都不好，建议只在内网给可信用户提供服务
# 若有更高需求，可以考虑使用Flask或Django
python -m http.server 8000 --directory "/folder"
```

如果这个简单的服务器不能满足需求，可以进行二次开发。`http.server`使用handler类处理客户端发来的请求，可以继承已有handler类实现更多功能

```python
import http.server
from http import HTTPStatus
import os
import re

class PartialContentHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # do_GET函数用于处理GET请求。当收到GET请求时调用此函数，请求参数是self.headers、self.path等
        # 这个例子中，解析请求头的Range参数，设置响应头的Content-Range等参数，并发送数据给客户端
        range_header = self.header.get('Range')
        if (range_header is None) or (not self.path.endswith('.mp4')):
            super().do_GET(self)  # 只处理MP4文件的范围请求，其余情况用父类处理

        # 计算文件大小、起止位置
        path = self.translate_path(self.path)
        fsize = os.path.getsize(path)
        try:
            start = int(re.match(r'bytes=(\d+)-\d*', range_header)[1])
        except:
            start = 0
        end = fsize - 1

        # 发送响应
        self.send_response(HTTPStatus.PARTIAL_CONTENT)
        self.send_header('Content-type', 'video/mp4')
        self.send_header('Content-Range', f'bytes {start}-{end}/{fsize}')
        self.send_header('Accept-Ranges', 'bytes')
        self.end_headers()
        f = open(path, 'rb')
        f.seek(start)
        return f

if __name__ == '__main__':
    import socket
    ip_addr = socket.gethostbyname(socket.gethostname())

    # 启动服务器
    server_address = (ip_addr, PORT)
    httpd = http.server.HTTPServer(server_address, PartialContentHandler)
    print(f'Serving HTTP on {ip_addr}:{PORT}')
    httpd.serve_forever()
```

## html

```python
from html.parser import HTMLParser

class MyParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print('start tag: ', tag, attrs)
    def handle_endtag(self, tag):
        print('end tag: ', tag)

    # 其他还有handle_startendtag(tag, attrs), handle_data(data)
    # handle_comment(data)， handle_entityref(name), handle_charref(name)等

parser = MyParser()
parser.feed('example.html')
# feed之后立即分析整个文档，每当遇到相应元素时，就会调用对应handle函数
```

## itertools（迭代器工具）

### 分组

```python
from itertools import gropby

# 按照指定字段分类
# L是list，其中元素都是dict，都包含键'date'
# 先对按照指定的字段L排序
# 返回一个groupby object（类似生成器），每次迭代返回值和对应组的生成器
g = groupby(L, key=itemgetter('date'))
```

### 迭代器切片

```python
from itertools import islice

gen = (i**2 for i in range(0, 100))
iter_slice = islice(gen, 10, 20)
# 返回一个islice object，它也是iterator
# 注意islice会消耗迭代器中的数据
```

### 丢弃开始元素

丢弃一个迭代器在key第一次返回False之前的元素

```python
from itertools import dropwhile

# 例：丢弃最开始的空行
with open('foo.txt') as fp:
    for line in dropwhile(lambda s: s=='', fp.readlines()):
    print(line)
```

### 排列组合

`permutations, combinations`

### 迭代多个序列

```python
from itertools import chain

a = [1, 2, 3]
b = [3, 2, 4]
c = chain(a, b)
sum(c)
```

## json（读写JSON文件）

```python
import json

# 读写文件
obj = json.load(fp)
json.dump(obj, fp, ensure_ascii=False, indent=2)  # ensure_ascii不是通用转换方式，建议设为False

# json字符串
json_str = json.dumps(obj)
obj = json.loads(json_str)

# 类型转换
json_str = json.dumps(obj, default=lambda obj: obj.__dict__)
obj = json.loads(json_str, object_hook=max)
```

把一个对象先dump再load后，不保证对象不变，比如说dict会变成list、dict的数值键都会变成字符串键，如果有同一个数的数值键和字符串键，其中一个会被覆盖掉

## logging（日志）

```python
import logging

# 日志配置
# 其实是在配置root logger，所有记录器都会继承这些设置
# 另一种做法是手动创建Formatter和Handler，配置给getLogger(__name__)
logging.basicConfig(
    # 日志等级。低于此等级的消息不输出
    level=logging.INFO,
    # 消息格式（使用这些参数隐式创建一个Formatter并绑定到Handler）
    format='%(asctime)s %(levelname)s-%(name)s: %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',  # 格式同time.strftime
    # 配置Handler（handler决定消息输出到哪里）
    filename='runtime.log',  # 创建一个FileHandler
    encoding='utf-8',
    handlers=(logging.StreamHandler(), )
      # 将这些handler绑定到root logger
      # 若它们没有formatter，则将format参数指定的格式绑定上去
)

# 创建记录器。相同名字创建出来的是指向同一个logger的引用
# logger以.作为分隔符划分层级，比如scan是scan.api的父级；此外，root是所有logger的父级
# 子记录器会继承父级的等级、处理器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 记录日志消息
logger.debug('this is debug message. It has %s', 'formatting')
# 常用等级包括：
# debug    调试信息
# info     程序正常运行
# warning  已经或即将发生意外，程序仍能正常运行
# error    发生严重问题，程序某些功能不能正常执行
# critical 严重错误，程序无法继续执行
```

其他常用Handler

```python
from logging.handlers import TimedRotatingFileHandler
```

## os（操作系统功能）

| function  | usage                                                      |
| --------- | ---------------------------------------------------------- |
| mkdir     | 创建目录                                                   |
| makedirs  | 创建目录（中间路径被一并创建）                             |
| rmdir     | 删除目录                                                   |
| listdir   | 返回目录下全部文件、文件夹                                 |
| remove    | 删除文件                                                   |
| rename    | 重命名文件、文件夹                                         |
| stat      | 查询文件信息，stat(file).st_size, stat(file).st_mtime, ... |
| walk      | 递归遍历全部子文件、文件夹，生成(path, dirs, files)        |
| startfile | 打开文件                                                   |

## pathlib（路径）

pathlib提供不涉及IO操作的纯路径类（`PurePath, PurePosixPath, PureWindowsPath`）和具体路径类（`Path, PosixPath, WindowsPath`），最常用的是`Path`类，它会按照需要自动实例化为`PosixPath`或者`WindowsPath`。在不需要访问操作系统时`PurePath`也有一定用处

```python
from pathlib import Path

p = Path('.')

# 查询路径属性
p.exists()
p.is_dir()
p.is_file()
p.resolve() # 转换为绝对路径
p.parent    # 父目录的路径
p.anchor    # 盘符
p.name      # 文件名/目录名
p.suffix    # 文件后缀，如'.txt'
p.suffixes  # 目录的扩展名列表
p.stem      # 无扩展名的最后一个路径组件

# 子文件、子目录
p.iterdir()         # 迭代子文件和子目录
p.glob('*/*.py')    # 搜索符合条件的子文件和子目录，返回一个生成器

# 使用斜杠组合路径
q = p / 'text.txt'
q = p / Path('text.txt')

# 打开文件
with q.open() as f:
    f.readline()
```

## pickle（保存对象到文件）

python对象的二进制序列化和反序列化。pickling与其他编程语言不兼容，且不同版本的python之间也未必兼容

pickle是不安全的，有办法构建恶意pickle数据，使得在解封时执行任意的代码。不要解封不信任来源的数据、可能被篡改过的数据。需要考虑安全性时，应该用hmal做数字签名

```python
import pickle

obj = pickle.load(fp)
pickle.dump(obj, fp)

pickle_bytes = pickle.dumps(obj)
obj = pickle.loads(pickle_bytes)
```

## re（正则表达式）

```python
import re

pattern = r'abc(\d{3})(\s)'     # 括号括起来部分称为group
string = 'abc123 def, abc456 ghi'

# 匹配字符串
match = re.match(pattern, string)         # 从头开始匹配
f_match = re.fullmatch(pattern, string)   # 全字符串匹配
search = re.search(pattern, string)       # 搜索第一个结果
findall = re.findall(pattern, string)     # 搜索全部非重叠结果，返回为一个list
finditer = re.finditer(pattern, string)   # 同findall，但返回迭代器

# 处理匹配结果
# group
match.group()        # 整个匹配字符串。此处是'abc123 '
match.group(0)       # 同上
match.group(1)       # 第一组，此处为'123'
match.group([1, 2])  # 第一、第二组的tuple，此处为('123', ' ')
match[0]             # 下标访问，和match.group[i]效果相同
# 其他
match.groups()       # 返回所有组的tuple
match.groupdict()    # 返回{组名:内容}，组命名方式是'(?P<name>\d)'
match.start(1)       # 第一组的起始index。end方法同理
match.span(0)        # (start, stop)
match.string         # 整个字符串（即匹配时的string参数）

# 其他功能
re.split(pattern, string)
re.sub(pattern, 'repl', string)
```

## sqlite3（嵌入式SQL数据库）

```python
import sqlite3

# 连接到数据库
conn = sqlite3.connect('test.db')   # 打开/创建数据库文件
cursor = conn.cursor()

# 操作数据库
cursor.execute('create table user (name varchar(100) primary key)')
cursor.execute('insert into user (name) values ("Tim")')
cursor.rowcount                 # insert, update或delete影响的行数
cursor.execute('select * from user')
values = cursor.fetchall()      # 查询结果，List[Tuple]

# 提交事务并关闭
conn.commit()
cursor.close()
conn.close()
```

## subprocess（运行其他程序）

```python
import subprocess

cmd = ['echo', 'Hello']
result = subprocess.run(cmd, capture_output=True, shell=True)
print(result.stdout.decode('utf-8'))
```

更进阶的用法可以参照[`Popen`](https://docs.python.org/zh-cn/3.13/library/subprocess.html#subprocess.Popen)接口

## turtle（海龟画图）

turtle是用于绘图的简单模块，和tk兼容。海龟绘图包含两个要素，绘图区域和画笔。结合tk使用时，对应的类是TurtleScreen和RawTurtle（别名RawPen），构造它们需要提供tk.Canvas。如果单独使用，使用以上两个类的子类Screen和Turtle，Screen是单实例的，而Turtle会在这个Screen实例上绘图，如果Screen实例不存在则会自动创建

turtle模块经常被用来做编程教学，所以有比较完善的过程式绘图方法。但是考虑到以前学matplotlib时过程式绘图的教训，还是用OOP比较稳

```python
from turtle import Turtle, Screen

screen = Screen()
pen = Turtle()

# 屏幕设置
screen.setup(0.5, 0.5)   # 设置屏幕大小和海龟初始位置，Screen独有
screen.screensize()      # 获取/设置屏幕大小
screen.delay()           # 获取/设置画布刷新时间间隔(ms)

# 海龟动作
pen.foward(-10)   # 向后移动10像素
pen.right(90)     # 右转90度
pen.goto(0, 20)   # 移动到坐标
pen.setheading(0) # 设置朝向（角度制，方向同极坐标）

# 获取海龟状态
pen.pos()
pen.heading()

# 画笔控制
pen.up()          # 提起画笔
pen.down()        # 放下画笔
pen.pen()         # 画笔属性字典，包括颜色，粗细等
pen.hideturtle()  # 隐藏海龟标志，可以加速绘制速度

# 关闭窗口
screen.bye()    # Screen独有
```

## urllib（网络）

第三方库[Requests](https://requests.readthedocs.io/en/latest/)在urllib基础上提供了更好用的api，较复杂应用可以考虑用Reauest代替urllib

### request

```python
from urllib import request

# simple GET request
req = request.Request(url)
req.add_header(key, value)
response = request.urlopen(req)  #也可以直接用url做参数，但是这样就不能加header

# 读取response
response.geturl()
response.getcode()  # HTTP status code
response.info()     # meta-information
response.read()     # 网页内容

# POST request
login_data = parse.urlencode(data).encode('utf-8')
req = request.Request('https://passport.weibo.cn/sso/login')
response = request.urlopen(req, data=login_data)

# Proxy
proxy_handler = request.ProxyHandler({'http': 'http://www.proxy.com:3128/'})
opener = request.build_opener(proxy_handler)
response = opener.open(req)     # 使用代理opener进行request
request.install_opener(opener)  # 模块级使用代理opener

# download network object
with open('example.jpg', 'wb') as fp:
    fp.write(response.read())
```

### parse

```python
from urllib import parse

# 分析url
foo = parse.urlparse('https://www.google.com')
    # 用foo.attr的方式获取信息，可以用repr(foo)查看有哪些属性
foo.geturl()  # 完整url

# 拼接url
base = 'https://www.python.org/doc/'
url = '/dev/peps/'
parse.urljoin(base, url)  # 返回'https://www.python.org/dev/peps/'
```

## wave（读写WAV文件）

```python
import wave

# 读wav文件
with wave.open('test.wav', 'rb') as fp:
    fp.getnchannels()      # 声道数量
    fp.getsampwidth()      # 采样深度（字节数）
    fp.getframerate()      # 采样频率
    fp.readframes(100)     # 读取并返回bytes对象的n帧音频
    fp.rewind()            # 回到文件开头
    fp.setpos(100)         # 设置文件指针
    fp.tell()              # 获取文件指针位置

# 写wav文件
with wave.open('mywav.wav', 'wb') as fp:
    # 三个相应的set方法
```

## zipfile（读写zip文件）

```python
import zipfile

# 访问zip文件。注意：第一层是整个文件的
with zipfile.ZipFile('spam.zip', 'a') as myzip:
    with myzip.open('eggs.txt', 'w') as myfile:
        myfile.write(b'eggs')

# Path对象。用法类似pathlib的Path对象，其实是包装过的ZipFile
p = zipfile.Path('spam.zip')
p.is_file('eggs.txt')
```

命令行使用

```bash
# 压缩（Create）
python -m zipfile -c spam.zip "eggs.txt" "process/"
# 解压（Extract）
python -m zipfile -e spam.zip "target-dir/"
# 其他：测试（Test, -t）、列出内容（List, -l）
```



# 有用的第三方库

## pydoc-markdown

从docstring直接生成markdown文档

```
pydocmd simple modulename+ > doc.md
```

注意加号不可省略。生成多个模块的文档只需要同时给多个模块名字（用空格隔开）

## sounddevice（录音和播放声音）

```python
import sounddevice as sd
import numpy as np

# 默认值设置
fs = 44100
sd.default.samplerate = fs  # 采样率(Hz)
sd.default.channels = 1     # 声道
duration = 5    # 持续时间(sec)

# 录音
myrecording = sd.rec(duration * fs, blocking=False)
sd.wait()   # 等待到录音结束，或者用blocking = True
# 录音得到一个np.ndarray，dtype = float，音量不知道怎么算的，振幅为1就已经挺大声了

# 播放
sd.play(myrecording, blocking=True)

# Stream
def func(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

with sd.Stream(callback=func):
    sd.sleep(duration*1000)

# InputStream
```

回调函数详述

sounddevice每隔一定时间会调用一次回调函数。如果没有回调函数，将会在阻塞模式（blocking mode）下运行，使用read write方法进行IO

`callback(indata:ndarray, outdata:ndarray, frames:int, time:cdata, )`

## openpyxl（操作excel表格）

```python
import openpyxl as xl

# 打开表格
wb = xl.load_workbook('example.xlsx')
sheet = wb['Sheet1']

# 读写表格内容
i = sheet['A1'].value
area = sheet['A1':'C2']
area[1][1]  # B1 Cell
sheet['A2'] = 2
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

## 虚拟环境

虚拟环境（Virtual Environment）是一个分离的python环境，可以在此环境安装第三方库而不影响其他python程序，比如给不同程序安装不同版本的库

```shell
# 建立虚拟环境
python -m venv env_name

# 打开虚拟环境
env_name\Scripts\activate.bat            # Windows
env_name\source env_name/bin/activate    # Unix or MacOS
```

打开虚拟环境之后命令行会显示如`(env_name) D:env_name>`的提示符，在此界面运行pip、运行解释器、运行脚本都是对虚拟环境中的东西进行操作

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

符号的unicode其实挺混乱的。比如说，中文逗号是`0xFF0C`Fullwidth Comma，顿号是`0x3001`Ideographic Comma。日文则用Ideographic Comma做逗号
