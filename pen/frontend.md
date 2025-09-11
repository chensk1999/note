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

DTD也可以定义XML实体，即自定义的转义字符。下面例子使用了内部实体`int`和外部实体`ext`

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

### display属性

这是实现页面布局的主要方法。各元素可以从上到下排列，或者从左到右排列。比如`<a>`默认从左到右排列，连续多个`<a>`元素在同一行；`<li>`元素默认从上到下排列，每个`<li>`元素另起一行

- `inline`：从左到右
- `block`：从上到下
- `flex`：根据`flex-direction`、`align-items`等属性排列子元素
- `grid`：根据`grid-template-columns`等属性排布子元素

**flex布局**

设置`display: flex;`的元素称作flex容器，它的属性决定了容器内子元素的排布

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
    flex-direction: row;  /* 主轴方向。row为排成一行，column为一列 */
    flex-wrap: wrap;      /* 是否“换行”。nowrap不换行，wrap则换行 */
    justify-content: center
        /* 主轴方向如何排布，有stretch, flex-start, flex-end, center, space-around, space-between */
    align-items: center;  /* 垂直主轴方向如何排布，可选值有stretch, flex-start, flex-end, center */
    
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

**grid布局**

网格布局将页面划分为若干网格，定义这些区域的大小、位置等关系。和flex布局相比，flex布局是按照轴线方向摆放元素，grid则是在二维行列上摆放。网格较为复杂，但是更容易控制布局

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

### float属性

将一个元素设置成`float`之后，它就“浮动”起来，其他元素绕开它，类似Microsoft Word将图片设置成文字环绕

- `left`：将元素浮动到左侧
- `right`：将元素浮动到右侧
- `none`：不浮动
- `inherit`：继承父元素的浮动属性

### position属性

此属性将元素定位到某个特定位置

# JavaScript

## 语法

[现代JavaScript教程](https://zh.javascript.info/)

### 数据类型与变量

JavaScript是弱类型的动态语言。动态指变量不与某个类型绑定，弱类型指操作涉及不匹配的类型时，进行隐式类型转换而不抛出错误

JS有7种基本类型 + 1种引用类型，引用类型又可以细分为许多种子类型：

```javascript
// 定义变量。let声明局部变量，const声明常量（列表、对象建议用const定义）
let x = 'name';
const arr = ['a', 'b', 'c'];
const obj = {name: 'Joe', sex: 'Male'};

// 获取变量类型。注意typeof是个特殊运算符，不是函数
typeof arr;

// 显式类型转换
x = Number("3.2");   // 转化为数字
x = parseInt(x);     // 转化为整数
x = String("x");     // 转化为字符串
```

#### 字符串

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

#### 列表

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

### 运算符

算数运算符（`+-*/%`)，赋值运算符（`=, +=, -=, *=, /=, %=`），自增自减（`++, --`），条件（`? :`），比较（`>, <, ==, >=, <=, !=`）和大部分编程语言相同，以下列出独特的运算符

```javascript
a === b;   // 绝对等于，值和类型均相等
a !== b;   // 不绝对等于，值或类型不相等
```

### 控制流

基本和C语言相同。下面列出不同点

```javascript
// for in循环
const person = {fname:"John", lname:"Doe", age:25};
for (let key in person) {
  console.log(key + " " + person[key]);
}

// 可以给代码块加标签，，用break或continue跳出指定的代码块
var x = false;
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

### 函数

用关键字function声明函数，函数内变量生存期为函数执行期间，作用域为函数内；函数外变量的生存期为网页存续期间，作用域为整个网页

```javascript
// 定义函数
function func(a, b) {
    return a * b;
}

// 匿名函数，Arrow Function
(a, b) => a + b;
const f = (a, b) {
    return a + b;
}
```

### 类与对象

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

#### `this`关键字

`this`关键字的值取决于上下文：

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

### 异步

```javascript
```

## 在网页中使用JS

### script标签

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
    
    <!-- 特殊：用a标签调用JS -->
    <a href="javascript:alert(1);">Don't Click</a>
</body>
```



### 事件

事件是用户的某种动作，比如鼠标点击、按键、调整页面大小等。将JavaScript代码绑定给HTML的事件处理器就能在事件发生时自动调用代码，下面的例子定义了一个`button`，点击它时`onclick`属性将被当作JavaScript代码执行。注意，事件处理代码中的`this`指代触发事件的HTML元素

```html
<button onclick="this.innerHTML = Date()"> 获取当前时间 </button>
```

### 事件监听器

```javascript
// 定义事件处理函数
bgChange(event) {
  const rndCol = 'rgb(' + random(255) + ',' + random(255) + ',' + random(255) + ')';
  e.target.style.backgroundColor = rndCol;
}

// 用事件监听器绑定
let btn = document.querySelector('button');
btn.addEventListener('click', bgChange);
btn.removeEventListener('click', bgChange);

// 查看绑定的所有函数
getEventListeners(btn)
```

**常用HTML事件**

| 事件      | 含义                         |
| --------- | ---------------------------- |
| change    | HTML 元素改变                |
| click     | 用户点击 HTML 元素           |
| mouseover | 用户在一个HTML元素上移动鼠标 |
| mouseout  | 用户从一个HTML元素上移开鼠标 |
| keydown   | 用户按下键盘按键             |
| load      | 浏览器已完成页面的加载       |

## HTML DOM

DOM（文档对象模型，Document Object Model）是描述HTML文档的树状结构。JavaScript可以通过操作DOM访问网页元素

### 访问网页元素

```javascript
// 用CSS选择器获取网页元素
let element = document.querySelector("div > p");
const elements = document.querySelectorAll("div > p");

// 访问网页元素
element.innerHTML = "Hello"; // 访问元素的内容
element.id = "honey";        // 访问元素Property
```

注意，JS访问的是元素对象的Property，它和HTML标签的Attribute不相同。绝大多数时候两者是同步的，但格式可能不同，比如：字符串的Attribute可能对应布尔值的Property；相对路径的Attribute可能对应绝对路径的Property。也有些例外是不同步的，比如`<input value="Hello">`标签，它的value Attribute是初始值，Property是当前值

用JS操作DOM时通常使用Property，它才是真正显示在页面上的东西。如果确实有访问Attribute的需求，可用`element.getAttribute("attr_name")`

### 添加、删除网页元素

```javascript
var div1 = document.querySelector("#div1");
var p1 = document.querySelector("#p1");
var p2 = document.querySelector("#p2");

// 插入DOM节点，添加网页元素
var p0 = document.createElement("p");
var p3 = document.createElement("p");
p0.innerHTML = "paragraph 0";
p3.innerHTML = "paragraph 3"
div1.appendChild(p3);      // 插入为div1最后一个子节点
div1.insertBefore(p0, p1); // 插入为p1前一个兄弟节点。注意，只有insertBefore，没有after

// 删除DOM节点，删除网页元素
div1.removeChild(p0);

// 替换网页元素
var p_new = document.createElement("p");
p_new.innerHTML = "new paragraph";
div1.replaceChild(p_new, p1)
```

## 在浏览器中存储数据

### Cookie

Cookie是HTTP协议中用来管理会话的字段，通常由服务器管理，但未设置`HttpOnly`的Cookie也可以用Javascript操作

```javascript
// 读取Cookie。读到的是包含键、值等信息的字符串
alert(document.cookie);
document.cookie = "user=John; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT";
```

### `localStorage`和`sessionStorage`

这两个对象是Javascript存储数据的主要手段。同源（域名、协议、端口相同的网站）共享数据。`localstorage`不会自动清空；`sessionStorage`在浏览器关闭时清空

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

这两个存储对象的键值对都只能是字符串

### IndexedDB

浏览器内建数据库，功能很强大，但复杂度较高，不适合一般网页使用。可配合ServiceWorkers等技术构建离线应用

## 网络请求



```javascript
// 发起请求
let response = await fetch(url, {
    method: "POST",
    headers: {
        Authentication: "Basic YWRtaW46YWRtaW4="
    },
    body: "id=1&page=1"
}
                          );

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



## 框架

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

### jQuery

jQuery于2006年发布，它解决了跨浏览器兼容问题，并提供了方便的DOM API，还提供了AJAX和许多有用的插件。其核心是jQuery对象和选择器。jQuery对象是DOM对象的包装，在DOM的基础上提供了更丰富的方法，选择器`$`则是通过DOM对象或者CSS选择器获取对应jQuery对象的函数

```javascript
// 使用选择器访问jQuery对象。注意，选择器$是函数而非特殊符号。JavaScript允许用$作为变量名
$("p:first");  // 返回首个<p>标签的jQuery对象
```

### Vue



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

## TamperMonkey

```javascript
// @name         保存文件
// @grant        GM_info
// @grant        GM_download
// @run-at       context-menu
// ==/UserScript==

(function() {
    'use strict';

    const elements = document.querySelectorAll("img");
    for (let i=0; i<elements.length; i++) {
        let url = elements[i].getAttribute("src");
        let name = elements[i].getAttribute("name");
        console.log(url + " " + name);

        // 把 url 转为 blobUrl
        if (GM_info.scriptHandler === 'Greasemonkey') {
          const res = fetch(url)
          const blob = res.blob()
          url = URL.createObjectURL(blob)
        }

        // 下载文件
        let download_arg = {
            url: url,
            name: name + ".png"
        };
        const download = GM_download(download_arg);
    }
})();
```

## Javascript压缩与混淆

目前主流的前端开发技术大多都会利用Webpack、Rollup等工具进行打包

[javascript-obfuscator](https://github.com/javascript-obfuscator/javascript-obfuscator)

