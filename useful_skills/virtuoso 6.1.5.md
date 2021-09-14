# 总览

1. 创建Library：略
2. 创建schemetic：打开 Library Manager ，从上方导航栏选择 File - New - Cellview，选择所属Library，填写 Cell 名字，选择 Type（或者填写 View）为schemetic，然后确认创建
3. 编辑原理图：放置器件，连线，创建引脚
4. 创建符号：从导航栏选择 Create - Cellview - From Cellview，填写 To View Name 为 symbol，确认
5. 前仿真
6. 创建 layout：打开 schemetic，选择 Launch - layout

# 原理图

## Schemetic Editor L 快捷键

| Key       | Usage            | Description              |
| --------- | ---------------- | ------------------------ |
| I         | Instance         | 放置器件                 |
| W         | Wire             | 连线                     |
| E         | Descend and Read | 打开下层元件（阅读模式） |
| Shift + E | Descend and Edit | 打开下层元件（编辑模式） |
| Ctrl + E  | Ascend           | 返回上层元件             |
| Q         | Property         | 元件参数                 |

# 前仿真

方法1

1. 准备好想要仿真的元件的 Symbol
2. 创建一个原理图用作测试台（testbench），名字可以加上后缀 _test 之类的。放置待仿真元件并加上信号源（如 analogLib 的 vdc、vpulse 等）、负载，设置其 Property 以提供合适的激励
3. 从导航栏选择 Launch - ADE L （Analog Design Environment）打开仿真菜单。之后操作皆在此菜单进行
4. 选择Analyses - Choose，添加需要仿真的内容
   1. tran：瞬态（transient）仿真，仿真电路行为。记得写 stop time！有 conservative，moderate，liberal三种模式，精度递减，耗时也递减
   2. dc：直流静态工作点仿真。勾选 Save DC Operating Point 可以仿单个工作点，或者选择一个sweep，仿工作点随变量的变化
5. 选择Outputs - To Be Plotted - Select On Schematic，选择输出的变量。选择节点是该处电流，导线是该处电压（为啥啊，常理来想不是应该反过来吗）
6. Simulation - Netlist and Run（或者点击右侧绿色图标）

方法2（简单，但是不够灵活，只能用有限几种标准激励，而且不能带负载）

1. 在元件原理图界面选择 Launch - ADE L 打开仿真菜单
2. 选择Setup - Stimuli，给各个端口提供驱动。驱动可以用变量（比如，将驱动的 DC Voltage 设置为 x，那么进行DC仿真时就可以扫这个参数）
3. 从方法1第四步继续

## 使用Calculator

1. 在 ADE L 或者 Visualization & Analysis XL 选择 Tools - Calculator
2. 在 Calculator 的 Function Panel 编辑要计算的值（需要信号作为变量时，可以切到绘图窗口双击信号 or 右键信号 - calculator 选择。但是不知道为什么有时候双击选不中），然后OK，这个量被加入到 buffer
3. 选择 buffer 界面上面的 evaluate 图标，计算。（然后算式被推入 stack，计算结果到buffer）
4. 可以回到 ADE L 仿真菜单界面，选择 Outputs - Setup，将表达式填入 Expression（可以复制粘贴或者通过 Get Expression 从计算器的缓冲取表达式），此后仿真时会计算这个值

## 仿真中的变量

设计中可以使用变量，比如，将MOS管宽度设置为 W。然后，在 ADE L 界面选择 Variables - Edit（或右键 Design Variables 面板 - Edit）给变量赋值，通过调整变量、仿真、再调整、再仿真，直到找到最佳取值

也可以将仿真的参数设置为变量，例如将控制电压设置为Vctr，然后能方便地调整它并仿真器件在不同控制电压下的性能

## Parametic Analysis

在ADE L 选择 Tools - Parametic Analysis，可以扫变量（一次性仿变量多个取值）。用法很直觉就不写了

在参数分析中温度（temp）也作为一个变量。像温度这样只需要几个特殊值的，可以不写 From To 之类的，直接设置 Inclusion List 为 0 27 85

Run mode - Parametic Set 只仿变量组（比如，v1 的 Value List 为 1 2 3，v2 的 Value List 为 2 4 6，则仿(v1, v2) = (1, 2), (2, 4), (3, 6)三组；如果用 Sweep 模式就会仿 9 组）。但是，Parametic Set 模式的结果用 calculator 算不了

准确的说，用一般的瞬态仿真或 Sweep模式仿出来的结果在 Calculator 中是`v("\net" ?result "tran-tran")`，用 Parametic Set 模式仿的结果是`v("\net" ?result "sweep1_tran-sweep")`，因此需要分别编写算式，即使算的东西是完全相同的

## 其他细节

使用了CMOS库之后要在 Setup - Environment 删除名字里包含 cmos 的几个视图，否则可能出现 no corresponding terminal 的错误

噪声频率 0.01~10G。说是由宝贵的经验定下来的

设置电路初值：ADE - Simulation - Convergence Aids - Initial Condition

# 版图

版图可以用 Layout Editor L 或者 XL，两者差别之一是 XL 可以用 Connectivity - Generate - Selected From Source 选项从原理图直接生成器件。首先点击 Selected From Source，切到 Schemetic Editor，选择若干元件，再切回来就能放置

DRC (Design Rule Check)

LVS (Layout versus Schemetic)

## Layout Editor L 快捷键

- 放置器件、连线

| Key       | Usage         |
| --------- | ------------- |
| I         | **I**nstance  |
| P         | **P**ath      |
| Shift + P | **P**olygon   |
| R         | **R**ectangle |
| O         | Via           |
|           |               |

- 调整

| Key     | Usage                                                        |
| ------- | ------------------------------------------------------------ |
| A       | Quick **A**llign（点击选择一个东西，然后点击要对齐到的位置） |
| S       | **S**tretch                                                  |
| C       | **C**hop                                                     |
| Shift+M | **M**erge（合并两个形状）                                    |

- 显示

| Key             | Usage                                   |
| --------------- | --------------------------------------- |
| F               | Zoom **F**it                            |
| Ctrl+F, Shift+F | 查看/不查看元件内部                     |
| Tab             | Pan（平移视图，移动到鼠标点击处为中心） |
| K, Shift+K      | Draw / Clear Rulers                     |

- 其他

| Key                | Usage                                                 |
| ------------------ | ----------------------------------------------------- |
| F2                 | Save                                                  |
| F3                 | 设置工具属性（比如，P，F3，可以设置Path的宽度等属性） |
| D, Ctrl+D          | **D**eselect / Deselect All                           |
| Ctrl+Y             | 在重叠对象之间切换                                    |
| Backspace          | 撤销上一次点击（可以在画Path过程中用）                |
| N, Shift+N, Ctrl+N | 更改画线的默认方向（斜/水平竖直/自动转弯的水平竖直）  |
| G                  | **G**ravity（自动吸附到边上）                         |
| T                  | Layer **T**ap（切换到点击的层）                       |
| V                  | Attach（比如将Label关联到Pad上）                      |

# 后仿真

1. Layout Editor - Calibre - Run PEX，将结果保存到 Calibre View
2. ADE - Setup - Environment，在 Switch View List 开头加上 calibre
3. 运行仿真

# 其他

电源宽度：1mA - 1um