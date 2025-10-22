# argparse - 命令行参数

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

# code - 自定义python解释器

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

# collections - 容器

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

# configparse - 配置文件

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

# csv - 读写CSV文件

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



# datetime - 时间

有两个时间的库：time和datetime，前者更接近操作系统层面，而datetime做了一定的封装，功能更丰富，用起来更容易

```python
from datetime import datetime, timedelta

some_time = datetime(year=2020, month=2, day=2)
now = datetime.now()  # 当前时间
tomorrow = now + timedelta(days=1)  # 时间偏移量

# 时间戳(float, in seconds)
timestamp = now.timestamp()
now_fromstamp = datetime.fromtimestamp(timestamp)
now_utc = datetime.utcfromtimestamp(timestamp)

# 时间字符串
time_str = now.strftime('%Y.%m.%d %H:%M:%S')
fromstr = datetime.strptime('2020.02.02', '%Y.%m.%d')
```

# hashlib

包括sha256, sha512等哈希算法

```python
import hashlib
h = hashlib.md5(b'some bytes')
h.update(b"update this hash object's state")
b = h.digest()         #得到bytes类型的hash
x = b.hexdigest()      #得到16进制字符串
```

# http.server - http服务器

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
        # 处理GET请求。当收到GET请求时调用此函数，请求参数是self.headers、self.path等
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

# json - 读写JSON文件

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

# logging - 日志

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

# pathlib - 路径

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

# re - 正则表达式

```python
import re

pattern = r'abc(\d{3})(\s)'     # 括号括起来部分称为group
string = 'abc123 def, abc456 ghi'

# 匹配字符串
match = re.search(pattern, string)   # 搜索第一个结果，返回Match对象
re.findall(pattern, string)          # 搜索全部非重叠结果，返回list[str]

# 处理匹配结果
match.group()        # 整个匹配字符串。此处是'abc123 '
match.group(1)       # 第一组，此处为'123'
match.groups()       # 返回所有组的tuple

# 其他功能
re.split(pattern, string)
re.sub(pattern, 'repl', string)
```

# socket - 套接字编程

```python
import socket

with socket.create_connection(('127.0.0.1', 8000), timeout=1):
    sock.sendall(b'example message\n')
    response = sock.recv(4096)
```

# sqlite3 - 嵌入式SQL数据库

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

# subprocess - 启动子进程

```python
import subprocess

cmd = ['powershell', 'write-host', 'Hello']
result = subprocess.run(cmd, capture_output=True)
print(result.stdout.decode('utf-8'))
```

# urllib - 网络

第三方库[Requests](https://requests.readthedocs.io/en/latest/)在urllib基础上提供了更好用的api，较复杂应用可以考虑用Request代替urllib

## request

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

## parse

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

# wave - 读写WAV文件

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

# zipfile - 读写zip文件

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
