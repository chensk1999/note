HTML定义了网页的内容，CSS 描述了网页的布局，JavaScript描述网页的行为。较为成熟的开发模式是分别设计HTML、CSS和JavaScript，然后在HTML里面调用另外两者。简单的网页可以把全部东西塞进html里，但考虑可维护性，还是强烈不建议这么做

# HTML

HTML（超文本标记语言，Hyper-Text Markup Language）是用于创建网页的标准标记语言

HTML由多个**元素**（Element）组成。元素由起始标签、元素的内容、终止标签构成，例如`<p>Hello, World</p>`。元素可以没有内容，甚至可以在起始的同时终止（比如，换行标签`<br />`。一些不规范写法将其写成`<br>`，可能会被当作缺少终止标签）

元素常具有**属性**（Attribute），属性用键值对表示，且属性值必须用引号括起来。例：`<a href="http://www.baidu.com">百度</a>`。特别地，元素的`id`属性必须是独一无二的，常用于标识元素；`class`属性可包含用空格分开的多个值

## 基础

```html
<!DOCTYPE html>   <!-- 声明是html5文档。建议用小写标签 -->
<html>            <!-- 根元素 -->
    <head>  <!-- 元数据 -->
        <title>文档标题</title>
        <meta charset="utf-8" />
    </head>

    <body>  <!-- 网页内容 -->
        <h1>一级标题</h1>
        <p>段落</p>
        <a href="http://www.google.com">超文本链接</a>
        <img src="/images/logo.png" width="100%" />
        <br>  <!-- 换行。源代码中的连续空白、空行都会被当作一个空格 -->
        <hr>  <!-- 分割线 -->
        <div>块级元素，经常当作容器</div>
  </body>
</html>
```

## 表单

表单用于收集用户输入。它由一个`form`元素和其中嵌套的若干`input`标签构成。当用户按下`type="submit"`的按钮之后，浏览器向服务器发出请求，请求地址为`form.action`，方法为`form.method`，并以`input.name=input.value`键值对作为参数。例如：

```html
<form action="/login" method="POST">
  <input type="email" name="email" required>
  <input type="password" name="password" required>
  <input type="submit" name="login_submit" value="Login">
</form>
```

以上代码创建了一个带有邮箱输入框、密码输入框、提交按钮的表单。按下提交按钮之后，浏览器以POST方法发出请求，请求地址是`example.com/login`，参数为`email=example@email.com&password=123456&login_submit=Login`

表单中一般还会包含说明文字。完整示例如下

```html
<form action="/" method="post">
    <!-- 文本输入框 -->
    <label for="name">用户名:</label>
    <input type="text" id="name" name="name" required>
    <br>

    <!-- 密码输入框 -->
    <label for="password">密码:</label>
    <input type="password" id="password" name="password" required>
    <br>

    <!-- 单选按钮 -->
    <label>性别:</label>
    <input type="radio" id="male" name="gender" value="male" checked>
    <label for="male">男</label>
    <input type="radio" id="female" name="gender" value="female">
    <label for="female">女</label>
    <br>

    <!-- 复选框 -->
    <input type="checkbox" id="subscribe" name="subscribe" checked>
    <label for="subscribe">订阅推送信息</label>
    <br>

    <!-- 下拉列表 -->
    <label for="country">国家:</label>
    <select id="country" name="country">
        <option value="cn">CN</option>
        <option value="usa">USA</option>
        <option value="uk">UK</option>
    </select>
    <br>

    <!-- 提交按钮 -->
    <input type="submit" value="提交">
</form>
```

# XML

XML（EXtensible Markup Language）是类似HTML的标记语言，但注重传输数据而非显示数据。XML没有预定义标签，标签名对大小写敏感，允许嵌套元素（但必须是严格的嵌套），每个XML文档有且仅有一个根元素

XML的嵌套元素形成了树状结构，每个元素也称作一个节点（Node）

## XPath

XPath（XML路径语言，XML Path Language）是用于描述XML中某部分位置的语言。以下面的XML为例

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bookstore>
    <book>
      <title lang="en-gb">Harry Potter</title>
      <price>29.99</price>
    </book>
    <book>
      <title lang="en-us">Learning XML</title>
      <price>39.95</price>
    </book>
</bookstore>
```

```powershell
[xml]$xml = Get-Content bookstore.xml
$bs = $xml.bookstore

# 路径
Select-Xml -Xml $bs -XPath "book"    # 相对路径
Select-Xml -Xml $bs -XPath "/"       # 绝对路径
Select-Xml -Xml $bs -XPath "//"      # 任意子路径
Select-Xml -Xml $bs -XPath "//@lang" # 具有lang属性的节点
Select-Xml -Xml $bs -XPath "book/*"  # 通配符
Select-Xml -Xml $bs -XPath "//title/text()"  # 节点内的文本
# 谓词（Predicates）
Select-Xml -Xml $bs -XPath "book[last()-1]"      # indexing。下标从1开始
Select-Xml -Xml $bs -XPath "book[position()<3]"  # 范围indexing
Select-Xml -Xml $bs -XPath "//title[@lang]"          # 具有lang属性
Select-Xml -Xml $bs -XPath "//title[@lang='en-us']"  # lang属性值为en-us
Select-Xml -Xml $bs -XPath "book[price<30]"
# 轴（Axes）。常用的XPath轴有：ancestor, descendant, parnet, child, namespace
# preceding（当前节点的开始标签之前的所有节点）, following（当前节点的开始标签之前的所有节点）
Select-Xml -Xml $bs -XPath "child::book"  # 子节点中的book节点

# 补充说明：用PowerShell访问XML节点
echo $bs.node
$bs.node.OuterXML > title.txt
```

## 文档类型定义

文档类型定义（Document Type Definition，DTD）用于定义文档结构。它可以用来描述文档格式，或者方便保持文档结构一致。它可以包装在`DOCTYPE`声明中，也可以封装在外部文件中并通过`DOCTYPE`声明引用

```xml
<?xml version="1.0"?>
<!DOCTYPE note [
    <!ELEMENT note (heading,body)>
    <!ELEMENT heading (#PCDATA)>
    <!ELEMENT body (#PCDATA)>
]>
<!-- 以上DTD声明文档中note元素包含heading和body两个子元素，且子元素数据类型都是#PCDATA -->
<note>
    <heading>Reminder</heading>
    <body>Don't forget me this weekend</body>
</note>
```

DTD也可以定义XML实体，即自定义的转义字符。下面例子使用了内部实体`int`和外部实体`ext`。解析外部实体可能导致安全问题，应避免使用

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ANY [
    <!ENTITY int "entity-value" >
    <!Entity ext SYSTEM "file://test.txt">
]>
<entity>
    <internal>&int;</internal>
    <external>&ext;</external>
</entity>
```

# CSS

CSS（层叠样式表，Cascading Style Sheets）定义了HTML样式。它由若干条规则构成，“层叠”指多个规则可以叠加起来对同一个元素生效

```css
p {
    color: red;
}
```

例子中，`p`是选择器，选定了这条规则的作用范围；`color: red`是属性以及值。应用这条规则之后，所有`<p>`元素的`color`属性都被改为红色

## CSS选择器

**简单选择器**

```css
/*元素选择器。选中所有<p>元素*/
p {color: red;}

/*id选择器。选中id属性为main的元素，如<h1 id="main">*/
#main {color: blue;}

/*类选择器。选中class属性为main的元素，如<h2 class="main">*/
.main {color: green;}
```

**属性选择器**

```css
/*具有role属性的元素*/
[role] {color: olive}

/*role属性值为navigation的元素*/
[role="navigation"] {color: purple;}
```

属性选择器有许多变体，语法是将`[attribute="value"]`中的等号替换为其他运算符

| 符号 | 例子           | 说明                 | 例子                        |
| ---- | -------------- | -------------------- | --------------------------- |
| `~=` | `[role~=navi]` | 属性包含独立词navi   | `<div role="navi">`         |
| `|=` | `[role|=navi]` | 属性开头是独立词navi | `<div role="navi sidebar">` |
| `^=` | `[role^=navi]` | 属性开头是navi       | `<div role="navigation">`   |
| `$=` | `[role$=navi]` | 属性结尾是navi       | `<div role="panavi">`       |
| `*=` | `[role*=navi]` | 属性包含navi         | `<div role="panavim">`      |

前两个的“独立词”指用空格、横线分割开的完整词，比如`p[lang~=en]`能匹配到`<p lang="en-us">`、`<p lang="en Zh">`，但是匹配不到`<p lang="enable">`

**组合器**

```css
/*后代选择器。<div>元素内的所有<p>元素*/
div p {background-color: white;}

/*子选择器。<div>子元素中的所有<p>元素*/
div > p {background-color: silver;}

/*相邻兄弟选择器。紧随<div>之后的<p>元素*/
div + p {background-color: gray;}

/*通用兄弟选择器。与<div>同级的所有<p>元素*/
div ~ p {background-color: black;}
```

**伪类、伪元素**

```css
/*伪类（pseudo-class）选择器：选择特殊状态的元素*/
a:visited {color: #FF0000;}
a:hover {color: #00FF00;}
p:first {color: blue;}

/*伪元素（pseudo-element）选择器：选择元素的指定部分*/
p::first-line {font-variant: small-caps;}
p::first-letter {font-size: 200%;}
div::text {background: white;}
```

## 使用样式表

```html
<head>
    <!-- 外部样式表 external style sheet -->
    <link rel="stylesheet" type="text/css" href="mystyle.css">

    <!-- 内部样式表 internal style sheet -->
    <style>
        hr {color:sienna;}
        p {margin-left:20px;}
        body {background-image:url("images/back40.gif");}
    </style>
</head>

<body>
    <!-- 内联样式 inline style -->
    <p style="color:sienna;margin-left:20px">这是一个段落。</p>
</body>
```

当样式重复定义时，冲突属性取最后定义的

## 布局

### 尺寸

HTML元素尺寸称作“盒子模型”，包括四部分

- **Margin（外边距 / 边距）**：边框外的留空。这部分不算HTMl元素自身
- **Border（边框）**：边框
- **Padding（内边距 / 填充）**：边框内的留空。这部分算作HTML元素
- **Content（内容）**：HTML元素内容

### flex布局

设置`display: flex;`的元素称作flex容器，flex容器以及其中的元素按从上到下或者从左到右排列。比如多个`flex-direction: row;`的元素在同一行从左到右排列；多个`flex-direction: column`的元素，每个元素另起一行

```html
<div class="box">
    <div class="one">One</div>
    <div class="two">Two</div>
    <div class="three">Three</div>
</div>
```

```css
/* Flex容器 */
.box {
    display: flex;
    flex-direction: row;     /* 主轴方向。row为排成一行，column为一列 */
    flex-wrap: wrap;         /* 是否换行。nowrap不换行，wrap则换行 */
    justify-content: center  /* 主轴方向如何排布，有stretch, flex-start, flex-end, center等 */
    align-items: center;     /* 垂直主轴方向如何排布 */
}

/* 容器内的元素 */
.one {
    flex-basis: 100px;    /* 主轴方向尺寸 */
    flex-grow: 1;         /* 拉伸元素时的权重 */
    flex-shrink: 1;       /* 缩小元素时的权重 */
}
/* 缩写形式。三个参数是grow, shrink, basis */
.two {
    flex: 2 auto 100px;
}
```

### grid布局

设置`display: grid;`的元素使用网格布局。网格布局将页面划分为若干网格，定义这些区域的大小、位置等关系。和flex布局相比，flex布局是按照轴线方向摆放元素，grid则是在二维行列上摆放。网格较为复杂，但是更容易控制布局

```html
<div class="wrapper">
    <div class="header">Example Page</div>
    <div class="sidebar">Options</div>
    <div class="content">Hello, World!</div>
    <div class="footer">About</div>
</div>
```

```css
.wrapper {
    display: grid;
    grid-template-columns: repeat(2, 1fr);  /* 2列，每列宽1fr */
    grid-template-rows: 50px 1fr 50px;      /* 三行，高度分别是50px，1fr，50px */
    grid-gap: 10px 5px;       /* 格子间距。可用grid-row-gap和grid-column-gap分别设置 */
    grid-auto-flow: row;      /* 自动填充顺序 */
    justify-items: center;    /* 水平对齐。start, end, center, stretch */
    align-items: start;       /* 垂直对齐 */
    justify-content: center;  /* 内容在容器里的水平对齐。除前几种外还有space-around, between, evenly */
    grid-auto-rows: 1fr;      /* 生成新行时的行高 */
}

.header {
    grid-row-start: 1;
    grid-row-end: 2;     /* 占据第一行 */
    grid-column: 1 / 3;  /* 第一、第二列 */
    z-index: 0;
}
```

`fr`（fraction）是按照权重分配的长度单位。如果两列的宽度分别是`1fr`和`2fr`，则后者宽度是前者两倍。`fr`可以与常规单位混用，也可以用`minmax(100px, 1fr)`这样的方式限定不小于`100px`、不大于`1fr`

### 其他布局

**float属性**：将一个元素设置成`float`之后，它就“浮动”起来，其他元素绕开它，类似Microsoft Word将图片设置成文字环绕

- `left`：将元素浮动到左侧
- `right`：将元素浮动到右侧
- `none`：不浮动
- `inherit`：继承父元素的浮动属性

**position属性**：此属性将元素定位到某个特定位置

# JavaScript

JS是20世纪90年代网景公司为了给自家浏览器添加动态网页功能而开发的语言，为了蹭Java的热度起名为JavaScript。1996年，ECMA为JS制定了标准，称为ECMAScript标准，简称ES。此后的JavaScript都可以说是ECMAScript标准的一种实现

目前（2026）的浏览器实现了ES 2015（也叫ES 6）的绝大部分标准，对更新版也有不同程度的实现。若无特殊说明，本笔记的代码都是符合此标准的

[现代JavaScript教程](https://zh.javascript.info/)

## 数据类型与变量

JavaScript是弱类型的动态语言。“动态”指变量不与某个类型绑定，“弱类型”指操作涉及不匹配的类型时，进行隐式类型转换而不抛出错误

```javascript
// 定义变量。var声明全局变量，let声明局部变量，const声明常量（列表、对象建议用const定义）
var GLOBAL_NAME = 'name';
let x = 1;
const arr = ['a', 'b', 'c'];
const obj = {name: 'Joe', sex: 'Male'};

// 获取变量类型。注意typeof是个特殊运算符，不是函数
typeof arr;

// 显式类型转换
x = Number("3.2");   // 转化为数字
x = parseInt(x);     // 转化为整数
x = String("x");     // 转化为字符串
```

### 字符串

```javascript
let text = 'some string';

// 常用属性和方法
text.length;       // 字符串长度
text.slice(0, 2);  // 截取片段。此例子返回前两个字符。可以用负数索引，也可以省略第二个参数
text.charAt(0);    // 获取指定位置字符。也可以用str[0]
text.trim();       // 去除头尾空白
text.split(' ');   // 分割
text.replace('pattern', 'repl');

// 正则表达式。常用修饰：i不区分大小写，g全局匹配，m多行匹配
let pattern = /regexp/gi;
text.includes(pattern);  // 返回是否匹配到（布尔值）
text.match(pattern);     // 返回包含了每个匹配的列表
text.replace(/some/g, 'random');  // 替换

// 反引号字符串（Template Literal，格式化字符串）
let text = `Welcome, ${firstName} ${lastName}!`;
```

### 列表

```javascript
const fruits = ["Banana", "Orange", "Apple", "Mango"];

// 常用方法
fruits.pop();             // 弹出末尾元素
fruits.push("Kiwi");      // 在末尾添加元素
fruits.shift();           // 弹出首个元素
fruits.unshift("Lemon");  // 在开头插入元素
fruits.slice(0, 3);       // 截取第0~第3个元素
fruits.indexOf("Apple");  // 寻找元素位置
fruits.concat(["Lemon", "Kiwi"]);           // 拼接列表
fruits.sort(function(a, b){return a-b});    // 排序

// 高阶函数。约定func接受三个参数：func(value, index, array)
fruits.map(func);     // 将func作用于每个元素，返回其返回值构成的列表
fruits.forEach(func); // 和map一样，只不过没有返回值
fruits.filter(func);  // 用func检查每个元素，返回通过检查（返回值为真）的元素构成的列表
fruits.every(func);   // all(fruits.map(func))
fruits.some(func);    // any(fruits.map(func))
```

## 运算符

算数运算符（`+-*/%`)，赋值运算符（`=, +=, -=, *=, /=, %=`），自增自减（`++, --`），条件（`? :`），比较（`>, <, ==, >=, <=, !=`）和大部分编程语言相同，以下列出独特的运算符

```javascript
a === b;   // 绝对等于，值和类型均相等
a !== b;   // 不绝对等于，值或类型不相等
```

## 控制流

基本和C语言相同。下面列出不同点

```javascript
// for in循环
const person = {fname:"John", lname:"Doe", age:25};
for (let key in person) {
  console.log(key + " " + person[key]);
}

// 可以给代码块加标签，，用break或continue跳出指定的代码块
let x = false;
label:
{
    if (x) break label;
}

// 错误处理
try {
    obj = JSON.parse(json_str)
} catch(err) {
    if (err instanceof SyntaxError) console.log('JSON Syntax Error');
    else throw err;  // 抛出的可以是字符串，对象，甚至别的什么东西
}
```

## 函数

用关键字function声明函数，函数内变量生存期为函数执行期间，作用域为函数内；函数外变量的生存期为网页存续期间，作用域为整个网页

```javascript
// 定义函数
function mult(a, b) {
    return a * b;
}

// 箭头函数（匿名函数）
const f1 = (a, b) => a + b;          // 单行箭头函数。箭头右边表达式即为返回值
const f2 = (a, b) => {return a + b;} // 多行箭头函数。大括号内和普通函数一样书写
```

## 类与对象

```javascript
class TaskManager {
  constructor(name) {    // 构造函数
    this.name = name;
    this.tasks = [];
  }

  addTask(taskName) {    // 方法
    this.tasks.push(taskName);
  }

  static maxTasks() {   // 静态方法
    return 100;
  }

  set name(newName) {   // Setter
    if (newName.length < 3) {
      throw new Error('名称至少需要3个字符');
    }
    this.name = newName;
  }
}

// 使用类构造对象
const manager = new TaskManager('我的任务');

// 直接定义对象
const car = {
    type:"Fiat",
    model:"500",
    create_description: function() {
        this.description = this.type + " " + this.model;
    }
};

// 访问对象
manager.addTask('学习JavaScript');
manager['name'];
car.create_description();
```

**`this`关键字**的值取决于上下文：

- 函数被HTML事件监听器调用时，函数中的`this`是引发事件的网页元素
- 函数被对象调用时，比如前文的`car.create_description`，`this`指对象本身
- 其他时候，取决于运行环境

```javascript
const obj = {
    name: 'example',
    method: function() {
        // 函数中，嵌套定义函数会“隔离”上下文，匿名函数则不会
        function f1() { console.log(this.name); }
        const f2 = () => console.log(this.name);

        f1();  // 嵌套函数隔开了上下文，this是不是obj，打印undefined
        f2();  // 匿名函数没有隔开上下文，this == obj，打印'example'
    },
    on_event: function (e) => {console.log(this.name);}
}

// 事件监听器中，可用函数（匿名与否都可以）隔离上下文
document.body.addEventListener('mouseover', obj.on_event);        // this接收事件的网页元素
document.body.addEventListener('mouseout', (e)=>obj.on_event(e)); // this是obj
```

## 异步与网络请求

```javascript
// 发起请求
let response = await fetch(url, {
    method: "POST",
    headers: {
        Authentication: "Basic YWRtaW46YWRtaW4="
    },
    body: "id=1&page=1"
});

// 处理响应包
alert(response.status);  // 状态码
for (let [key, value] of response.headers) {
  alert(`${key} = ${value}`);  // 响应头
}
// 响应体。两种方法选一个
let text = response.text();
let data = response.json();
let data = response.blob();
```

## 模块

- CommonJS模块：使用`module.exports, require`语句管理
- ES6模块：使用`export, import`语句管理

```javascript
// 示例模块 circle.js
const PI = 3.14;
const area = (r) => PI * r * r;

// 命名导出。模块可以定义多个命名导出，其他模块使用此名称进行导入
export const PI = 3.14;  // 定义同时导出
export { PI, area as circle_area };  // 集中导出。便于统一管理对外接口，还可起别名

// 默认导出。将所有入口打包在一起导出
export default {
    PI,
    area
};

// 在其他模块中导入以上的内容
import { circle_area as ca } from './circle.js';  // 导入命名导出的对象
import * as circle from './circle.js';            // 导入所有对象，并设置命名空间
import circle from './circle.js';                 // 导入默认导出的对象。名字可以任意取
```

## 在网页中使用JS

### 嵌入JS代码

浏览器从上到下解析HTMl，遇到`script`标签就会加载并执行其中的脚本，执行完之后继续解析剩余HTML

一般把Javascript脚本放在Body末尾，这样一来脚本运行时页面元素都已加载完毕，可以用Javascript控制；此外放在底部不会阻塞HTML解析

```html
<body>
    <p id="demo">Javascript Demo</p>
    <button type="button" onclick="func()"> Button </button>

    <!-- 外部脚本 -->
    <script src="myScript.js"></script>

    <!-- 内联脚本 -->
    <script>
        function func() {document.getElementById("demo").innerHTML="Hello";}
    </script>
</body>
```

- `async`：若存在此属性，则此脚本会异步加载、执行（即，浏览器不会直接继续解析HTMl，不会等待此脚本）
- `defer`：包含此属性的脚本会在脚本解析完毕、`DOMContentLoaded`事件之前执行
- `type="module"`：代码被当作ES6模块处理。执行时间同`defer`
- `type="importmap"`：表示代码中包含json格式的导入映射表，如：`<script type="importmap">{"imports":{"vue": "https://unpkg.com/vue@3/dist/vue.esm-browser.js"}}`

### 事件

一般还会将JS代码**绑定到事件**

```html
<!-- HTML硬编码事件 -->
<button onclick="this.innerHTML = Date()"> 获取当前时间 </button>

<script>
    function bgChange(event) {  // 将背景色改为绿色
        event.target.style.backgroundColor = "rgb(100,200,100)";
    }
    // 使用事件监听器绑定
    const btn = document.querySelector("button");
    btn.addEventListener("click", bgChange);    // 绑定处理函数
    btn.removeEventListener("click", bgChange); // 解绑
</script>
```

### HTML DOM

DOM（文档对象模型，Document Object Model）是描述HTML文档的树状结构。JavaScript可以通过操作DOM访问网页元素

```javascript
// 使用id属性获取元素
const elem = document.getElementById("content")

// 用CSS选择器获取网页元素
let element = document.querySelector("div > p");
const elements = document.querySelectorAll("div > p");

// 访问网页元素
element.innerHTML = "Hello"; // 访问元素的内容
element.id = "honey";        // 访问元素Property
```

注意，JS访问的是元素对象的Property，它和HTML标签的Attribute不相同。绝大多数时候两者是同步的，但格式可能不同，比如：字符串的Attribute可能对应布尔值的Property；相对路径的Attribute可能对应绝对路径的Property。也有些例外是不同步的，比如`<input value="Hello">`标签，它的value Attribute是初始值，Property是当前值

用JS操作DOM时通常使用Property，它才是真正显示在页面上的东西。如果确实有访问Attribute的需求，可用`element.getAttribute("attr_name")`

添加、删除网页元素

```javascript
const div1 = document.querySelector("#div1");
const p1 = document.querySelector("#p1");
const p2 = document.querySelector("#p2");

// 插入DOM节点，添加网页元素
const p0 = document.createElement("p");
const p3 = document.createElement("p");
p0.innerHTML = "paragraph 0";
p3.innerHTML = "paragraph 3"
div1.appendChild(p3);      // 插入为div1最后一个子节点
div1.insertBefore(p0, p1); // 插入为p1前一个兄弟节点。注意，只有insertBefore，没有after

// 删除DOM节点，删除网页元素
div1.removeChild(p0);

// 替换网页元素
const p_new = document.createElement("p");
p_new.innerHTML = "new paragraph";
div1.replaceChild(p_new, p1)
```

### 在浏览器中存储数据

**Cookie**是HTTP协议中用来管理会话的字段，通常由服务器管理，但未设置`HttpOnly`的Cookie也可以用Javascript操作

```javascript
// 读取Cookie。读到的是包含键、值等信息的字符串
alert(document.cookie);
document.cookie = "user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT";
```

**`localStorage`和`sessionStorage`**是Javascript存储数据的主要手段。同源（域名、协议、端口相同的网站）共享数据。`localstorage`不会自动清空；`sessionStorage`在浏览器关闭时清空。这两个存储对象的键值对都只能是字符串

```javascript
localStorage.setItem("app_name", "applet-7ff2");
localStorage.getItem("app_name");
localStorage.removeItem("app_name");
localStorage.clear();

for(let i = 0; i < localStorage.length; i++) {
  let key = localStorage.key(i);  // 获取第 i 个键
  alert(`${key}: ${localStorage.getItem(key)}`);
}
```

**IndexedDB**：浏览器内建数据库，功能很强大，但复杂度较高，不适合一般网页使用。可配合ServiceWorkers等技术构建离线应用

# JS前端

Javascript原生的DOM API用起来不太方便。不同浏览器对Javascript的支持不同，修改HTML元素（包括内容、样式、行为）需要大量代码，并且页面行为复杂时可维护性非常糟糕。前端框架通过封装原生DOM，提供更易用的接口以及控制模式来解决此问题

框架发展大致经过两个阶段

- 加强版DOM：以jQuery为代表，它提供了简洁的DOM API
- 状态管理架构：此类架构舍弃了手动编辑DOM，使用组件化 + 状态管理的方式控制页面的外观与行为。此类框架的代表有AngularJS、React、Vue.js

快速判断网页使用了什么框架 / 库：

```javascript
console.log({
  React: !!window.React,         // React 检测
  Vue: !!window.Vue,             // Vue 2
  Vue3: !!window.Vue?.version,   // Vue 3+
  Angular: !!window.ng,          // AngularJS/Angular
  jQuery: !!window.jQuery,       // jQuery
  lodash: !!window._,            // Lodash
});
```

注：库和框架的区别：库是工具，可以自由调用；框架是半成品，必须遵守已有模式并把剩下部分补全。两者并非泾渭分明，本节并未严格区分

## jQuery

jQuery于2006年发布，它解决了跨浏览器兼容问题，并提供了方便的DOM API，还提供了AJAX和许多有用的插件。其核心是jQuery对象和选择器。jQuery对象是DOM对象的包装，在DOM的基础上提供了更丰富的方法，选择器`$`则是通过DOM对象或者CSS选择器获取对应jQuery对象的函数

```javascript
// 使用选择器访问jQuery对象。注意，选择器$是函数而非特殊符号。JavaScript允许用$作为变量名
$("p:first");  // 返回首个<p>标签的jQuery对象
```

## Vue

### 基础

Vue开发中，通常使用单文件组件（Single-File Component，SFC，即`.vue`文件）封装所有代码，将HTML、JS、CSS分别封装在`<template>, <script>, <style>`块中；编写完成后，需要用构建工具打包为标准的JS和CSS

```vue
<script setup>
    import { ref } from 'vue';
    const count = ref(0);
</script>

<template>
    <button v-on:click="count++">
        Count is: {{ count }}
    </button>
</template>

<style>
    .red {color: red;}
</style>
```

- 声明式渲染：template部分使用扩展的HTMl语法，如双大括号渲染页面；`v-bind`指令绑定HTML元素属性（因为最常用，也可省略，简写为类似`:id`的形式）；`v-on`指令绑定事件监听（可以简写为`@click`的形式）
- 响应性：JS变量更改时，页面内容也会随之更改

也可以不进行编译。这种情况下，需要用带有构建工具的完整版本，例如`vue.global.js`、`vue.esm-browser.js`，不可以用`runtime`版本

备注：这两个完整版本区别

- `vue.global.js`：通用模块，在普通`<script>`标签内用`const { createApp } = Vue`加载，全局作用域
- `vue.esm-browser.js`：ESM模块，在`<script type="module">`标签中用`import`语句加载

```html
<div id="app">{{ message }}</div>

<script type="module">
  import { createApp, ref } from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js'

  createApp({
    setup() {
      const message = ref('Hello Vue!')
      return {
        message
      }
    }
  }).mount('#app')
</script>
```

### API风格

**选项式（Options）API**：用包含data、methods、mounted等选项的对象描述组件逻辑

```vue
<script>
export default {
    // data()返回响应式状态，可以用this.count访问
    data() {
        return {count: 0}
    },
    // methods中包含更改网页状态的函数，常绑定到事件处理
    methods: {
        increment() {this.count ++}
    }
    //生命周期钩子，特定时候被调用，例如挂载完成后调用mounted
    mounted() {
        console.log(`Initial count is ${this.count}`);
    }
}
</script>
```

**组合式（Composition）API**：使用`<script setup>`块导入API函数，并描述组件逻辑

```vue
<script setup>
import { ref, onMounted } from 'vue'

// 响应式状态
const count = ref(0)
// 用来修改状态、触发更新的函数
function increment() {
    count.value++
}
// 生命周期钩子
onMounted(() => {
  console.log(`The initial count is ${count.value}.`)
})
</script>
```

两种API功能相同；选项式更符合面向对象的风格，组合式则更加自由。对于简单应用，建议使用选项式；若打算做复杂的单页应用，建议使用组合式

## JS加密库

JSEncrypt - RSA加密

cryptoJS - 待补充

# JS后端

## Node.js

[Node.js](https://nodejs.org/en/download)是服务端的JavaScript运行环境，可以用来建设服务器，也常用作JavaScript开发平台

```bash
node      # 运行交互式解释器
npm init  # 创建项目。其核心是package.json文件，包括了项目名称、依赖、入口等信息
```

**npm**是Node.js默认的包管理器

```bash
npm -v
npm search $module   # 查找可安装模块

# 本地安装。安装在 ./node_modules 目录，给当前项目使用
npm install $module
npm list               # 查看已安装模块
npm update $module     # 更新
npm uninstall $module  # 卸载

# 全局安装。安装在/usr/local/bin，%AppData%/npm，或者Node.js安装目录，常用于安装命令行工具
npm install --global $module
npm list -g   # 指令和本地安装相同，只是多了 -g 参数

# 运行已安装的模块
npx $module
```

安装后，可以用`import`语句导入模块，或用`require`语句导入（前者导入ES6模块，后者是CommonJS模块。目前ES6是最通用的，CommonJS逐渐被淘汰）

```javascript
import path from 'path';
const app = require('app.js');   // 不建议使用。也不建议两种导入混用
```

## Express

Express.js是一个简洁的Web应用后端框架

安装：`npm install express`

```javascript
import express from 'express';

const app = express();

// 首页托管。以下配置会将public目录映射到网页根目录
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
app.use(express.static(path.join(__dirname, 'public')));

// 添加路由
app.get('/hello', (req, res) => {
    let name = req.query.name || 'World';
    res.send(`Hello, ${name}`);
})
app.get('/user/:id/:type?', (req, res) => {
    res.json({id: req.params.id});
});
app.post('/login', (req, res) => {
    res.json(req.body.password === 'default_pass');
})

// 静态资源
app.use('/static', express.static(path.join(__dirname, 'static')));

// 启动服务器
const PORT = 8081
const server = app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
})
```

### 路由

路由表示如何根据请求的URL进行响应

```javascript
app.get('/hello', handler);
```

当服务器接收到访问`/hello`的GET请求时，会调用`handler`（请求处理函数，`(req, res) => {}`）进行处理。示例：

```javascript
app.get('/user/:id/:type?', handler);
```



```javascript
const router = express.Router();

// 绑定路由
router.get('/query', query_handler);
router.post('/upload', upload_handler);

// 中间件
router.use(middleware);

app.use('/api', router);
```

## 请求处理

```javascript
function handler(req, res, next) {
    const ip = req.ip || req.socket.remoteAddress;
    if (ip === '127.0.0.1') {
        return next()
    }
    res.status(403).send('Access denied')
}
```





## Webpack

Webpack是基于Node.js的前端打包工具，可以将繁杂的前端资源（HTML、CSS、JS、图片、字体等）打包为浏览器可以高效加载的资源，还可辅助管理依赖关系

**安装Webpack**：Webpack分为`webpack`（核心）、`webpack-cli`（命令行界面）两个模组。以下示例用`-g`参数全局安装，也可以用`--save-dev`参数安装为开发阶段依赖

```bash
npm install -g webpack
npm install -g webpack-cli
```

**配置与打包**：配置文件`webpack.config.js`定义了打包的入口、出口以及构建过程

```javascript
const path = require('path');
module.exports = {
    entry: "./src/index.js"  // 入口文件。webpack会分析其依赖一并打包
    output: {
        filename: 'main-[contenthash:8].js',  // 出口文件，即打包结果
        path: path.resolve(__dirname, ''),
        clean: true
    },
    mode: 'none'
};
```

然后用`npx webpack`指令打包（如果不写配置文件，也可用`npx webpack app.js -o bundle.js`简单打包）

# 其他

## 转义

### URI

- 未保留字符（字母、数字、下划线、句点等）：不需转义
- 分界符（冒号，斜杠，问号，等号，`@`等）：作为分隔符时不需转义，作为路径或者参数的一部分时需要转义
- 其他特殊字符（空格，百分号，中文等）：需要转义

使用**百分号编码转义**，如空格的UTF-8编码为`0x20`，转义为`%20`；“我”的UTF-8编码为`0xe68891`，转义为`%e6%88%91`。常用以下两个javascript函数

```javascript
let url = encodeURI('https://example.com/下载');      // 保留分界符，转义其他特殊字符，常用于转义URL
let param = encodeURIComponent('/asset/example.txt'); // 转义分界符和其他特殊字符，常用于转义GET参数
let full_uri = url + '?file=' + param;
```

**非标准转义**

- **`application/x-www-form-urlencoded`类型**：由于历史原因，HTML表单使用一种非常相似的编码方案，使用这种方案时会在请求头加上`Content-Type: application/x-www-form-urlencoded`。此方案它将空格转义为`+`，其他和百分号编码相同
- **escape**：用`%uxxxx`表示，其中`xxxx`是四位16进制数，表示字符的Unicode码位值

### HTML

**字符实体引用**（Character Entity Reference）是HTML的转义序列，常用实体有`&lt; &gt; &quot; &amp`，分别表示小于号、大于号、双引号、`&`。原本字符是HTML标签的一部分，转义后视作普通文本。字符也可用Unicode转义，例如“我”的Unicode码位为25105，因此转义为`&#25105;`，称作**字符值引用**（Numeric Character Reference, NCR）

php的HTML转义函数`htmlspecialchars`默认不转义单引号，因此拼接带单引号字符串时可能产生XSS漏洞

## Javascript压缩与混淆

目前主流的前端开发技术大多都会利用Webpack、Rollup等工具进行打包

[javascript-obfuscator](https://github.com/javascript-obfuscator/javascript-obfuscator)
