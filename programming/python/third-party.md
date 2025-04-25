# 简介

python有大量第三方模块，只要在[PyPI](https://pypi.org/)上注册就能发行自己的模块，可以通过pip等工具非常方便地安装第三方模块。本笔记记录第三方模块的管理方法，以及部分第三方模块的使用（内容较少或我学习不深入的记录在这里，体量较大的单独放一个笔记）

# 管理工具

第三方模块的安装、更新、卸载都可以用工具实现。第三方模块的管理又分为两个层面：

- **包管理**：pip
- **环境管理**：venv

还有很多第三方的管理工具，如[uv](https://docs.astral.sh/uv/)、[conda](https://mirrors.tuna.tsinghua.edu.cn/anaconda/)。这几个工具各有优势，都可以用，无非是速度、方便程度各有高低，哪个最好用也没有定论

## pip + venv

python自带的管理工具

## uv

uv是用Rust写的python环境管理工具，运行速度比pip快得多。安装以及使用方式可以参考[uv文档](https://docs.astral.sh/uv/)

**更换镜像**

1. 创建环境变量`UV_DEFAULT_INDEX`，变量值为镜像源地址
2. 在配置文件中添加下面的内容
   - 用户配置文件：`%APPDATA\uv\uv.toml`（Windows）或`~/.config/uv/uv.toml`（Linux）
   - 项目配置文件：`pyproject.toml`

```toml
[[index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

3. 用`--index`或`--default-index`参数临时指定镜像

**Project**

uv一般使用Project来管理python运行环境。创建项目时，会创建`pyproject.toml, .python-version, uv.lock`等配置文件，还有对应的虚拟环境（默认为`.venv`）。安装或删除第三方库时，会将操作记录在配置文件中，并修改虚拟环境

这种管理方式的好处是容易发布、容易管理——只需发布环境配置文件和源代码，其他人就能简单地配出完全相同的运行环境；需要配多个不同环境时，只需创建多个项目，在每个项目的虚拟环境中分别配置即可

```shell
uv init example-app   # 创建项目
cd example-app
uv add requests       # 在项目虚拟环境中安装模块(所有操作都在虚拟环境中，之后不再重复说明)
uv run python         # 运行python
```

uv通过在当前目录下找`pyproject.toml`文件来确定使用哪个项目。也可以用`--project 目录`参数指定项目。`uv run`会用真实环境（而非虚拟环境）运行；`uv add`则无法安装模块（理论上来说，可以用`uv pip`指令安装模块到真实环境，不过都用上uv了就别画蛇添足）

# 第三方库

## passlib - 密码散列

算法列表：https://passlib.readthedocs.io/en/stable/lib/passlib.hash.html#module-passlib.hash

```python
from passlib.hash import pbkdf2_sha256

hash = pbkdf2_sha256.hash("password")       # 计算hash
if pbkdf2_sha256.verify("password", hash):  # 验证hash
    print('success')
```

## whisper - 语音识别

NA

## pydoc-markdown

从docstring直接生成markdown文档

```
pydocmd simple modulename+ > doc.md
```

注意加号不可省略。生成多个模块的文档只需要同时给多个模块名字（用空格隔开）

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

# InputStream
```

回调函数详述

sounddevice每隔一定时间会调用一次回调函数。如果没有回调函数，将会在阻塞模式（blocking mode）下运行，使用read write方法进行IO

`callback(indata:ndarray, outdata:ndarray, frames:int, time:cdata, )`

## openpyxl - 操作excel表格

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

## requests - 网络请求

```python
import requests

# GET请求
get_response = requests.get(
    'example.com',
    params={'page', '1'},                     # GET参数
    headers={'User-Agent': 'Mozilla/5.0'}     # 请求头
    cookies={'SESSIONID':'8A25432CEC745A1C'}  # Cookie
)

# POST请求
post_response = requests.post(
    'example.com',
    headers={'Referer':'example.com/login'},  # 请求头
    cookies={'SESSIONID':'8A25432CEC745A1C'}, # Cookie
    data={'user':'admin', 'action':'logout'}  # 请求体
)

# 响应
r = get_response
r.status_code   # 状态码 
r.headers       # 响应头, dict
r.text          # 文本格式的响应体
r.content       # 二进制格式的响应体
r.json()        # 用json解码的响应体
```



```python
# 使用代理
cert = '../cert/burp-ca.crt'
proxy = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}
requests.get('example.com', proxies=proxy, verify=cert)
```