本笔记为HTML、XML和CSS笔记。Javascript参考[Javascript笔记](./javascript.md)

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
