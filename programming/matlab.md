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

help [cmd]      % 显示指令帮助
lookfor [cmd]   % 显示指令参数的帮助
quit            % 退出
```

# 控制流

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

# 函数

```matlab
% 函数应该放在一个.m文件中，一个文件对应一个函数
% 主函数名必须为文件名
function [x1,x2] = quadratic(a,b,c)
    % 二次方程求根
    % 函数声明之后立即跟着的注释会被当做文档，被help打印出来
    d = sqrt(b^2 - 4*a*c);
    x1 = (-b + d) / (2*a);
    x2 = (-b - d) / (2*a);
    % 注意：不用return返回结果。它仅作退出函数用
end      % 函数结束的end。没有在函数体内定义函数时可以省略

% 同一个文件中定义的其他函数（第一个之外的函数）称作子函数，只能在该文件内被调用
function result = cmp(a, b)
    if a > b
        result = a;
    else
        result = b;
    end
end
```

```matlab
% 匿名函数
power = @(x, n) x .^ n
result = power(7, 3)
```



# 矩阵与向量

```matlab
% 定义矩阵/向量
A = [11 12 13; 21 22 23; 31 32 33];
B = A * 2;
r = [1 2 3];    % 行向量，只有一行的矩阵
c = [1; 2; 3;]; % 列向量

% 特殊矩阵/向量的定义
zeros(5)        % 五阶零方阵
ones(4, 3)      % 4x3填1的矩阵
eye(4)          % 四阶单位阵
lin = 1:1:10    % initval:step:endval，定义一个包括endval的线性行向量


% 矩阵运算
A + B           % 矩阵加法
A - 1           % 逐元素运算
A * 2           % 数乘
A * B           % 矩阵乘法
A .* B          % 逐元素乘法
A / B           % 矩阵除法，相当于A * inv(B)
A ./ B          % 逐元素相除
A \ B           % 矩阵左除法，相当于inv(A) * B。相当于求A*x=B的解
A .\ B          % 逐元素左除法，相当于B ./ A
A ^ 2           % 矩阵乘方
A .^ 2          % 逐元素乘方
A'              % 矩阵转置
A.'             % 转置，但复数不取共轭

% 矩阵索引：索引从1开始
A(1, 2)         % 第1行第2列
A(2, :)         % 第二行。注意：A(2)是第二行第一个元素
A(1:2, 2:3)     % 1~2行的2~3列
A([3, 1], :)    % 第3行和第1行

# 添加/删除矩阵元素
[A[0, :], 14]   % 一维矩阵拼接
A(:, 2) = []    % 删除第二列
A(:, :, 2) = A  % 插入到第三维
a = 1, a(5) = 2 % 给标量插入新元素构成向量。未定义部分填0

% 拼接矩阵
cat(1, M, r)
cat(2, M, c)
```

# Cell Array

大致相当于指针数组，或者numpy中类型为Object的数组，每个元素可以指向任意一种对象

```matlab
% 定义Cell Array
c1 = {1 'A'; 3.5 {2 2} }
c2 = cell(5, 3)         % 5x3的空cell
```

# 字符串

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

# IO

```matlab
format short    % 更改数字显示格式
                % 可选选项：short, long, short e, long e, bank, +, rat, compact, loose

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
ax1 = subplot(2, 2, 1, 'parent', tab2);     % 不用tab时用fig做parent
ax2 = subplot(2, 2, [2 4 6], 'parent', tab2);
ax3 = subplot(2, 2, [3 5], 'parent', tab2);
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

