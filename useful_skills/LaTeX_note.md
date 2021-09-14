```latex
$LaTeX expression$
```

# 基础

```latex
分数		\frac{a}{b}
乘方/上标	a^b
下标		a_b
根号		\sqrt{2}, \sqrt[n]{2}
一撇(求导)	\prime, 如y^\prime
复合上下标举例	{}_1^2\!a_{1}^{2}

点乘		\cdot
叉乘		\times
除以		\div
```

# 字母上下的符号

```latex
向量		\vec{a}
帽		\hat{a} or \widehat{a}
点		\dot{a}
两点		\ddot{a}
横线		\bar{a} or \overline{a}
波浪线		\tilde{a} or \widetilde{F}
```

# 微积分

```latex
微分		\mathrm{d}
偏微分		\partial
哈密顿算符	\nabla

求和		\sum\limits_{i=1}^{n}
		\sum_{k=1}^N
求积		\prod, 其余同sum
积分		\int_{-1}^{1} e^x\, dx
二重积分	\iint_{D}^{W} e^x\, dx\, dy
回路积分	\oint
极限		\lim_{x \to 0}{expression}
无穷		\infty
```

# 比较

```latex
>, \ge, \geqq, \gg, \ggg       %大于，大于等于，远大于
<, \leq, \leqq, \ll, \lll      %小于，etc.
=, \equiv, \dot=               %等于
\sim, \approx, \simeq, \cong   %波浪线等于
\not                           %能与其他任何比较符号复合
\ne, \neq                      %不等于
\propto                        %正比于
\pm, \mp                       %正负负正
```

# 字体

```latex
希腊字母	\eta, \mu, etc.
异体希腊字母	\varepsilon, \varpi, etc.
黑板粗体   \mathbb
正粗体		\mathbf
罗马体		\mathrm
哥特体		\mathfrak
手写体		\mathcal
希伯来字母	\aleph, \beth, \gimel, \daleth
```

# 括号，空格

```latex
左括号		\left{, \left[, \left{, \left
右括号同理
其他可以配合\left, \right使用的符号：
角括号		\langle, \rangle
单竖线		\left|, \right|
双竖线		\|
向下取整	\lfloor, \rfloor
斜线、反斜线	/, \backslash

quad空格	\quad
大空格		\ , 即反斜线+空格
中等空格	\;
小空格		\,
紧贴		\!
```

# 集合与逻辑

```latex
\subset         %真包含⊂
\subseteq       %包含⊆
\supset         %被包含⊃
\in             %属于∈
\notin          %不属于∉
\cap            %交集∩
\cup            %并集∪

\forall         %任意
\exists         %存在
\varnothing     %空集

\neg, \lnot     %非¬
\vee, \lor      %或∨
\wedge, \land   %且∧

\Rightarrow，\Leftarrow，\Leftrightarrow    %充要条件等，首字母小写则变成单箭头
\nRightarrow，\nLeftarrow，\nLeftrightarrow %不是充要条件等
```

# 其他

```latex
因为所以	\because, \therefore
角∠		\angle
角度°		60^\operatorname{\omicron}, 60^\circ
同余		\pmod{m}, a \bmod b
\binom{n}{m}        %组合数
```

```latex
%Matrix (lcr here means left, center or right for each column)
\left[
\begin{array}{lcr}
a11 & a12 & a13 \\
a21 & a22 & a23
\end{array}
\right]

%另一种矩阵
%将 matrix 改成 bmatrix、Bmatrix、pmatrix、vmatrix、Vmatrix 分别得不同的矩阵括号
\begin{matrix}
k & u \\
i & n
\end{matrix}

Equations(here \& is the symbol for aligning different rows)
\begin{align}
a+b&=c\\
d&=e+f+g
\end{align}

%多行公式用aligned对齐（在&处对齐，在\\处换行）
\[
\left\{
\begin{aligned}
&a+b=c\\
&d=e+f+g
\end{aligned}
\right.
\]

%分段函数
f(x)=
\begin{cases}
x+1 & x>0 \\
1-x & x<0
\end{cases}
```
