# HTML，CSS与JavaScript

HTML定义了网页的内容，CSS 描述了网页的布局，JavaScript描述网页的行为。较为成熟的开发模式是分别设计HTML、CSS和JavaScript，然后在HTML里面调用另外两者。简单的网页可以把全部东西塞进html里，但考虑可维护性，还是强烈不建议这么做

# HTML

HTML（超文本标记语言，Hyper-Text Markup Language）是用于创建网页的标准标记语言

HTML由多个**元素**（Element）组成。元素由起始标签、元素的内容、终止标签构成，例如`<p>Hello, World</p>`。元素可以没有内容，甚至可以在起始的同时终止（比如，换行标签`<br />`。一些不规范写法将其写成`<br>`，可能会被当作缺少终止标签）

元素常具有**属性**（Attribute），属性用键值对表示，且属性值必须用引号括起来；属性通常写在开始标签。例：`<a href="example.html">链接</a>`

## 基础

```html
<!DOCTYPE html>   <!-- 声明是html5文档。建议用小写标签 -->
<html>            <!-- 根元素 -->
    <head>            <!-- head标签是元数据 -->
        <title>文档标题</title>
        <meta charset="utf-8" />
        <base href="//www.runoob.com/images/" target="_blank" />     <!-- 默认链接 -->
        <link rel="stylesheet" type="text/css" href="mystyle.css" /> <!-- 外部样式 -->
    </head>

    <body>            <!-- body包含了可见的内容 -->

        <h1>一级标题</h1>
        <p>段落</p>
        <a href="http://www.google.com">超文本链接</a>
        <img src="/images/logo.png" width="100%" height="30" />
            <!-- 宽度为页面的100%，高度30像素。会自动拉伸图片，如果宽高只指定一个就能保持宽高比 -->
        <br>  <!-- 换行。源代码中的连续空白、空行都会被当作一个空格 -->
        <hr>  <!-- 分割线 -->

        <p>字体
            <b>粗体(bold)</b>
            <i>斜体(italic)</i>
            <strong>加重，通常也被渲染为粗体</strong>
            <em>着重，常被渲染称斜体</em>
            <sub>下标</sub>
            <sup>上标</sup>
            <del>删除线</del>
        </p>

        <p style="color:blue;margin-left:20px;">
            内联样式。常用样式：
            background-color   背景颜色
            font-family        字体
            color              文字颜色
            font-size          文字尺寸，如20px
            text-align         对齐方式，如center
            在旧版本，有font, center, strike标签，color, bgcolor属性用来实现样式
            现在建议只使用style
        </p>

        <!-- 图像 -->
        <img src="boat.gif" alt="加载不出来的时候显示这段文字" width="304" height="228">

        <!-- 表格 -->
        <table width="500" border="1" cellpadding="10">
            <caption>标题</caption>
            <tr>
                <th colspan="2">Header 1</th>
                <!-- th表示表头，colspan表示跨列（即一个占两列），rowspan表跨行-->
            </tr>
            <tr>
                <td>row 1, cell 1</td>
                <td>row 1, cell 2</td>
            </tr>
            <tr>
                <td>row 2, cell 1</td>
                <td>row 2, cell 2</td>
            </tr>
        </table>

        <li>无序列表</li>
        <ol>
            <li>li套在ol里为有序列表</li>
        </ol>

        <div>
            块级元素，经常当作容器
        </div>
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

## 实体引用

实体引用（Character Entity Reference）相当于HTML的转义字符，格式是`&entity_name;`

| 实体引用        | 显示的字符        |
| --------------- | ----------------- |
| `&lt; &gt;`     | `< >`             |
| `&amp;`         | `&`               |
| `&apos; &quot;` | `' "`             |
| `&#25105;`      | 我（unicode字符） |

# XML

XML（EXtensible Markup Language）是类似HTML的标记语言，但注重传输数据而非显示数据。XML没有预定义标签，标签名对大小写敏感，允许嵌套元素（但必须是严格的嵌套），每个XML文档有且仅有一个根元素

## XML命名空间(XML Namespaces)

`<前缀:标签名 xmlns:前缀="命名空间">`
`<root xmlns:前缀="命名空间">`（在根元素中声明）
一个命名空间被定义后，拥有相同前缀的元素都与该空间相关联
命名空间通常使用对应的url

## XHTML

XHTML是结合了XML和HTML的一种标记语言
语法规则大体与XML相同，功能大体与HTML4相同

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

**其他**

伪类（pseudo-class）选择器：选择特殊状态的元素，比如鼠标悬停、已访问的链接

伪元素（pseudo-element）选择器：选择元素的指定部分，比如首字母、元素之前或之后

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

## 尺寸

HTML元素尺寸称作“盒子模型”，包括四部分

- **Margin（外边距 / 边距）**：边框外的留空。这部分不算HTMl元素自身
- **Border（边框）**：边框
- **Padding（内边距 / 填充）**：边框内的留空。这部分算作HTML元素
- **Content（内容）**：HTML元素内容

## 布局

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

### 数据类型与变量

JavaScript是弱类型的动态语言。动态指变量不与某个类型绑定，弱类型指操作涉及不匹配的类型时，进行隐式类型转换而不抛出错误

JS有7种基本类型 + 1种引用类型，引用类型又可以细分为许多种子类型：

```javascript
// 基本类型
let x;      // Undefined
x = null;   // Null
x = 1.5;    // Number
x = 'Joe';  // String，单引号或者双引号均可
x = true;   // Boolean
x = BigInt("1234567890");   // BigInt
const sym = Symbol("foo");  // Symbol

// 引用类型
const arr = [1, 2, 3];  // 数组
const obj = {name:"John", age:14};  // 对象
const dat = new Date();

// 获取类型。注意typeof是个特殊运算符，不是函数
typeof arr;

// 显式类型转换
x = Number("3.2");   // 转化为数字
x = parseInt(x);     // 转化为整数
x = String("x");     // 字符串
```

**声明变量**

声明变量有若干种方式。建议普通变量用`let`声明，常量和引用类型变量（列表、对象等）用`const`声明

```javascript
let b;  // let声明，作用域为当前block
var c;  // var声明，作用域延伸到当前block之外
const d = 0;  // const声明，不允许再次赋值
```

**字符串**

```javascript
let text = 'some string';
text.replace('pattern', 'repl')

// 常用属性和方法
text.length;       // 字符串长度
text.slice(0, 2);  // 截取片段。此例子返回前两个字符。可以用负数索引，也可以省略第二个参数
text.charAt(0);    // 获取指定位置字符。也可以用str[0]
text.trim();       // 去除头尾空白
text.split(' ');   // 分割

// 正则表达式
// 格式：/表达式内容/[修饰]；常用修饰：i不区分大小写，g全局匹配，m多行匹配
let pattern = /regexp/gi;
text.includes(pattern);  // 返回是否匹配到（布尔值）
text.match(pattern);     // 返回包含了每个匹配的列表
text.search(pattern);    // 返回匹配子串起始位置
text.replace(/some/g, 'random');  // 替换

// Template Literal 格式化字符串。使用反引号
let firstName = "John";
let lastName = "Doe";
let text = `Welcome ${firstName}, ${lastName}!`;
```

**列表**

```javascript
// 定义与访问。注意，用const声明列表
const cars = ["Saab", "Volvo", "BMW"];
console.log(cars[0]);
cars[100] = "Opel";  // 超出范围不会报错，但是3~99全部变成undefined

// 常用方法
const fruits = ["Banana", "Orange", "Apple", "Mango"];
fruits.pop();             // 弹出末尾元素
fruits.push("Kiwi");      // 在末尾添加元素
fruits.shift();           // 弹出首个元素
fruits.unshift("Lemon");  // 在开头插入元素
fruits.slice(0, 3);       // 截取第0~第3个元素
fruits.splice(2, 0, "Lemon", "Kiwi");  // 在2号位置插入Lemon和Kiwi，然后删除0个元素
fruits.concat(["Lemon", "Kiwi"]);      // 拼接列表
fruits.sort(function(a, b){return a-b});
fruits.indexOf("Apple");  // 寻找元素位置

// 使用高阶函数的方法。约定接受三个参数：func(value, index, array)
fruits.map(func);     // 将func作用于每个元素，返回其返回值构成的列表
fruits.filter(func);  // 用func检查每个元素，返回通过检查（返回值为真）的元素构成的列表
fruits.every(func);   // all(fruits.map(func))
fruits.some(func);    // any(fruits.map(func))
```

**对象**

```javascript
// 定义对象
const car = {
    type:"Fiat",
    model:"500",
    color:"white",
    create_description: function() {
        return this.type + " " + this.model;
    }
};

// 访问对象
console.log(car.type);
car["model"] = 404;
```

### 运算符

算数运算符（`+-*/%`)，赋值运算符（`=, +=, -=, *=, /=, %=`），自增自减（`++, --`），条件（`? :`），比较（`>, <, ==, >=, <=, !=`）和大部分编程语言相同，以下列出独特的运算符

```javascript
a === b;   // 绝对等于，值和类型均相等
a !== b;   // 不绝对等于，值或类型不相等
```

### 控制流

```javascript
// if分支
if (time < 10) {
    console.log("Good morning");
} else if (time < 20) {
    console.log("Good day");
} else {
    console.log("Good evening");
}

// switch分支
// switch ... case ... default，同C

// for循环
const fruits = ["Banana", "Orange", "Apple", "Mango"];
let text = "<ul>";
for (let i=0; i<fruits.length; i++) {
    text += "<li>" + fruits[i] + "</li>";
}
text += "</ul>";

// for in循环
const person = {fname:"John", lname:"Doe", age:25};
for (let p in person) {
  console.log(p + " " + person[p]);
}

// while循环，do/while循环
// 略

// break和continue：跳出循环、跳过本次迭代
// 还可以给代码块加标签，跳出指定的代码块
var x = false;
label:
{
    // do something
    if (x) break label;
    // do some other things
}

// 错误处理
try {/*do something*/}
catch(err) {/*发生错误之后执行这段*/}
finally {/*不论有没有捕捉到错误都会运行*/}

//抛出异常
let exception = "Runtime Error";
throw exception;  // 异常可以是字符串、数字、逻辑值或对象
```

### 函数

用关键字function声明函数，函数内变量生存期为函数执行期间，作用域为函数内；函数外变量的生存期为网页存续期间，作用域为整个网页

```javascript
// 定义函数
function func(a, b) {
    return a * b;
}

// 调用函数
let x = func(3, 4);
console.log(x);

// Arrow Function (lambda表达式)
(a, b) => a + b;
```

## 调用

### 代码块

JavaScript以代码块的形式嵌入到html，一般定义在head中或者body的底部。其中的代码在网页加载时会被运行一次，之后还可以事件处理器等方式调用

```html
<head>
    <!-- 使用外部脚本 -->
    <script src="myScript.js"></script>

    <!-- 在head中写脚本 -->
    <script>
        function funcInHead() {document.getElementById("demo").innerHTML="Head";}
    </script>
</head>

<body>
    <p id="demo">Javascript Demo</p>
    <button type="button" onclick="funcInHead()"> Button1 </button>
    <button type="button" onclick="funcInBody()"> Button2 </button>

    <!-- 在body底部写脚本 -->
    <script>
        function funcInBody() {document.getElementById("demo").innerHTML="body";}
    </script>
</body>
```

### 事件

事件是用户的某种动作，比如鼠标点击、按键、调整页面大小等。将JavaScript代码绑定给HTML的事件处理器就能在事件发生时自动调用代码，如：

```html
<button onclick="this.innerHTML = Date()"> 获取当前时间 </button>
```

更常见的做法是不把onclick属性写死在html里面，而是用JavaScript把代码动态绑定到事件处理器。将页面内容与网页行为分离能大大降低开发和维护的难度

```javascript
// 定义事件处理函数
bgChange(event) {
  const rndCol = 'rgb(' + random(255) + ',' + random(255) + ',' + random(255) + ')';
  e.target.style.backgroundColor = rndCol;
}

// 把这个函数绑定到Button
let btn = document.querySelector('button');
// 用属性绑定。这个方法不常用
btn.onclick = bgChange;
// 用事件监听器绑定。可以绑定多个函数
btn.addEventListener('click', bgChange);
btn.removeEventListener('click', bgChange);
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

DOM（文档对象模型，Document Object Model）是描述文档的树状结构。JavaScript可以通过操作DOM访问网页元素。JavaScript提供了丰富的DOM API，使用`document`、`console`等对象就能访问网页内容，如：

```javascript
document.getElementById("demo").innerHTML = "Hello World";
```

此例子将首个id为demo的元素内容更改为Hello World

### 访问网页元素

```javascript
// 获取网页元素
let element = document.querySelector("p.intro");
const elements = document.querySelectorAll("p.intro");

// 访问网页元素
element.innerHTML = "Hello";     // 访问元素的内容
element.name = "honey";          // 访问元素Property
element.hasAttribute("name");    // 访问元素Attribute
element.setAttribute("name", "bee");
element.getAttribute("name");
element.removeAttribute("name");
```

访问网页元素有Property和Attribute两种方式。严格来说，Attribute和Property是不同的东西，Attribute属于HTML，Property属于DOM

绝大多数时候两者是同步的，但格式可能不同，比如：字符串的Attribute可能对应布尔值的Property；相对路径的Attribute可能对应绝对路径的Property。也有些例外是不同步的，比如非标准Attribute不会生成Property，Attribute在老版本IE浏览器有很多奇怪行为

一般建议使用Property，一方面因为更简洁（尤其是布尔值Property），另一方面是在旧版本浏览器上问题较少

### 添加和删除网页元素

假设网页内容如下：

```html
<div id="div1">
    <p id="p1">第1段</p>
    <p id="p2">第2段</p>
</div>
```

通过插入和删除DOM节点的方式添加和删除网页元素

```javascript
var div1 = document.querySelector("#div1");
var p1 = document.querySelector("#p1");
var p2 = document.querySelector("#p2");

// 添加网页元素
var p0 = document.createElement("p");
var p3 = document.createElement("p");
p0.innerHTML = "paragraph 0";
p3.innerHTML = "paragraph 3"
div1.appendChild(p3);      // 插入为div1最后一个子节点
div1.insertBefore(p0, p1); // 插入为p1前一个兄弟节点。注意，只有insertBefore，没有after

// 删除网页元素
div1.removeChild(p0);

// 替换网页元素
var p_new = document.createElement("p");
p_new.innerHTML = "new paragraph";
div1.replaceChild(p_new, p1)
```

# 转义

## URI

### 分类

- 未保留字符（字母、数字、下划线、句点等）：不需转义
- 分界符（冒号，斜杠，问号，等号，`@`等）：作为分隔符时不需转义，作为路径或者参数的一部分时需要转义
- 其他特殊字符（空格，百分号，中文等）：需要转义

### 转义方法

百分号编码，如空格的UTF-8编码为`0x20`，转义为`%20`；“我”的UTF-8编码为`0xe68891`，转义为`%e6%88%91`。常用以下两个javascript函数

- `encodeURI`：转义其他特殊字符，常用于转义完整**URL**
- `encodeURIComponent`：转义分界符和其他特殊字符，常用于**转义GET参数**，如

```javascript
let uri = 'example.com?file=' + encodeURIComponent('/asset/example.txt')
```

### 非标准转义方法

**`application/x-www-form-urlencoded`类型**：由于历史原因，部分表单使用一种非常相似的编码方案，使用这种方案时会在请求头加上`Content-Type: application/x-www-form-urlencoded`。此方案它将空格转义为`+`，其他和百分号编码相同

**escape**：用`%uxxxx`表示，其中`xxxx`是四位16进制数，表示字符的Unicode码位值

## HTML
