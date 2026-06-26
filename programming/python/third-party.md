# 简介

python有大量第三方模块，只要在[PyPI](https://pypi.org/)上注册就能发行自己的模块，可以通过pip等工具非常方便地安装第三方模块。本笔记记录第三方模块的管理方法，以及部分第三方模块的使用（内容较少或我学习不深入的记录在这里，体量较大的单独放一个笔记）

第三方模块的安装、更新、卸载都可以用工具实现。第三方模块的管理又分为两个层面：

- **包管理**：pip
- **环境管理**：venv

还有很多第三方的管理工具，如[uv](https://docs.astral.sh/uv/)、[conda](https://mirrors.tuna.tsinghua.edu.cn/anaconda/)。这几个工具各有优势，都可以用，无非是速度、方便程度各有高低，哪个最好用也没有定论

# pip + venv

python自带的管理工具

```shell
python -m venv env_name
```

虚拟环境（Virtual Environment）是一个分离的python环境，可以在此环境安装第三方库而不影响其他python程序，比如给不同程序安装不同版本的库

```shell
# 建立虚拟环境
python -m venv env_name

# 打开虚拟环境
env_name\Scripts\activate.bat            # Windows
env_name\source env_name/bin/activate    # Unix or MacOS
```

打开虚拟环境之后命令行会显示如`(env_name) D:env_name>`的提示符，在此界面运行pip、运行解释器、运行脚本都是对虚拟环境中的东西进行操作

# uv

uv是用Rust写的python环境管理工具，运行速度比pip快得多。安装以及使用方式可以参考[uv文档](https://docs.astral.sh/uv/)

- 脚本一键安装：`powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`，默认安装位置`%USERPROFILE%/.local/bin`
- 手动安装：下载[uv Releases](https://github.com/astral-sh/uv/releases)，将`uv.exe`路径加入Path

## 配置

**管理python版本**

```shell
uv python list          # 查看可安装版本
uv python install 3.12
uv python dir           # 查看安装位置
uv python pin 3.12      # 设置为默认版本
```

管理

**管理存储目录**

```shell
uv cache dir    # 查看缓存目录
uv cache clean requests  # 删除requests库
uv cache clean  # 删除全部库
uv cache prune  # 删除过时库文件

uv tool dir     # 查看工具安装目录
```

安装第三方库时，库文件首先下载到缓存目录；虚拟环境使用第三方库时，若缓存目录和虚拟环境在同一个盘，用硬链接直接引用缓存的库文件。参考文档[Settings | uv](https://docs.astral.sh/uv/reference/settings/#cache-dir)，添加以下配置可更改缓存目录

```toml
# 用户配置文件`%APPDATA%\uv\uv.toml`（Windows）或`~/.config/uv/uv.toml`（Linux）
cache-dir = "./.uv_cache"

# 项目配置文件`pyproject.toml`
[tool.uv]
cache-dir = "./.uv_cache"
```

工具目录需要用环境变量设置，添加环境变量`UV_TOOL_DIR`，设置为工具的安装目录

**换源**

在配置文件中添加下面的内容。用户配置文件或项目配置文件`pyproject.tmol`
```toml
# 用户配置文件`%APPDATA%\uv\uv.toml`（Windows）或`~/.config/uv/uv.toml`（Linux）
# 或者项目配置文件``pyproject.toml
[[index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

或者用`--index`参数临时指定镜像

## 运行脚本

```shell
uv run example.py
```

以上命令会在虚拟环境运行脚本。uv会自动安装inline metadata指定的包，格式如下：

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "requests<3",
#   "rich",
# ]
# ///

import requests
from rich.pretty import pprint
```

或者用`--with`参数：

```shell
uv run --with requests,rich example.py
```

## 管理Project

创建项目时，会创建`pyproject.toml, .python-version, uv.lock`等配置文件，还有对应的虚拟环境（默认为`.venv`）。安装或删除第三方库时，会将操作记录在配置文件中，并修改虚拟环境

这种管理方式的好处是容易发布、容易管理——只需发布环境配置文件和源代码，其他人就能简单地配出完全相同的运行环境；需要配多个不同环境时，只需创建多个项目，在每个项目的虚拟环境中分别配置即可

```shell
uv init example-app   # 创建项目
cd example-app
uv add requests       # 在项目虚拟环境中安装模块(所有操作都在虚拟环境中，之后不再重复说明)
uv run python         # 运行python
```

uv通过在当前目录下找`pyproject.toml`文件来确定使用哪个项目。也可以用`--project 目录`指定Project

## 安装本地包

**方法1**：安装为可编辑的包。会成为不在`pyproject.toml`中的“幽灵依赖”，但修改包的代码后可以直接运行

```bash
uv pip install -e "pkg_name @ ./path/to/pkg"
```

**方法2**：添加到项目。首先在项目的`pyproject.toml`添加配置

```toml
[project]
dependencies = [
    "local-package"
]

[tool.uv.sources]
local-package = { path = "../local_package"}
```

然后运行`uv sync`更新环境。更新代码之后可能需要重装：

```bash
uv sync --reinstall-package local-package
```

# 第三方库

## openpyxl - 操作excel表格

```python
from openpyxl import load_workbook

# 打开表格
wb = load_workbook('example.xlsx')
sheet = wb['Sheet1']

# 读写表格内容
i = sheet['A1'].value
area = sheet['A1':'C2']
area[1][1]  # B1 Cell
sheet['A2'] = 2

# iter
for row in ws.iter_rows(min_row=2):
    print(row[0])
```

## passlib - 密码散列

算法列表：https://passlib.readthedocs.io/en/stable/lib/passlib.hash.html#module-passlib.hash

```python
from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("password")       # 计算hash
if pbkdf2_sha256.verify("password", hash):  # 验证hash
    print('success')
```

## sounddevice - 录音和播放声音

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
```

回调函数参数：`callback(indata:ndarray, outdata:ndarray, frames:int, time:cdata, status)`

sounddevice每隔一定时间会调用一次回调函数。如果没有回调函数，将会在阻塞模式（blocking mode）下运行，使用read write方法进行IO

## tensorflow - 神经网络

Sequential是若干线性堆叠的层构成的神经网络，其中每层输入输出都为一个张量

```python
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 定义Sequential模型
model = keras.Sequential()
model.add(tf.keras.layers.Flatten(input_shape=(28, 28)))
model.add(tf.keras.layers.Dense(128, activation='relu'))   # 128节点的全连接层
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.summary()    # 查看每层的输入输出形状、总参数数量

# 加载训练数据集
mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()
# mnist是手写数字数据集
# train_images是一个60000*28*28的numpy数组（60000张28*28的手写数字图片）
# train_labels是长度60000的numpy数组，代表图片中的数字
# test与train类似，不过只有10000张
x_train, x_test = x_train / 255.0, x_test / 255.0  # 转为0~1浮点数

# 指定训练配置：优化器、损失、指标
model.compile(optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'])

# 训练与验证模型
history = model.fit(train_images, train_labels, epochs=5)
result = model.evaluate(test_images, test_labels, verbose=2)

# 保存与加载模型
model.save('my_model')    # 创建my_model的文件夹，并将模型架构、权重、训练配置存进去
my_model = keras.models.load_model('my_model')
```
