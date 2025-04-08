# Scrapy

## Command line tool

```shell
scrapy [command] <options> <args>

global commands
startproject <name> [dir]	创建新项目
genspider <name> <domain>	在当前文件夹/当前项目的spider文件夹创建新爬虫
shell <url>			在shell中打开url，打开的网页在response对象

project-only commands
crawl <spider>	用指定的spider爬取网页

-h	帮助
```

## Spider

```
class scrpy.spider.Spider
属性
name		独一无二的名字
allowed_domains	若开启OffsiteMiddleware，不属于此list的域名将不会被爬
start_urls		list
其他属性
custom_settings, crawler, settings, logger
```

### 方法

```
parse(self, response)		default callback. Must return an iterable of Request and/or dicts or Item objects.
log(message[, level, component])	Wrapper that sends a log message through the Spider’s logger

其他方法
from_crawler, srart_requests, closed(reason)
following links	response.follow(url, callback)	支持相对路径url

用yield，可以产生多个返回值。回调函数必须返回Request, Item object, dicts 或其iterable
```

## Selector

### 定义selector

```
Selector(response, text, type)
response    HtmlResponse or XmlResponse object
text        string. Using text and response together is undefined behavior
type        if type==None, it will be inferred from response type. ('html' for text)
            Otherwise it will be forced.
            注：完整地说应该是scrapy.http.request.Request object
            但是用scrapy.Request('url', callback)同样能定义
response.selector也是其对应selector对象
```

### 使用selector

```
方法
css	传入css表达式，返回装有对应节点的selector list
xpath	传入xpath表达式，返回装有对应节点的selector list
	response.xpath('$var', var="sth")可以在xpath表达式中使用变量
re	传入正则表达式，返回匹配到内容的unicode字符串列表
	注：there are shortcuts response.css, response.xpath ...
extract		提取当前节点的内容
extract_first		提取selector list中第一个元素内容。若为空列表，返回None（也可以传入参数default来指定此时返回的内容
re_first		返回正则表达式匹配到的第一个字符串
urljoin		连接当前url与相对路径
register_namespace(prefix, url)
remove_namespaces()
```

### SelectorList

装有selector的列表。对其使用Selector的方法，相当于对其中每个元素分别使用

## Item

```
Item is a class with dictionary-like API, which is intruduced to make the output more structured
declaring item	key=scrapy.Field(**args)
		(虽然形式上是定义了类属性，实际上只是提供了有那些允许的属性名称)

可用args
serializer	???用途不明
input_processor
output_processor

attribute
fields	一个包含field信息的dict

Field
完全相同于dict

如果不想item的内容都被打印出来，可以重写__repr__
e.g.
def __repr__(self) :
    attr = {想要打印的内容的dict}
    return repr(attr)
```

## ItemLoader

```
方便地填充item
from scrapy.loader import ItemLoader
ItemLoader(item, selector, response)
item	一个dict或item，用于填充内容
selector	从selector提取数据
response	从response产生一个selector. If selector argument is given, it will be ignored.

方法
add_xpath(field, xpath)
add_css(field, css)
add_value(filed, value)
load_item()
Input Processor	自己定义，名称为fieldName_in，default_input_processor
Output Processor	自己定义，名称为fieldName_out，default_output_processor
nested_xpath(xpath)	创建nested loader
nested_css(css)	创建nested loader

不常用方法
get_collected_values(fieldName)
get_output_value(fieldName)
get_input_processor(fieldName)
get_output_processor(fieldName)
item()
context()
selector()
```

### 工作流程

每次使用三个add方法之一，就向指定的field的Input Processor传相应的参数，Input Processor处理后的结果暂时存储在```ItemLoader```中的一个list；当使用load_item方法时，分别调用每个field的Output Processor，将处理后的结果存到Item中，返回该Item
Input Processor 和Output Processor都应该接受一个iterator，返回值没有要求
使用哪个Processor的优先级：```ItemLoader field-specific attributes > Field metadata > ItemLoader defaults```

Loader Context
一个叫做context，type为dict的属性，允许在任何时候任意地修改它
当一个方法有参数loader_context时，会被自动传入

Built-in processors

```
(in module scrapy.loader.processors)
参数均是一个iterator
Identity		什么都不做
TakeFirst		返回第一个非空元素
Join(seperator=u' ')	连接字符串
Compose(*functions, **default_loader_context)
		按顺序调用每个function（用第一个函数的返回值作为第二个函数的参数，以此类推）
MapCompose(*functions, **default_loader_context)
		对iterator中每个元素调用第一个function，产生新的iterator，再对新iterator中元素分别调用第二个iterator，以此类推
```

## ItemPipeline

(item pipeline继承自Object类)
必须有的方法

```
process_item(self, item, spider)	自动对每个pipeline component调用。返回1)dict, 2)item, 3)Twisted Deferred, 4)raise DropItem exception
open_spider(self, spider)	当spider开始运行时调用
close_spider(self, spider)	当spider关闭时调用
from_crawler(cls, crawler)	If present, this classmethod is called to create a pipeline instance from a Crawler. It must return a new instance of the pipeline.

Activating ItemPipeline component
example:
ITEM_PIPELINES = {
    'myproject.pipelines.PricePipeline': 300,		#this value must be an int ranged from 0 to 1000
    'myproject.pipelines.JsonWriterPipeline': 800,	#items go through from lower valued to higher valued classes
}
```

## Feed Export

（待补充）

## Request

```
class scrapy.http.Request(url[, callback, method='GET', headers, body, cookies, meta, encoding='utf-8', priority=0, dont_filter=False, errback, flags])

属性
url	string, read only
method	A string representing the HTTP method in the request (GET, POST, PUT, etc.)
headers	dictionary-like
body	string, read only
meta	meta是一个dictionary, 可以通过response.meta访问，给callback函数传额外内容

方法
copy()
replace([url, method, headers, body, cookies, meta, encoding, dont_filter, callback, errback])
```

## Response

```
class scrapy.http.Response(url[, status=200, headers=None, body=b'', flags=None, request=None])

属性
url
status	http状态码
headers
body
request	The Request object that generated this response
meta	=response.request.meta
flags

方法
copy()
replace([url, status, headers, body, request, flags, cls])
urljoin(url)		接受相对地址，返回绝对地址。wrapper over urlparse.urljoin
 follow(url, callback=None, method='GET', headers=None, body=None, cookies=None, meta=None, encoding='utf-8', priority=0, dont_filter=False, errback=None)
		接受相对地址，返回Request对象
```

## Logging in scrapy

Spider有属性logger，能用它logging (e.g. self.logger.info('page 1 scraped'))

# XPath

使用路径表达式选取XML文档中的节点或节点集

节点(Node)

有七种类型的节点：元素、属性、文本、命名空间、处理指令、注释以及文档（根）节点

基本值(Atomic value)
无父或无子的节点

节点关系
Parent, Children, Sibling, Ancestor, Descendant

路径表达式

```
/absolute_path  以/起始的路径表示绝对路径
path/name       all children node called "name"
path//name      all descendant node called "name"
.               当前节点
..              当前节点的父节点
@               选取属性
text()          该元素的文本内容
```

谓语
谓语用[]括起来，接在路径表达式中表示选取满足特定条件的节点

```
数字         第i个子元素（从1开始）
last()      最后一个，能进行运算，如last()-2
position()  位置，以不等式来使用，如position()<3
@attr       拥有attr属性的元素节点
@attr="v"   attr属性的值为v的元素节点
ele         元素的值满足某些要求，如price>35.00
```

通配符

```
*       任何元素节点
@*      任何属性节点
node()  任何节点
|       放在两个路径表达式中间表示或
```

Xpath轴

```
定义相对于当前节点的节点集
ancestor            所有先辈（父、祖父等）
descendant          所有后代元素（子、孙等）
ancestor-or-self    ancestor & 本身
descendant-or-self  descendant & 本身
parent              父节点
child               子元素
self                自身
attribute           当前节点的所有属性
preceding           当前节点的开始标签之前的所有节点
following           当前节点的结束标签之后的所有节点
namespace           当前节点的所有命名空间节点
preceding-sibling   当前节点之前的所有同级节点

轴名称::节点测试[谓语]
例：child::*/child::price	当前节点的所有 price 孙节点
```
