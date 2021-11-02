```markdown
How to use latex in markdown:

$LaTeX expression$

$$
LaTex Block
$$
```

# 基础



```latex
\frac{a}{b}     % 分数
a^b_c, {}_1^2\!a_{1}^{2}        % 上下标
\sqrt{2}, \sqrt[n]{2}           % 根号
y^\prime        % 求导

\cdot           % 点乘
\times          % 叉乘
\div            % 除以
```

# 字母上下的符号

```latex
\vec{a}         % 向量
\dot{a}         % 点
\ddot{a}        % 两点
\hat{a} or \widehat{a}          % 帽
\bar{a} or \overline{a}         % 横线
\tilde{a} or \widetilde{F}      % 波浪线
```

# 微积分

```latex
\mathrm{d}     % 微分
\partial       % 偏微分
\nabla         % 哈密顿算符

\sum_{k=1}^N        % 求和
\sum\limits_{i=1}^{n}
\prod_{k=1}^N       % 求积

\int_{-1}^{1} e^x\, dx          % 积分
\iint_{D}^{W} e^x\, dx\, dy     % 二重积分
\oint                           % 回路积分
\lim_{x \to 0}{expression}      % 极限
\infty              % 无穷
```

# 比较

```latex
>, \ge, \geqq, \gg, \ggg        % 大于，大于等于，远大于
<, \leq, \leqq, \ll, \lll       % 小于，etc.
=, \equiv, \dot=                % 等于
\sim, \approx, \simeq, \cong    % 波浪线等于
\not                            % 能与其他任何比较符号复合
\ne, \neq                       % 不等于
\propto                         % 正比于
\pm, \mp                        % 正负负正
```

# 特殊字母

```latex
\eta, \mu               % 小写希腊字母
\Eta, \Mu               % 大写希腊字母
\varepsilon, \varpi     % 异体希腊字母
\mathbb                 % 黑板粗体
\mathbf                 % 正粗体
\mathrm                 % 罗马体
\mathfrak               % 哥特体
\mathcal                % 手写体
\aleph, \beth, \gimel, \daleth  % 希伯来字母
```

# 括号与空格

```latex
\left{, \left[, \left{, \left   % 左括号。右括号同理

% 其他可以配合\left, \right使用的符号：
\langle, \rangle    % 角括号
\left|, \right|     % 单竖线
\|                  % 双竖线
\lfloor, \rfloor    % 向下取整
/, \backslash       % 斜线、反斜线

\quad   % quad空格
\       % 大空格。反斜线+空格
\;      % 中等空格
\,      % 小空格
\!      % 紧贴

\\      %换行
```

# 集合与逻辑

```latex
\subset         % 真包含⊂
\subseteq       % 包含⊆
\supset         % 被包含⊃
\in             % 属于∈
\notin          % 不属于∉
\cap            % 交集∩
\cup            % 并集∪

\forall         % 任意
\exists         % 存在
\varnothing     % 空集

\neg, \lnot     % 非¬
\vee, \lor      % 或∨
\wedge, \land   % 且∧

\Rightarrow，\Leftarrow，\Leftrightarrow    % 充要条件等，首字母小写则变成单箭头
\nRightarrow，\nLeftarrow，\nLeftrightarrow % 非充要条件等
```

# 其他

```latex
\because, \therefore    % 因为所以
\angle                  % 角∠
60^\circ                % 角度°
\pmod{m}, a \bmod b     % 同余
\binom{n}{m}            % 组合数
```

```latex
% 矩阵 (lcr here means left, center or right for each column)
\left[
\begin{array}{lcr}
a11 & a12 & a13 \\
a21 & a22 & a23
\end{array}
\right]

% 另一种矩阵
% 将 matrix 改成 bmatrix、Bmatrix、pmatrix、vmatrix、Vmatrix 分别得不同的矩阵括号
\begin{matrix}
k & u \\
i & n
\end{matrix}

Equations(here \& is the symbol for aligning different rows)
\begin{align}
a+b&=c\\
d&=e+f+g
\end{align}

% 多行公式用align或者aligned对齐（在&处对齐）
\left\{
\begin{aligned}
&a+b=c\\
&d=e+f+g
\end{aligned}
\right.


% 分段函数
f(x)=
\begin{cases}
x+1 & x>0 \\
1-x & x<0
\end{cases}
```