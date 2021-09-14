# numpy

numerical python

## 数据类型

| type              | description                                |
| ----------------- | ------------------------------------------ |
| int8/16/32/64     | 有符号x位整数                              |
| uint8/16/32/64    | 无符号                                     |
| float32           | 单精度浮点数（和C的float兼容）             |
| float64           | 双精度浮点数（和C的double，py的float兼容） |
| float128          | 扩展精度浮点数                             |
| complex64/128/256 | 实虚部分别用x/2位浮点数表示的复数          |

默认数据类型`int_`, `float_`, `complex_`

## ndarrray

N维定长数组，表示一个标量/矢量/矩阵/张量
要求元素数据类型统一，可以进行优化过的矩阵操作

### indexing

- **simple indexing**

 一维同list；高维数组可以用类似`array[1, -1]`的方式引用

- **bool indexing**

用一个同shape的布尔数组来索引

```python
arr = np.array([1, 3, 2, 1])
bool_arr = [True, True, False, True]
arr[bool_arr]   # array([1, 3, 1])
arr[arr > 1]    # array([3, 2])
```

- **fancy indexing**

用一个array-like object进行索引。用ndarray做fancy indexing好像会有奇怪的错误

```python
arr = np.eye(8)
arr[[0, 2, 4]]       # 第0, 2, 4行
arr[[1, 1], [2, 5]]  # (1, 1)和(2, 5)元素
```

- **slice**

类似内建的切片，但切片的部分不会被复制

```python
arr = np.ones(shape=(10, 8))
array[0:5, ::-1]
```



### 初始化

```python
#一般的
array(object, dtype=None)
   返回根据object(array-like)构建的ndarray
asarray(object, dtype=None)
    和array差不多（少几个可选参数）
    当object为ndarray时，不复制，返回原对象

#一维的
arange([start, ]stop[, step], dtype=None)
    和range函数效果相同，不过返回的是ndarray
linspace(start, stop, num=50, endpoint=True, dtype=None)
    返回等差数列列表
    start, stop     序列起止点
    num             样本点个数
    endpoint        若endpoint=True，则把stop作为最后一个元素，公差为Δ/num
                    否则，不包含stop，公差为Δ/(num-1)
logspace(start, stop, num=50, endpoint=True, base=10.0, dtype=None)
    返回以base^start为首项的等比数列列表
    start, stop     float, 序列起止点

#在整个array填充指定值
ones(shape, dtype=None, order='C')
    返回指定形状的填满1的数组
ones_like(a, dtype=None, order='K')
    返回形状和a相同的填满1的数组
zeros       同ones，填0
zeros_like  同ones_like，填0
empty       同ones，不初始化
empty_like  同ones_like，不初始化
full        同ones，shape后面要一个fill_value，用它填满
full_like   同ones_like，a后面要一个fill_value，用它填满

#单位矩阵
eye(N, M=None, k=0, dtype=<class 'float'>, order='C')
    在指定“对角线”填1，其他填0
    N, M    行列数
    k       k=0为主对角线，正值上移，负值下移
identity(n, dtype=None)
    返回指定大小单位方阵

#特殊的
>>> arr = np.arange(0, 5)
>>> gt = arr>3
array([False, False, False, False,  True])
```

### 属性

    shape       ndarray的形状，即有几个维度、每个维度有多长
                ()          0维数组（标量）
                (5,)        长度为5的一维数组
                (3, 8, 8)   容量为3*8*8的三维数组
    dtype       数据类型
### 方法

    reshape(shape, order='C')
        修改ndarray的shape，但是总长度不能变
        shape参数可以装在tuple里，也可以写成多个参数
    astype(dtype, order, casting, subok, copy)
        返回一个数组，内容为类型转换后的self
        即使dtype和self的类型相同，同样会返回一个拷贝
    a.copy(order='C')
        返回自身的一个拷贝
### 运算

- **常量运算**

常量与ndarray运算，两个shape相同的nearray进行运算，或者数学函数作用于ndarray，相当于其中的逐个元素进行运算

```python
>>> import numpy as np
>>> arr1 = np.array([1, 2, 3, 4, 5])
>>> arr2 = arr1**2
>>> arr2
array([ 1,  4,  9, 16, 25], dtype=int32)
>>>
>>> arr1 * arr2		#注意两个array相乘是逐个元素相乘，而不是矩阵乘法
array([  1,   8,  27,  64, 125])
>>>
>>> np.sqrt(arr2)
array([1., 2., 3., 4., 5.])
```

不同shape的矩阵之间投影后逐元素运算

```python
import numpy as np

arr2d = np.array([[1, 2], [3, 4]])
arr1d = np.array([2, 1])
arr2d - arr1d    # shape分别是(2, 2)和(2, )，结果是array[[-1, 1], [1, 3]]

img_color = np.zeros(shape=(600, 600, 3))
img_gray = np.zeros(shape=(600, 600))
# (600, 600, 3)和(600, 600)不能运算
img_color - img_gray[:, :, None]    # (600, 600, 3)和(600, 600, 1)可以运算
```

- **矩阵运算**

```python
# 矩阵乘法。以下两种方法等价，不改变原矩阵
np.dot(A, B)
A.dob(B)

# 矩阵转置
A.T
```

## 函数

```python
np.argmax(A)        #返回第一个最大值在扁平化数组（相当于A.reshape((n,))）中的index
fill_diagonal(A, v) #对角元填充指定值
triu(A, k)          #返回A的上三角阵
tril(A, k)          #下三角阵
trace(A)            #迹
diagonal(a, offset=0, axis1=0, axis2=1)
                    #对角元
set_printoptions	#设置打印格式（全局），参数举例：
                    #precision=3, suppress=True 小数点后三位，不使用科学记数法
                    #formatter={'float': '{: 0.3f}'.format}
                    #linewidth=90 一行的长度，到了这么多字符就自动换行
```

## 随机

```python
import numpy as np
from numpy.random import Generator, PCG64

np.random.random()                      # 产生[0, 1)均匀分布随机浮点数
np.random.integers(10, 20, size=(5, 5)) # 产生[10, 20)均匀独立分布5x5整数数列
np.random.normal(0, 1.0, size=10)       # 产生长度为10的标准正态分布数列
random.choice(a=[0, 1], p=[0.3, 0.7])   # 已知的离散分布

# 也可以显式创建一个生成器
seed = 12345  # None, int or Array[int]。当缺省/为None时从操作系统取一个随机值
rg = Generator(PCG64(seed))
rg.normal()
```

# how-to

## 求解常微分方程初值问题

`solve_ivp(fun, t_span, y0, method='RK45', t_eval=None, dense_output=False, events=None, vectorized=False, args=None, **options)`

- fun：`Callable[t, y]`，t是时间（自变量），y是因变量或者因变量序列
- t_span：`Tuple[number, number]`，要求解的时间范围
- y0：`Array[number]`，初值
- t_eval：`Array[number]`，差分节点

返回值是个solve对象，打印出来再和后面的例子对照着看就能明白怎么用了

```python
import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# 一阶常微分方程
# 例：y' = e^-t * cost - y，且t = 0时y = 0。解析解为y = e^-t * sint
dy_dt = lambda t, y: np.exp(-t) * np.cos(t) - y
sol = solve_ivp(dy_dt, [0, 10], [0], t_eval=np.linspace(0, 10))
plt.plot(sol.t, sol.y[0])
plt.show()

# 一阶常微分方程组
# 例：y0' = y1, y1' = -y0，且t = 0时y0 = 0，y1 = 1。解析解为y0 = sint, y1 = cost
dy_dt = lambda t, y: [y[1], -y[0]]
sol = solve_ivp(dy_dt, [0, 10], [0, 1], t_eval=np.linspace(0, 10))
plt.subplots()
plt.plot(sol.t, sol.y[0])
plt.plot(sol.t, sol.y[1])
plt.show()
```

高阶常微分方程处置问题也可以用这个方法来解。例：
$$
\left\{
\begin{aligned}
&\frac{d^2y}{dt^2} + \frac{dy}{dt} + y = 0 \\
&y|_{t = 0} = 1  \\
&\frac{dy}{dt}|_{t = 0} = 0 \\
\end{aligned}
\right.
$$

令$u_0 = y, u_1 = \frac{dy}{dt}$，则方程化为一阶线性方程组
$$
\left\{
\begin{aligned}
&\frac{du_0}{dt} = u_1 \\
&\frac{du_1}{dt} = -u0 - u1  \\
&u_0(0) = 1 \\
&u_1(0) = 0 \\
\end{aligned}
\right.
$$

## 傅里叶变换

```python
from numpy.fft import fft

t = np.linspace(0, 1000)
y = 4*np.sin(2*t) + np.sin(4*t)
f = fft(y)
```

## 巴特沃夫滤波

```python
import numpy as np
import scipy.signal as signal

t = np.linspace(0, 100)
y = np.sin(2 * np.pi * t) + np.cos(20 * np.pi * t)
max_freq = 5
sos = signal.butter(10, max_freq, 'lowpass', output='sos')
filtered = signal.sosfilt(sos, y)
```

## 寻找极大值/极小值/局部极值

```python
import numpy as np
import scipy.signal as signal

# 假设arr是一个有噪声的序列，局部极值之间的距离大于100。极小值同理，找-arr的极大值
maxima, _ = signal.find_peaks(arr, distance=100)
```

## 任意函数拟合

```python
from scipy.optimize import curve_fit

# 假设对x, y做线性拟合
linear = lambda x, k, b: k * x + b
popt, pcov = curve_fit(linear, x, y)
# popt = [k, b]
# pcov = 协方差
y_fit = linear(x, *popt)
```

## 寻找最大值所在位置

```python
import numpy as np
index = np.argmin(arr)
np.where(arr == 3)
```

## 排序

```python
# 基本排序
arr = np.array([[1, 6, 5], [7, 2, 3]])
np.sort(arr, axis=-1)   # 沿最后一根axis排序。返回[[1, 5, 6], [2, 3, 7]]，不改变原数组
arr.sort(axis=0)        # 沿第一根axis排序。返回None，原数组变为[[1, 2, 3], [7, 6, 5]]

# 沿某一行/某一列排序
arr = np.array([[1, 6, 5], [7, 2, 3]])
a[:, a[0, :].argsort()]
a[a[:, 0].argsort()]
```

## 拼接数组

```python
arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

# 沿着某条axis拼接，如将两个一维数组拼成更长一维数组
arr3 = np.concatenate([arr1, arr2], axis=0)

# 拼至一条新axis，如将两个一维数组拼成二维数组
arr4 = np.stack([arr1, arr2], axis=0)   # shape = (2, 3)
arr5 = np.stack([arr1, arr2], axis=1)   # shape = (3, 2)，相当于上一个的转置
```

