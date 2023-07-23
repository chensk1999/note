# 交互式命令

```matlab
exp(i*pi/4)     % 计算并立即打印结果
v0 = 10;        % 带分号语句结果不会打印

who             % 查看定义的所有变量
whos            % 查看所有变量及它们的值、类型
exist v0        % 判断变量或文件存在

clear v0        % 删除变量
clear           % 删除所有变量

clc             % 清屏。clear command window
home            % 滚屏，将光标移动到左上

format short    % 更改数字显示格式
                % 可选选项：short, long, short e, long e, bank, +, rat, compact, loose

help [cmd]      % 显示指令帮助
lookfor [cmd]   % 显示指令参数的帮助
quit            % 退出
```

# 语法

## 控制流

```matlab
% if分支
a = 21;
if a == 10
    disp('a = 10\n');
elseif a == 20
    disp('a = 20\n');
else
    disp('a = %d\n', a);
end

% switch分支
key = 'A';
switch key
    case 'A'
        disp('A is pressed\n');
    case 'B'
        disp('B is pressed\n');
    otherwise
        disp('invalid key\n');
end

% while循环
i = 0;
sum = 0;
while i < 100
    sum = sum + i;
    i = i + 1;
end

% for循环
for a = [24,18,17,23,28]
    disp(a)
end

% 可以将for循环用到的数组换成用冒号表达式定义的数组
sum = 0;
for i = 0:100
    sum = sum + i;
end

% break & continue。该是怎样就怎样
```

# 编程

## 脚本

脚本可以包含代码以及局部函数，运行脚本等同于直接在命令行逐行执行代码（即，脚本变量和交互式界面的变量是共通的）

局部函数不能和其他函数文件重名

## 函数

函数放在`.m`文件中，一个文件对应一个函数，且主函数名必须为文件名

### 定义

```matlab
function [x1,x2] = quadratic(a,b,c)
    % 这行注释称作H1行，lookfor命令可查看此行。通常写函数名和函数功能简要描述
    % H1行以及之后紧跟的注释可以用help命令查看。通常写输入输出说明以及调用说明

    d = sqrt(b^2 - 4*a*c);
    x1 = (-b + d) / (2*a);
    x2 = (-b - d) / (2*a);
    % 注意：不用return返回结果。return仅作退出函数用
    % 注意2：如果调用时实参数量<形参数量，仍能调用，缺少的参数在函数体内未定义（反之，实参多于形参则不行）
end

% 同一个文件中定义的其他函数称作子函数，只能在该文件内被调用
function result = cmp(a, b)
    if a > b
        result = a;
    else
        result = b;
    end
end

% 函数句柄(function handle)，类似于其他语言的匿名函数、函数指针
f = @sin;
g = @(x, n) x .^ n;    % 匿名函数句柄
```

### 调用

matlab支持两种调用格式：

```matlab
max(1, 2)      % 正常的调用
max 1 2        % 类似指令的调用。使用此方式，所有参数都被视作char
```

调用时，实参数量可以少于形参；接受返回值的左值数量也可以少于返回值个数

如果实参数量少于形参，缺少的参数在函数体内等同于未定义，如果需要用到缺失的参数，将提示参数个数不足。反之（实参数量多于形参）则报错。进一步地可以在函数体内动态定义这些参数，实现类似于默认参数的效果

如果接收返回值的变量个数少于返回值个数，多出来的返回值被“丢弃”。反之，如果多于返回值个数，报错。

```matlab
function [result, cnt] = my_sum(a, b, c)
    if ~exist(b)        % 使用exist动态定义
        b = 0;
    end
    if nargin() == 2    % 使用nargin动态定义
        c = 0;
    end
    result = a + b + c;
    cnt = nargin();
end

result = my_sum(1, 2);
[result, cnt] = my_sum(32);
```

### 可变长输入输出

`varargin` / `varargout`是特殊的输入参数 / 输出变量，可以获取任意个参数 / 返回任意个值。它们是元胞行向量

```matlab
function varargout = var_io(varargin)
    for i = 1:nargout()
        varargout{i} = varargin{i};
    end
end
```

### 参数解析器

使用参数解析器可实现参数类型检查、可选参数、可选键值对参数

```matlab
function result = parser_example(varargin)
    p = inputParser();
    is_scalar_num = @(x) isnumeric(x) && isscalar(x);

    % 添加参数
    p.addRequired('a', is_scalar_num);     % 参数a，用is_scalar_num检查合法性
    p.addOptional('b', 0, is_scalar_num);  % 可选参数b，默认值0
    p.addParameter('mode', 'rb');          % 可选键值对参数，参数名是mode，默认值是'rb'

    % 解析
    p.parse(varargin{:});
    p.Results    % 包含各参数的struct

    % (not recommended) 将解析结果赋值给变量
    % matlab元编程好像有些奇怪结果，最好不要用eval
    fields = fieldnames(p.Results);
    for i = 1:length(fields)
        field = fields(i);
        eval(sprintf('%s = p.Results.%s;', field, field));
    end
end

% 调用例
parser_example(1);
parser_example(1, 'mode', 'wb');
parser_example(1， 2, 'mode', 'wb');
```

## 类

[类组件](https://ww2.mathworks.cn/help/matlab/matlab_oop/class-components.html)

```matlab
% 定义
classdef MyNum
    properties
        value {mustBeNumeric}
    end

    methods
        function obj = MyNum(val)
            % 构造函数。应该支持无参数语法（即不输入参数也能运行），以便创建默认对象
            if ~exist('val', 'var')
                val = 0;
            end
            obj.value = val;
        end

        function obj = increment(obj)
            obj.value = obj.value + 1;
        end
    end
end

% 使用
a = MyNum
b = MyNum(2)
a.value = 3.2
a.increment()
```

注意：Matlab默认的类是值类，其内容无法更改，对其赋值会创造一个新的对象。比如例子里面的`increment`函数，它会返回一个新的对象，而原来的不变。内建的数组、元胞数组等都是如此

如果想写“正常”的类，需要继承[句柄类](https://ww2.mathworks.cn/help/matlab/matlab_oop/comparing-handle-and-value-classes_zh_CN.html)：

```matlab
classdef MyHandleClass < handle
    % 略
end
```

值类进行比较可以用`==`或者`isequal`。句柄类，`==`比较两者是否是同一个对象，`isequal`比较两者的值是否相等

### 特性

[类特性](https://ww2.mathworks.cn/help/matlab/matlab_oop/class-attributes.html)、[方法特性](https://ww2.mathworks.cn/help/matlab/matlab_oop/method-attributes.html)和[属性特性](https://ww2.mathworks.cn/help/matlab/matlab_oop/property-attributes.html)定义一些特殊行为（比如继承，静态）。例如：

```matlab
classdef (Abstract = true) Example
    properties (Access = protected, Constant = true)
        a = 1;
    end
    methods (Static = true)
        % 略
    end
end
```

### 继承

```matlab
classdef MyPosNum < MyNum   % 继承MyNum类
    methods
        function obj = MyPosNum(value)
            if nargin == 0
                value = 1;
            end
            obj@MyNum(value);   % 调用父类构造函数
        end
    end
end
```



## 工作区

脚本、命令行中的变量储存在基础工作区中，函数则有自己的函数工作区。跨工作区传递数据最好用参数传递，但也有[其他办法](https://ww2.mathworks.cn/help/matlab/matlab_prog/share-data-between-workspaces.html)，比如

```matlab
function increment()
    data = evalin('base', 'data');          % 获取基础工作区数据
    assignin('base', 'data', data + 1);     % 向基础工作区赋值
end
```

这个办法可用做于gui回调函数，但它的风险和`eval`是等同的

# 数据类型

## 数组

Matlab的大多数数据都是数组。数字是零维数组，向量是一维数组，矩阵是二维数组

```matlab
% 定义数组
r = [1 2 3];        % 行向量
c = [1; 2; 3;];     % 列向量
A = [11 12 13; 21 22 23; 31 32 33];  % 矩阵
B = A * 2;

% 特殊数组的定义
zeros(5)        % 五阶零方阵
ones(4, 3)      % 4x3填1的矩阵
eye(4)          % 四阶单位阵
lin = 1:1:10    % initval:step:endval，定义一个包括endval的线性行向量

% 矩阵运算
A + B           % 矩阵加法
A - 1           % 矩阵减法
A * 2           % 数乘
A * B           % 矩阵乘法
A .* B          % 逐元素乘法
A / B           % 矩阵除法，相当于A * inv(B)
A ./ B          % 逐元素相除
A \ B           % 矩阵左除法，相当于pinv(A) * B，或求A*x=B的解
A .\ B          % 逐元素左除法，相当于B ./ A
A ^ 2           % 矩阵乘方
A .^ 2          % 逐元素乘方
A'              % 矩阵转置
A.'             % 转置，但复数不取共轭

% 数组索引：索引从1开始
A(1, 2)         % 第1行第2列
A(2, :)         % 第二行。注意：A(2)是第二行第一个元素
A(1:2, 2:3)     % 1~2行的2~3列
A([3, 1], :)    % 第3行和第1行

% 添加/删除数组元素
[A[0, :], 14]   % 一维矩阵拼接
A(:, 2) = []    % 删除第二列
A(:, :, 2) = A  % 插入到第三维
a = 1, a(5) = 2 % 给标量插入新元素构成向量。未定义部分填0

% 数组大小
size(A)         % 对于标量、向量和矩阵，返回[row col]；对于高维数组，返回各维度的长度
length(A)       % 等于max(size(A))
numel(A)        % 数组包含元素数量，等于prod(size(A))
ndims(A)        % 数组维数

% 拼接矩阵
[M, c]
[M, r]
cat(1, M, r)
cat(2, M, c)

% 其他
[row, col] = find(A==12)      % 寻找元素
[M, I] = max(A);              % 寻找最大元素以及其index
```

## 元胞数组

元胞（Cell Array）是可以包含任意类型数据的容器。1×1元胞数组有时也直接称作元胞

```matlab
% 定义Cell Array
c1 = {1 'A'; 3.5 {2 2} }
c2 = cell(5, 3)         % 5x3的空cell

% 访问Cell Array
c1(1, 1)    % 圆括号访问元胞集，得到{1}
c1{1, 1}    % 花括号访问元胞内容，得到1
```

## 结构体

结构体（struct）是用字段将数据组合在一起的数据结构

```matlab
% 圆点表示法定义。此例子定义的结构体包含a和b两个字段
s.a = 1
s.b = 'value'

% struct函数定义
s = struct('a', 1, 'b', 'value')
s = struct()    % 定义没有字段的结构体

% 访问结构体
s.a = 2
s.('b')         % 用字符串访问

isfield(s, 'a');    % 判断field是否存在
```

结构体数组

```matlab
s = struct('a', 1, 'b', 'value');
s_arr = [s, s, s];

% 批量访问
[s_arr.a] = deal(1, 2, 3);
```

## 表

```matlab
tb = table();
tb.a = [1; 2; 3];              % 添加一列
tb.b = ["abc"; "def"; "ghi"];  % 再添加一列（必须和现有的列高度相同）

if ismember("a", tb.Properties.VariableNames)
    % 判断列是否存在
    tb.a(1) = 0;
end
```

## 字符与字符串

用单引号括起来的文本字符（char），用双引号括起来的文本是字符串（string）。注意两者不同，比如`'abc' ~- "abc"`，需要用`strcmp`函数。字符串用起来更方便

```matlab
% 格式化字符串/格式化输出
filename = sprintf('%.2f.csv', 3.2)
fprintf('a = %d\n', 10)

strfind('hello, world', 'o')    % 寻找出现的所有位置
strrep('hello', 'hell', '')     % 将'hello'中的全部'hell'替换为''
strsplit('hello, world', ' ')   % 分割字符串
split('hello, world', ' ')      % 分割字符串。可以用在字符串数组上
strtrim('  hello, world  ')     % 去除开头结尾空白

% 正则表达式
regexp("ababaab", "a+b", "match");

% 其他一些函数。先在这里列出来，要用再看再补笔记吧
% extractBefore, extractAfter, extractBetween
% regexp, regexpi, regexprep, isspace, symvar
```

因为字符被当作字符数组，进行遍历操作的时候可以用元胞数组

```matlab
files = {'1.csv', '2.csv', '3.csv'};
data = {};
for i = 1:length(files)
    file = files{i};
    data{i} = importdata(file, ',', 1);
```

文本字符和字符串的区别

```matlab
'abc' + 'def'    % 数组求和，[197, 199, 201]
"abc" + "def"    % 字符串拼接，"abcdef"
```

# 文件操作

```matlab
fprintf('a = %d', 1);
disp([1 2 3]);

% 保存数据。会自动覆盖同名文件
save('workspace.mat')           % 保存工作区所有变量
save('data.mat', data)          % 保存指定的变量
dlmwrite('data.txt', M, ',')    % 保存ascii delimited file

% 读取文件。大部分文件（比如excel表、csv、空格/逗号分隔的文本文件）都能自动解析成好用的形式
data1 = load('workspace.mat');
data2 = importdata('example.jpeg');
data3 = importdata('example.csv', ',', 1); % 分隔符是','，第1行是文件头
clip = importdata('-pastespecial');        % 保存剪贴板内容。注意windows剪贴板有长度限制
% 一般load适合读取.mat文件或纯数字数据，importdata适合读有行列名的文本文件
```

TODO:其他的函数：fopen+fread+fclose

# 绘图

常见的matlab的绘图教程都不喜欢显式使用`figure`和`axes`，这么做写起来虽然方便，但读起来、改起来就很痛苦了。而且画的图一复杂就搞不清到底哪个图是活跃的，代码容易乱成一坨。

我会用尽量明确的写法，能面向对象的就面向对象，这样就能很容易弄清楚自己在操作图的那些部分

```matlab
% 产生一些数据
x = 0:0.1:10;
y1 = sin(x);
y2 = y1 .* exp(-x);

% 简单绘图。这也是大部分教程的写法，但我从下一节开始将不再用这个方法
hold on;        % 将活跃的axes设为hold状态。如果没有此句，每绘制一条线就会覆盖上一条
plot(x, y1);    % 执行之后立即绘制并显示
plot(x, y2);
```

## 初始化绘图区域

```matlab
fig = figure();
tabgroup = uitabgroup(fig);
tab1 = uitab(tabgroup, 'title', 'TAB 1');
ax = axes(tab1, 'nextplot', 'add');
% 如果只画一张图，应跳过uitab，直接axes(fig)
% 以上每个初始化都可以在参数加任意组属性名&值指定属性。属性名不区分大小写
% 例子中只有tab的标题和ax的NextPlot被指定

% 更改绘图区域格式。在命令行看fig和ax的属性能列出全部可设置格式
ax.FontName = 'Arial';
ax.FontSize = 8;
ax.GridLineStyle = '--';

% 定义子图，其编号是从左到右从上到下
% ╔═════╦═════╗
% ║  1  ║  2  ║
% ╟═════╬═════╢
% ║  3  ║  4  ║
% ╟═════╬═════╢
% ║  5  ║  6  ║
% ╚═════╩═════╝
tab2 = uitab(tabgroup, 'title', 'TAB 2');
ax1 = subplot(3, 2, 1, 'parent', tab2);     % 不用tab时用fig做parent
ax2 = subplot(3, 2, [2 4 6], 'parent', tab2);
ax3 = subplot(3, 2, [3 5], 'parent', tab2);
```

另外，matlab还提供了`uifigure`和`uiaxes`，ui类据说比较合适用于嵌入到应用程序中

## 绘制曲线

```matlab
% 产生一些数据
x = 0:0.1:10;
y1 = sin(x);
y2 = y1 .* exp(-x);

% 初始化绘图区域
fig = figure();
ax = axes(fig, 'nextplot', 'add');

% 绘图
line1 = plot(ax, x, y1, '--ok');            % 用LineSpec字符串指定格式
line2 = plot(ax, x, y2, 'linewidth', 0.3);  % 用Name+Value指定格式

% 更改曲线格式。在命令行看line的属性能列出全部可设置格式
line1.LineWidth = 0.3;
line1.Color = [0 0.4470 0.7410];
line2.Color = '#D95319';            % 三元数组和颜色字符串都可以
```

LineSpec字符串可用于方便地设置线型、点型和颜色：

| 种类 | 符号                         | 说明                                                         |
| ---- | ---------------------------- | ------------------------------------------------------------ |
| 线型 | `-`, `--`, `:`, `-.`, `none` | 实线、虚线、点、点划线、无线                                 |
| 点型 | `o+*.x_|`, `^v<>`, `sdph`    | 和符号相同、不同朝向的三角形、Square、Diamond、Pentagon、Hexagon |
| 颜色 | rgb, cmyk, w                 | 不用解释了吧。总之都不是好看的颜色                           |

例子：`--^k`表示虚线、朝上的三角标记、黑色

绘图函数

| 函数名 | 说明       | 备注                     |
| ------ | ---------- | ------------------------ |
| plot   | 绘制曲线   |                          |
| stairs | 阶梯状曲线 | 适合绘制幅度会跳变的信号 |
| stem   | 针状图     | 适合绘制离散序列         |



## 其他图形元素

```matlab
% 绘图区初始化和曲线绘制部分如上一节

% 设置曲线标签
line1 = plot(x, y, 'DisplayName', 'line 1');  % 设置标签
line1.DisplayName = 'line 1';   % 同上
legend(line2, 'line 2');        % 设置并且显示。但是会把其他的legend隐藏掉
lgd = legend(ax);               % 显示标签。properties(lgd)可查看标签可设置的属性
legend(ax, 'location', 'north');% 等同于lgd.Location = 'north'。其他位置还有'NorthEast'等
legend(ax, 'boxoff');           % 等同于lgd.Box = 'off'
legend(ax, 'show');             % show, hide, toggle显示/隐藏；'off'删除

% 设置坐标轴范围
xlim(ax, [0, inf]);             % 坐标下限为0，上限自动选择
ylim(ax, 'tight');              % 坐标范围紧贴数据范围
ylim(ax, 'padded');             % 坐标范围贴合数据，并留出一点边距
xlim(ax, 'manual');             % 设置为手动模式，继续绘图时坐标范围不会自动改变
% 手动设置
[ymin, ymax] = bounds(ax.Children.YData, 'all');
yspan = ymax - ymin;
ax.YLim = [ymin - 0.1*yspan, ymax + 0.1*yspan];

% 坐标轴刻度

% log scale
set(ax, 'XScale', 'log')

% 设置标题和坐标轴标签
% 这些都是axes的属性，可以通过修改ax.Title、ax.GridLineStyle等属性来修改
% 或者用set函数更改
title(ax, 'title');
xlabel(ax, 'xlabel');
ylabel(ax, 'ylabel');
set(ax, 'TickLabelInterpreter', 'latex');

# grid
grid(ax);
```

# GUI

```matlab
fig = figure();
g = uigridlayout(fig);

% 绘图区域
ax1 = uiaxes(g, 'nextplot', 'add');
ax.Layout.Row = 1;
ax.Layout.Column = [1, 2];

% 滑块
sld = uislider(g, 'Limits', [1, 5]);
sld.Layout.Row = 2, sld.Layout.Column - 1;
sld.ValueChangedFcn = @(obj, e) callback(obj, e, ax);
% sld.ValueChangingFcn = ...
% changing在拖动滑块过程中也会调用（此时sld.Value仍未改变，必须用event.Value）
% changed只有滑块移动结束，松开鼠标之后才会调用

% 滑块移动的回调函数
function callback(obj, event, ax)
    cla(ax);
    t = linspace(0, pi, 100);
    plot(ax, t, sin(event.Value * t));
end
```

# Simulink

Simulink是基于模型的设计工具，可以作为Matlab的附加功能安装

# 数字滤波器

需要Signal Processing Toolbox

## 数字滤波器设计

- 窗函数法：传统方法，滤波效果一般不如后面两种最优化方法
- 等波纹：让滤波器频率响应逼近目标，并且让波纹（理想与实际之差）均匀分布在通带和阻带，优点是波纹均匀分布，最大误差比较小。常用Parks-McClellan算法，对应`firpm`函数
- 最小二乘：让滤波器频率响应逼近目标，并让总平方误差最小。一般通带和阻带内部响应比等波纹的平坦，但边缘波动稍大。对应`firls`函数

例1：用Parks-McClellan算法设计切比雪夫FIR滤波器，实现CIC滤波器的补偿滤波

```matlab
% 求目标频率响应
N = 2;
fb = 0.25;   % passband
f = linspace(0, fb, 40);
H = sinc(f*N) ./ sinc(f);  % CIC滤波器频率响应
a = 1 ./ abs(H);           % 目标频率响应。补偿passband droop

% 设计滤波器
order = 4;
[b err] = firpm(order, f, a);
% f和a是目标频率以及该频率的增益。其长度必须为偶数，两两一组表示一个频带；不同频带之间为过渡带

% 进行滤波
a = 1;      % 滤波器函数的分母项。对于FIR滤波器a=1
filter(b, a, vin)
```

## 数字滤波器分析

```matlab
[b, a] = butter(3, 0.2, 'low');    % 巴特沃斯低通滤波器

% 使用系统模型（Control System Toolbox）
ts = 1;
sys = tf(b, a, ts);
stepplot(sys);        % 单位冲激响应

% 使用Signal Processing Toolbox
[h, w] = freqz(b, a, 512);
plot(w/pi, abs(h));
legend('幅频响应');
```

# 其他

```matlab
% 取整
x = 1.5;
floor(x)     % 向下取整
ceil(x)      % 向上取整
round(x)     % 四舍五入取整
fix(x)       % 向0取整

% 保存命令行输出
diary("matlab.log");
diary off
```

