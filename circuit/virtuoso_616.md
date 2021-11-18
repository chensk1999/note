# 总览

1. 创建Library：CIW - File - New - Library，输入要创建的库名，选择Attach to an existing techfile，选择要用的工艺库（如果不链接到工艺库，版图设计时无工艺层）
2. 创建schemetic：打开 Library Manager ，从上方导航栏选择 File - New - Cellview，选择所属Library，填写 Cell 名字，选择 Type（或者填写 View）为schemetic，然后确认创建
3. 编辑原理图：放置器件，连线，创建引脚
4. 创建符号：从导航栏选择 Create - Cellview - From Cellview，填写 To View Name 为 symbol，确认
5. 前仿真
6. 创建 layout：打开 schemetic，选择 Launch - layout

# 原理图

1. 打开 Library Manager，File - New - Cellview（注意这个窗口默认会在后台打开。检查一下任务栏），选择所属Library，填写 Cell 名字，选择 Type（或者填写 View）为schemetic，然后确认创建
2. 编辑原理图：放置器件，连线，创建端口
3. 创建符号：从导航栏选择 Create - Cellview - From Cellview，填写 To View Name 为 symbol，确认

## Schemetic Editor L 快捷键

### 增

| Key  | Usage    | Description |
| ---- | -------- | ----------- |
| I    | Instance | 放置器件    |
| W    | Wire     | 连线        |
| L    | Label    | 线网标签    |
| P    | Pin      | 端口        |

### 改

| Key           | Usage            | Description                                                  |
| ------------- | ---------------- | ------------------------------------------------------------ |
| Q             | Property         | 元件参数                                                     |
| C             | Copy             | 复制                                                         |
| M             | Move             | 移动                                                         |
| R             | Rotate           | 旋转。在移动/放置器件时按R旋转，Shift+R左右翻转，Ctrl+R上下翻转 |
| U, Shift+U    | Undo, Redo       | 撤销上一步操作                                               |

### 查
| Key           | Usage            | Description                                                  |
| ------------- | ---------------- | ------------------------------------------------------------ |
| E             | Descend and Read | 打开下层元件（阅读模式）                                     |
| Shift + E     | Descend and Edit | 打开下层元件（编辑模式）                                     |
| Ctrl + E      | Ascend           | 返回上层元件                                                 |
| F             | Zoom Fit         | 缩放至适合窗口大小                                           |
| 鼠标左键+拖动 |                  | 区域选择                                                     |
| 鼠标右键+拖动 |                  | 放大选中区域                                                 |


## 其他细节

将器件名（Instance Name）改成如`I0<5:0>`的形式就能放多个器件。同理，信号名也可以用如`VOUT<5:0>`的形式。假设要将这6个器件连成环，可以将输出写为`VOUT<5:0>`，输入写为`VOUT<0>,VOUT<5:1>`。其他接法也类似，用逗号隔开。不能有空格

创建文字注解：Create - Note - Text（或者Shift+N）

右键 - Annotations 或 View - Annotations：显示/隐藏哪些参数。有一些要进行相应仿真之后才能显示

Edit - Renumber Instances：重新编号

Options - Select Filter 或 Ctrl + F 或 工具栏几个有鼠标的图标：调整可以选中的东西。如果设置错误，可能导致无法选中器件/线网等

# 前仿真

## 流程

方法1：testbench

1. 准备好想要仿真的元件的 Symbol
2. 创建一个原理图用作测试台（testbench），名字可以加上后缀 _test 之类的。放置待仿真元件并加上驱动、负载。驱动和负载要尽量与电路实际工作时相同，可以使用实际器件，也可以使用analogLib库的理想器件，甚至可以自己写Verilog-A。analogLib常用元件：gnd, vdc, vpulse等
3. 从导航栏选择 Launch - ADE L （Analog Design Environment）打开仿真菜单。之后操作皆在此菜单进行
4. 在Design Variables一栏右键，按需编辑变量。原理图的全部变量都要有一个数值
5. 选择Analyses - Choose，添加需要仿真的内容（或者右侧有AC，DC等文字的图标）
   1. tran：瞬态（transient）仿真，仿真电路行为。记得写 stop time！有 conservative，moderate，liberal三种模式，精度递减，耗时也递减
   2. dc：直流静态工作点仿真。勾选 Save DC Operating Point 可以仿单个工作点，或者选择一个sweep，仿工作点随变量的变化
6. 选择Outputs - To Be Plotted - Select On Schematic，选择输出的变量。选择节点是该处电流，导线是该处电压
7. Simulation - Netlist and Run（或者点击右侧绿色图标）
8. Session - Save State（或者Toolbar的保存图标），推荐保存为Cellview

方法2：在端口提供激励（简单，但是只能用标准激励，而且不能带负载。这样仿出来和实际工作状态不同，尽量不要用）

1. 在元件原理图界面选择 Launch - ADE L 打开仿真菜单
2. 选择Setup - Stimuli，给各个端口提供驱动。驱动可以用变量（比如，将驱动的 DC Voltage 设置为 x，那么进行DC仿真时就可以扫这个参数）
3. 从方法1第四步继续

## 变量与表达式

- 设计变量：将MOS管宽度设置为 W。然后，在 ADE L 界面选择 Variables - Edit（或右键 Design Variables 面板 - Edit）给变量赋值，通过调整变量并仿真，直到找到最佳取值
- 仿真参数：将控制电压设置为vctr，然后能方便地调整它并仿真器件在不同控制电压下的性能
- 仿真结果：设置Outputs的值为`cross(VT("/VOUT") 0.9 1 "falling")`，仿真后会直接输出它的值

使用Calculator编辑表达式：

1. 在 ADE L 或者 Visualization & Analysis XL 选择 Tools - Calculator
2. 在 Calculator 的 Function Panel 编辑要计算的值（需要信号作为变量时，可以点击Schematic Selection Toolbar - 切换到原理图点击对应信号。Sechematic Selection Toolbar是有vt、vf、vdc等很多选项的菜单，鼠标悬停可看各种类的含义。如果没有View - Schematic Selection Toolbar显示），然后OK，这个量被加入到 buffer
3. 选择 buffer 界面上面的 evaluate 图标，计算。（然后算式被推入 stack，计算结果到buffer）
4. 可以回到 ADE L 仿真菜单界面，选择 Outputs - Setup，将表达式填入 Expression（复制粘贴或者点击 Get Expression 从计算器的缓冲取表达式），此后仿真时会计算这个值

## Parametic Analysis

在ADE L 选择 Tools - Parametic Analysis，可以扫变量（一次性仿变量多个取值）。用法很直觉就不写了

在参数分析中温度（temp）也作为一个变量。像温度这样只需要几个特殊值的，可以不写 From To 之类的，直接设置 Inclusion List 为 0 27 85

Run mode - Parametic Set 只仿变量组（比如，v1 的 Value List 为 1 2 3，v2 的 Value List 为 2 4 6，则仿(v1, v2) = (1, 2), (2, 4), (3, 6)三组；如果用 Sweep 模式就会仿 9 组）。但是，Parametic Set 模式的结果用 calculator 算不了

准确的说，用一般的瞬态仿真或 Sweep模式仿出来的结果在 Calculator 中是`v("\net" ?result "tran-tran")`，用 Parametic Set 模式仿的结果是`v("\net" ?result "sweep1_tran-sweep")`，因此需要分别编写算式，即使算的东西是完全相同的

## 工艺角仿真

ADE-L - Setup - Model Libraries - 选择想要仿真的工艺角，然后运行仿真

## 蒙特卡罗仿真

ADE-XL

## 显示仿真结果

绘制Outputs：Results - Plot Outputs - 仿真类型

仿真结束之后还想添加其他信号：Results - Direct Plot - Main Form，设置好之后**不要关掉Direct Plot Form窗口**，鼠标选择要绘制的信号（有的变量不会保存，这种情况Direct Plot报错。加入Outputs中能绘制，但可能导致仿真时间变长）

显示MOS管参数：选择DC仿真，选中Save DC Operating Point，仿真结束之后Results - Print - DC Operating Point可以打印静态参数

静态工作点：DC仿真，Results - Annotate - DC Operating Points，然后点击信号

## 其他细节

使用了CMOS库之后要在 Setup - Environment 删除名字里包含 cmos 的几个视图，否则可能出现 no corresponding terminal 的错误

噪声频率 0.01~10G。说是由宝贵的经验定下来的

设置电路初值：ADE - Simulation - Convergence Aids - Initial Condition

# 版图

版图可以用 Layout Editor L 或者 XL，两者差别之一是 XL 可以用 Connectivity - Generate - Selected From Source 选项从原理图直接生成器件。首先点击 Selected From Source，切到 Schemetic Editor，选择若干元件，再切回来就能放置

## Layout Editor L 快捷键

- 放置器件、连线

| Key       | Usage         |
| --------- | ------------- |
| I         | **I**nstance  |
| P         | **P**ath      |
| Shift + P | **P**olygon   |
| R         | **R**ectangle |
| O         | Via           |

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

## DRC (Design Rule Check)

待补充

## LVS (Layout versus Schemetic)

待补充

# 后仿真

1. Layout Editor - Calibre - Run PEX，将结果保存到 Calibre View
2. ADE - Setup - Environment，在 Switch View List 开头加上 calibre
3. 运行仿真

# 其他

电源宽度：1mA - 1um