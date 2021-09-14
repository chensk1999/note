# urllib.request

```
urlopen(url, data=None, [timeout, ] *, cafile=None, capath=None, cadefault=False, context=None)
	url	网页url，可以是一个string或Request object
	data	需要Post给服务器的信息
	timeout	访问超时时间（单位：s）
	其余	与身份验证有关
总是返回一个有如下方法的对象：
geturl()	返回网页url
info()	返回meta-information
getcode()	返回http status code
对于http以及https协议的网页，返回一个http.client.HTTPResponse对象

Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
	url, data同urlopen
	headers是一个dict，常包含：User-Agent, Referer, Connection（注：Referer没有双写r，不是referrer）
	也可以用add_header方法添加header
Request类的方法
add_header(key, value)
```

# HTML

HTML(超文本标记语言，Hyper-Text Markup Language)是用于创建网页的标准标记语言

HTML元素以起始标签（如```<p>```）起始，终止标签（如```</p>```）结束，起止标签中间的内容就是元素的内容，有的标签具有空内容，空元素甚至在同一个标签同时起始和终止。不同种类的标签定义了不同的网页元素（如，标题，段落，etc.）。标签常具有属性，属性可能规定了其样式，也可能是用于区分不同标签的

爬虫需要通过各种方式选中想要的标签，从而爬取需要的内容

# XML(EXtensible Markup Language)

类似与HTML, 但XML设计来传输数据，而非显示数据
XML的标签没有预定义，都是由文档创作者所写
XML标签对大小写敏感
允许嵌套（但必须是严格的嵌套），每个XML文档有且仅有一个根元素

## 实体引用

欲使用一些预保留字符，xml文档编码所无法表示的unicode字符，需要用实体引用，规则是&实体名;

```
实体名	含义
lt    <
gt    >
amp   &
apos  '
quot  "
```

## XML命名空间(XML Namespaces)

<前缀:标签名 xmlns:前缀="命名空间">
<root xmlns:前缀="命名空间">（在根元素中声明）
一个命名空间被定义后，拥有相同前缀的元素都与该空间相关联
命名空间通常使用对应的url

## XHTML

XHTML是结合了XML和HTML的一种标记语言
语法规则大体与XML相同，功能大体与HTML4相同

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

# CSS

样式层叠表，Cascading Style Sheets

## CSS选择器

```
选择器              例子              说明                       在CSS几定义的
.class             .intro           选择 class="intro" 的所有元素			1
#id                #firstname       选择 id="firstname" 的所有元素			1
*                  *                选择所有元素				2
element            p                选择所有 <p> 元素				1
element,element    div,p            选择所有 <div> 元素和所有 <p> 元素		1
element element    div p            选择 <div> 元素内部的所有 <p> 元素		1
element>element    div>p            选择父元素为 <div> 元素的所有 <p> 元素		2
element+element    div+p            选择紧接在 <div> 元素之后的所有 <p> 元素	2
[attribute]        [target]         选择带有 target 属性所有元素			2
[attribute=value]  [target=_blank]  选择 target="_blank" 的所有元素			2
[attribute~=value] [title~=flower]  选择 title 属性包含单词 "flower" 的所有元素		2
[attribute|=value] [lang|=en]       选择 lang 属性值以 "en" 开头的所有元素		2
:link              a:link           选择所有未被访问的链接			1
:visited           a:visited        选择所有已被访问的链接			1
:active            a:active         选择活动链接				1
:hover             a:hover          选择鼠标指针位于其上的链接			1
:focus             input:focus      选择获得焦点的 input 元素			2
:first-letter      p:first-letter		选择每个 <p> 元素的首字母			1
:first-line        p:first-line		选择每个 <p> 元素的首行			1
:first-child       p:first-child		选择属于父元素的第一个子元素的每个 <p> 元素 	2
:before            p:before		在每个 <p> 元素的内容之前插入内容 		2
:after             p:after		在每个 <p> 元素的内容之后插入内容 		2
:lang(language)    p:lang(it)		选择带有以 "it" 开头的 lang 属性值的每个 <p> 元素	2
element1~element2  p~ul		选择前面有 <p> 元素的每个 <ul> 元素		3
[attribute^=value] a[src^="https"]	选择其 src 属性值以 "https" 开头的每个 <a> 元素	3
[attribute$=value] a[src$=".pdf"]	选择其 src 属性以 ".pdf" 结尾的所有 <a> 元素	3
[attribute*=value] a[src*="abc"]	选择其 src 属性中包含 "abc" 子串的每个 <a> 元素	3
:first-of-type     p:first-of-type	选择属于其父元素的首个 <p> 元素的每个 <p> 元素	3
:last-of-type      p:last-of-type	选择属于其父元素的最后 <p> 元素的每个 <p> 元素	3
:only-of-type      p:only-of-type	选择属于其父元素唯一的 <p> 元素的每个 <p> 元素	3
:only-child        p:only-child	选择属于其父元素的唯一子元素的每个 <p> 元素	3
:nth-child(n)      p:nth-child(2)	选择属于其父元素的第二个子元素的每个 <p> 元素	3
:nth-last-child(n) p:nth-last-child(2)	同上，从最后一个子元素开始计数		3
:nth-of-type(n)    p:nth-of-type(2)	选择属于其父元素第二个 <p> 元素的每个 <p> 元素	3
:nth-last-of-type(n)	p:nth-last-of-type(2)	同上，但是从最后一个子元素开始计数		3
:last-child        p:last-child		选择属于其父元素最后一个子元素每个 <p> 元素	3
:root              :root		选择文档的根元素				3
:empty             p:empty		选择没有子元素的每个 <p> 元素（包括文本节点）	3
:target            #news:target	选择当前活动的 #news 元素			3
:enabled           input:enabled	选择每个启用的 <input> 元素			3
:disabled          input:disabled	选择每个禁用的 <input> 元素			3
:checked           input:checked	选择每个被选中的 <input> 元素			3
:not(selector)     :not(p)		选择非 <p> 元素的每个元素			3
::selection        ::selection		选择被用户选取的元素部分			3
```

# Scrapy

## Command line tool

```
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