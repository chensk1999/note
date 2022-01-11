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
    fprintf('a = 10\n');
elseif a == 20
    fprintf('a = 20\n');
else
    fprintf('a = %d\n', a);
end

% switch分支
key = 'A';
switch key
    case 'A'
        fprintf('A is pressed\n');
    case 'B'
        fprintf('B is pressed\n');
    otherwise
        fprintf('invalid key\n');
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

## 函数句柄

函数句柄（function handle）类似于C的函数指针

```matlab
f = @sin;
g = @(x, n) x .^ n;    % 匿名函数句柄
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
    
    % (optional) 将解析结果赋值给变量
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

```matlab
% 定义
classdef MyClass
    properties
        value {mustBeNumeric}
    end
    
    methods
        function r = roundOff(obj)
            r = round([obj.value], 2);
        end
    end
end

% 使用
a = MyClass
a.value = 3.2
a.roundOff()
```

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
disp(s.a)
```

## 字符与字符串

用单引号括起来的文本字符（char），用双引号括起来的文本是字符串（string）。因为一般不会用matlab做字符处理，不分清楚也没有大碍

```matlab
% 格式化字符串/格式化输出
filename = sprintf('%.2f.csv', 3.2)
fprintf('a = %d\n', 10)

strfind('hello, world', 'o')    % 寻找出现的所有位置
strrep('hello', 'hell', '')     % 将'hello'中的全部'hell'替换为''
strsplit('hello, world', ' ')   % 分割字符串
split('hello, world', ' ')      % 分割字符串。可以用在字符串数组上
strtrim('  hello, world  ')     % 去除开头结尾空白

% 其他一些函数。先在这里列出来，要用再看再补笔记吧
% extractBefore, extractAfter, extractBetween
% regexp, regexpi, regexprep, isspace, symvar
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
clip = importdata('-pastespecial');    % 保存剪贴板内容
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
ax = axes(tab, 'nextplot', 'add');
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

## 其他图形元素

```matlab
% 绘图区初始化和曲线绘制部分如上一节

% 设置曲线标签
line1.DisplayName = 'line 1';
legend(line2, 'line 2');        % 两种方法等同
lgd = legend(ax);               % legend不可用Name+Value（与添加多个标签混淆）设置，但可以设置lgd的属性
legend(ax, 'location', 'north');% 等同于lgd.Location = 'north'
legend(ax, 'boxoff');           % 等同于lgd.Box = 'off'
legend(ax, 'show');             % show, hide, toggle显示/隐藏；'off'删除

% 设置坐标轴范围
[xmin, xmax] = bounds(ax.Children.XData, 'all');
[ymin, ymax] = bounds(ax.Children.YData, 'all');
yspan = ymax - ymin;
ax.XLim = [xmin xmax];
ax.YLim = [ymin - 0.1*yspan, ymax + 0.1*yspan];

% 设置标题和坐标轴标签
% 这些都是axes的属性，可以通过修改ax.Title、ax.GridLineStyle等属性来修改
title(ax, 'title');
xlabel(ax, 'xlabel');
ylabel(ax, 'ylabel');
grid(ax);
```
