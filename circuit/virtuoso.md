# 总览

Virtuoso是Cadence公司的EDA软件。本笔记记录用Virtuoso进行模拟设计的流程，以及一些使用技巧

**启动virtuoso**

```bash
ssh -X c01n01  # 连接计算节点。实验室服务器有c01n01 ~ c01n05一共五个节点
. bash616      # 初始化环境变量的脚本
virtuoso &
```

**设计流程**

```mermaid
graph LR
    A(原理图设计)
    B(前仿真)
    C(版图设计)
    D(验证)
    E(后仿真)

    A --> B --> C --> D --> E
```

其中，每一步如果不通过 / 不满足指标就要回到之前步骤修改

**操作流程**

1. 创建Library：CIW - File - New - Library，输入要创建的库名，选择Attach to an existing techfile，选择要用的工艺库（如果不链接到工艺库，版图设计时无工艺层）
2. 创建schemetic：打开 Library Manager ，从上方导航栏选择 File - New - Cellview，选择所属Library，填写 Cell 名字，选择要创建的 Type，然后确认创建
3. 编辑原理图
4. 创建符号：从Schematic L导航栏选择 Create - Cellview - From Cellview，填写 To View Name 为 symbol，确认
5. 前仿真
6. 创建 layout：打开 schemetic，选择 Launch - layout
6. 验证与后仿真

# 原理图

## 流程

1. 打开 Library Manager，File - New - Cellview（注意这个窗口默认会在后台打开。检查一下任务栏），选择所属Library，填写 Cell 名字，选择 Type（或者填写 View）为schemetic，然后确认创建
2. 编辑原理图：放置器件，连线，创建端口
3. 创建符号：从导航栏选择 Create - Cellview - From Cellview，填写 To View Name 为 symbol，确认
4. 编辑符号：符号中只有pin（红色小方块以及端口名）是有电气属性的，绿色的线只是外观。`@partName`会显示为cell名称（比如BUF），`@instanceName`显示为元件名（比如U0）

## Schemetic Editor快捷键

**增**

| Key  | Usage    | Description |
| ---- | -------- | ----------- |
| I    | Instance | 放置器件    |
| W    | Wire     | 连线        |
| L    | Label    | 线网标签    |
| P    | Pin      | 端口        |

**改**

| Key           | Usage            | Description                                                  |
| ------------- | ---------------- | ------------------------------------------------------------ |
| Q             | Property         | 元件参数                                                     |
| C             | Copy             | 复制                                                         |
| M             | Move             | 移动                                                         |
| R             | Rotate           | 旋转。在移动/放置器件时按R旋转，Shift+R左右翻转，Ctrl+R上下翻转 |
| U, Shift+U    | Undo, Redo       | 撤销上一步操作                                               |

**看**

| Key       | Usage            | Description              |
| --------- | ---------------- | ------------------------ |
| E         | Descend and Read | 打开下层元件（阅读模式） |
| Shift + E | Descend and Edit | 打开下层元件（编辑模式） |
| Ctrl + E  | Ascend           | 返回上层元件             |
| F         | Zoom Fit         | 缩放至适合窗口大小       |

**其他**

- Shift+左键：多选
- Ctrl+左键：取消选择
- Ctrl+拖动：移动物体，移动时切断连接
- 左键+拖动：区域选择
- 右键+拖动：放大到选中区域

## 其他

**总线**

Vector：`DATA<0:7>`表示8位向量，`I0<0:5>`表示6个器件。向量索引：`DATA<low:up:increment> = DATA<0:7:2>`，`DATA<0,2,4,6>`（两种索引含义相同。注意逗号后没有空格）

Bundle：组合多根线，比如`A,B,C`

用重复运算符`<*n>`扩展标量：`<*2>A,B = A,A,B`，`A,<*2>(B,C) = A,B,C,B,C`，括号可以嵌套，比如`<*2>(A,<*2>(B,C))`

用重复运算符`<*n>`扩展向量：`A<0*2> = A<0,0>`，`A<0:2*2> = A<0,0,1,1,2,2>`，`A<(0:2)*2> = A<0,1,2,0,1,2>`

**参数化电路**

将电路参数设置为型如`pPar("var")`的方式，就能在调用的时候设置参数值。在设计行为级电路模型的时候很有用，但是实际电路一般不这么干（因为参数化电路的设计难度远大于设计的必要性。需要参数化版图pCell）

添加或者删除了参数之后，需要用CIW - tools - CDF将参数加到cell里面（或者生成symbol也会自动添加。但是删除必须用CDF）。使用CDF时，layer要选择base，否则修改不会保存到cell里面。CDF还能设置默认参数值等信息

**杂项**

创建文字注解：Create - Note - Text（或者Shift+N）

右键 - Annotations 或 View - Annotations：显示/隐藏哪些参数。有一些要进行相应仿真之后才能显示

Edit - Renumber Instances：重新编号

Options - Select Filter 或 Ctrl + F 或 工具栏几个有鼠标的图标：调整可以选中的东西。如果设置错误，可能导致无法选中器件/线网等

# 版图

## 显示设置

Options-Display - Grid Controls，建议将Type调成None，并且需要将X / Y Snap Spacing调整为对应工艺的值。对于180nm，两者为0.005

## Layout Editor快捷键

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
| Shift+C | **C**hop（点击选择对象，然后选择要切掉的部分）               |
| Shift+M | **M**erge（合并两个形状）                                    |

- 显示

| Key             | Usage                                   |
| --------------- | --------------------------------------- |
| F               | Zoom **F**it                            |
| Ctrl+F, Shift+F | 查看/不查看元件内部                     |
| Tab             | Pan（平移视图，移动到鼠标点击处为中心） |
| K, Shift+K      | Draw / Clear Rulers                     |

- 其他

| Key                 | Usage                                                        |
| ------------------- | ------------------------------------------------------------ |
| F2                  | 保存                                                         |
| F3                  | 设置工具属性（比如，P，F3，可以设置Path的宽度等属性；C，F3，可以批量复制） |
| F4                  | Partial Select / Full Select                                 |
| D, Ctrl+D           | **D**eselect / Deselect All                                  |
| Ctrl+Y              | 在重叠对象之间切换                                           |
| Backspace           | 撤销上一次点击（可以在画Path过程中用）                       |
| N, Shift+N, Ctrl+N  | 更改画线的默认方向（斜/水平竖直/自动转弯的水平竖直）         |
| G                   | **G**ravity（自动吸附到边上）                                |
| T                   | Layer **T**ap（切换到点击的层）                              |
| V                   | Attach（比如将Label关联到Pad上）                             |
| X, Shift+X, Shift+B | Edit in place, Descend edit, Ascend                          |

## 其他

从原理图生成器件：Connectivity - Generate - Selected From Source，切到原理图选择元件。注意Layout Editor L没有此功能，需要用XL

导出gds2格式版图：File - Export - stream；导入版图：File - Import - Stream，选择Stream File和Library、Technology Library即可。注意导入时可能建立很多个cellview，最好导入到新的库（在Library填库名即可，不需手动建库）

电源轨宽度：1 mA (rms) = 1um（Electric migration，是金属层承载电流的上限）、IR drop（电源电压下降 = 峰值电流I × 走线电阻R）

180工艺：过孔电阻 ≈ 10Ω/via，金属层电阻 ≈ 0.1Ω/sq，相邻金属层电容 ≈ 0.05fF/um2

一般建议布线距离在DRC要求的1.3~1.4倍以上，否则对良品率稍有影响

# 验证

验证与寄生参数提取使用Mentor Graphics的Calibre软件进行。它并不是Cadence的一部分，需要用skill脚本加载，通常写进`.cdsinit`文件自动加载。加载成功后在Layout Editor菜单出现Calibre子菜单

## DRC

DRC（Design Rule Check)检查布局布线是否违反设计规则（常见违例有走线太近、天线效应等）

底层模块需要保证没有密度之外的错误；当前密度可以在Check Density_PRINT看

## LVS

LVS (Layout versus Schemetic)检查原理图和版图是否一致
- 网表：Rules - LVS Run Directory文件夹下的Inputs - Netlist - Spice Files文件
- 忽略器件：LVS Options - Gates
- 黑箱子：LVS Options - Include - 勾选Include Rule Statements，在输入框加入`LVS BOX <cell name>`：把cell当成黑箱子

## PEX

PEX (Parasitic Extraction)：提取寄生参数用于后仿真
- 抽参数可能出现找不到library的错，原因是library在`cds.lib`和`lib.defs`两个文件中都有定义，而`lib.defs`文件没有更新。可以手动修改，或者Tools - Library Path Editor
- 黑箱子：Inputs - Blocks，只勾选要抽取的Cell，然后Outputs - Extraction Type选ADMS（Analog-Digital Mixed Signal）

## RVE

RVE（Result Viewing Environment）是查看寄生参数的工具

- 完成PEX之后选择Start RVE，可以看各个Net的寄生电容、Pin与Pin之间的寄生电阻。注意打开的是最近一次PEX抽出来的参数

# 仿真

仿真主要工具是ADE L和ADE XL（ADE：Analog Design Environment）。ADE L和XL是软件界面，底层的仿真器是相同的（老服务器默认都是Spectre。也可以手动加载别的仿真器，比如数模混仿用AMS。新一代仿真器Spectre X据说在不牺牲精度的同时速度还比Spectre快好几倍）

## 流程

**testbench**

1. 准备好想要仿真的元件的 Symbol
2. 创建一个原理图用作测试台（testbench），可以命名为`<待仿真元件名>_test` 之类的
3. 放置待仿真元件，并加上驱动、负载。驱动和负载要尽量与电路实际工作时相同，可以使用实际器件，也可以使用理想器件，还可以自己写Verilog-A。常用理想器件有analogLib的gnd、vdc、vpulse、vcvs；ahdlLib

也可以在端口提供激励，这样就不需要testbench。这种方法简单，但是只能用标准激励，而且不能带负载，仿出来和实际工作状态不同，尽量不要用。使用方法：ADE L - Setup - Stimuli，给各个端口提供驱动

**ADE L**

1. Schematic导航栏 - Launch - ADE L，打开仿真菜单。之后操作皆在此菜单进行
2. Analyses - Choose（或者右侧有AC，DC等文字的图标），编辑需要仿真的内容。详见仿真种类一节
3. Outputs - To Be Plotted - Select On Schematic，然后回到原理图点选要输出的信号；或者直接在Outputs面板编辑
4. Simulation - Netlist and Run（或者点击右侧绿色图标）
5. Session - Save State（或者Toolbar的保存图标），推荐保存为Cellview

**ADE XL**

XL功能比L强大很多，但用起来比较复杂。这一节仅介绍最基础用法

1. Schematic导航栏 - Launch - ADE XL
2. Tests - Click to add test，打开Test Editor，其界面与编辑方式均和ADE L相同，也可以Load State加载ADE L的状态
3. Run SImulation

## 仿真种类

### 一般

- tran：瞬态（transient）仿真，仿真电路行为
- dc：直流静态工作点仿真。建议勾选 Save DC Operating Point。Sweep Variable可以仿静态工作点随变量的变化
- ac：交流仿真

### 周期

**pss**：周期稳态（Periodic Steady-State）仿真，仿真周期性电路的工作点

- Engine：Shooting通过瞬态仿真求解，Harmonic Balance在频域求解。有高次谐波（比如方波）而且关注时域波形的电路shooting精度更高；高Q值电路Harmonic Balance精度更高
- Fundamental Tones - Beat Frequency / Beat Period是各个频率的最大公因子（比如，一个PLL输入时钟是800 MHz，输出是300 MHz，Beat Frequency就是100MHz）
- Output Harmonics：计算的谐波数量。注意，是相对于Beat Frequency的谐波。不影响精度，但影响仿真时间。需要看几次谐波就填几，不关注谐波时可以填0
- Additional Time for Stabilization (tstab) 是电路达到稳态需要的时间，一般填周期10倍以上

**pac**：周期交流（Periodic AC）仿真

**pnoise**：周期噪声（Periodic Noise）仿真。必须先跑PSS仿真求得静态工作点才能跑

- Output Frequency Sweep Range：计算噪声的频率范围
- Sidebands：计算多少个sideband，比如设置maximum sideband = 10，就会计算1~10次谐波附近的噪声。可以取PSS仿真降低40 dB的谐波作为maximum sideband，然后增加sideband数量，直到噪声结果不变
- Reference Side-Band：输入与输出频率的变化，没有变化时填0。这项设置应该是给混频器等电路用的
- 查看仿真结果：1. Results - DIrect Plot（注意：和tran的direct plot不同，不需要点选信号，而是直接点击GUI的Plot）；2. Results - Print - Noise Summary。Noise Summary中的类型有fn MOS管闪烁噪声，id MOS管热噪声，rd 电阻热噪声等
  - Output Noise，Input Noise：输入输出参考噪声
  - Noise Figure：简称NF，$NF = SNR_i / SNR_o$，其中$SNR_i$和$SNR_o$是输入输出的信噪比
  - Noise Factor：简称F，$F = 10 \cdot log_{10}(NF)$


### 仿真设置

在Choosing Analysis界面右下的Options可以进行更多设置

**Algorithm**

- Convergence Parameters
  - cmin：若电路中有浮空节点，可能导致“Zero diagonal found in Jacobian”；设置cmin = 1f（在每个节点加上1fF的寄生电容）一般能解决问题。注意：如果电路中有小尺寸管子，或者其他对寄生特别敏感的元件，可能导致结果出现很大偏差
- Integration Method Parameters
  - 精度是`euler < trap < gear2`，速度反之
  - `traponly`和`gear2only`表示只用`trap` / 只用`gear2`算法

## 变量与仿真结果

**信号与表达式**

- 信号（Signal）指电路某节点的电压电流，通常在Output Setup添加Signal后直接在原理图点选
- 表达式（Expression）如其名，是SKILL语言的表达式，比如`peakToPeak(VT("/VOUT"))`表达式计算了VOUT信号的峰峰值。可以借助Tools - Calculator编辑

仿真结束之后还想添加其他信号：Results - Direct Plot - Main Form，设置好之后不关掉Direct Plot Form窗口，鼠标选择要绘制的信号（有的信号没有被保存，导致Direct Plot报错。需要将其加入Outputs中，并勾选Save）

**显示MOS管静态工作点**：选择DC仿真，选中Save DC Operating Point，仿真结束之后，

1. Results - Print - DC Operating Point
2. Results - Annotate - DC Operating Points，然后点击信号
3. 选中器件，右键 - Annotations - DC Operating Points
4. 计算形如`OP("/MN0" "gm")`的表达式

**信号保存设置**

- Outputs - Save All
- Analyses - Choose - Options - Output（会覆盖前一项的设置。建议不要动）

前仿真可以用默认设置，后仿真建议设置selected，否则仿真结果动辄几十几百GB。注意，信号保存选项和电流保存选项是分开的。保存选项有

- selected：只保存Outputs中的信号
- lvl：保存`nestlvl`深度的信号，比如`nestlvl = 0`就只保存顶层的信号
- all：保存全部信号
- lvlpub、allpub：类似lvl和all，不过只保存”public“信号，一些内部节点（比如Verilog-A内部节点和某些晶体管内部的节点）会被忽略

## 特殊仿真方法

### 参数仿真

原理图中可以将电路参数写为设计变量（Design Variable），如，将控制电压设置为vctr，或将MOS管宽度设置为 W。特别地，temp是表示温度的变量，仿温度影响时通常取温度为0，27，85

使用设计变量，不修改原理图就可以仿真参数对性能的影响，可以较方便地找到最佳取值。设置参数与扫参数的方法为：

**ADE L**

- 设置参数：在Design Variables面板右键 - Edit，或者选择Variables - Edit
- 扫参数：Tools - Parametric Analysis

**ADE XL**

- 设置参数：Data View面板的Global Variables或Tests - Design Variables，右键变量，Edit Variable（只有取消Global Variable勾选时Design Variable才有效）
- 扫参数：给参数设置多个值然后仿真

### 工艺角仿真

**ADE L**：Setup - Model Libraries - 选择想要仿真的工艺角，然后运行仿真

**ADE XL**：Corners

### 蒙特卡罗仿真

只能用ADE XL跑。Run - Monte Carlo Sampling

### 后仿真

首先跑PEX，提取clibre view；Setup - Environment，在Switch View List开头加上calibre

## 仿真速度与精度设置

以下设置，可以在Setup - High-Performance Simulation配置，也可以在Setup - Environment - User Command Line Option加上参数。（部分设置在GUI中没有，只能加参数）

这些方法基本都涉及速度精度的折中，注意不要光顾着速度就忘了精度。[参考](https://community.cadence.com/cadence_blogs_8/b/cic/posts/spectre-optimizing-spectre-aps-performance)

- **多线程**：Setup - High-Performance Simulation - Simulation Performance Mode - APS。APS（Accelerated Parallel Simulator）并行仿真提高速度，精度不受影响
- **`++aps`和Errpreset**（此设置精度越高速度就越低。为了简洁起见只说精度不说速度）
  - `+aps > ++aps`
  - `conservative > moderate > liberal`，且此项影响大于前一项
  - 精度从高到低分别是`+aps=conservative`，`++aps=conservative`，`+aps=moderate`，`++aps=moderate`，`+aps=liberal`，`++aps=liberal`
  - 据黄鲁老师说，数字电路用liberal、模拟电路用conservative或者moderate
- `+postlayout`：合并部分RC，用于后仿真加速，同样牺牲精度
  - `+postlayout=upa`（Ultra precision analog）精度最高，`+postlayout=hpa`（High precision analog）次之（1% between no reduction and `+postlayout=hpa`），`+postlayout`精度最差
  - 据李嘉铭说，速度差别不大，精度差别没有验证过


官方建议设置使用APS、从`++aps=moderate +postlayout=hpa`开始，根据结果调整仿真精度。这种流程有点理想化，仅当参考

## 其他细节

**设置电路初值**：ADE L - Simulation - Convergence Aids - Node Set / Initial Condition（补充说明：仿真器进行tran仿真之前会进行DC仿真求解电路初值。Node Set设置DC仿真迭代初值，**帮助仿真收敛**；Initial Condition设置DC仿真全程的节点电压，用于**设置电路初值**。如果Initial Condition设成一个正常无法达到的状态，可能导致后续tran仿真错误。[Source](https://community.cadence.com/cadence_technology_forums/f/rf-design/29843/ade--difference-between-node-set-and-initial-condition)）

**并行仿真**：ADE XL - Options - Job Setup设置数量大于1，Options - Run Options选择Parallel，可以同时进行多个仿真

使用了CMOS库之后要在 Setup - Environment 删除名字里包含 cmos 的几个视图，否则可能出现 no corresponding terminal 的错误

噪声频率 0.01~10G。说是由宝贵的经验定下来的

快捷键：A、B设置Point Marker，M添加Point Marker，H、V添加Horizontal / Vertial Marker

# 其他

## 输出图片

**方法1：输出点阵图**

原理图和版图：File - Export Image

仿真波形：File - Save Image

**方法2：输出矢量图**

首先在工作目录（cds.lib所在目录）或者根目录（CDS.log所在目录）创建`.cdsplotinit`文件（规定输出格式、输出尺寸等），内容如下：

```
EPS|Encapsulated Postscript: \
    :manufacturer=Adobe: \
    :type=epsf: \
    :maximumPages#1: \
    :resolution#300: \
    :paperSize="Unlimited" 72000 72000:

EPS Color|Encapsulated Postscript: \
    :manufacturer=Adobe: \
    :type=epsfC: \
    :maximumPages#1: \
    :resolution#300: \
    :paperSize="Unlimited" 72000 72000:
```

服务器的`/cdsmgr/IC616/tools/plot/sample`文件夹下有更详细的示例，`/cdsmgr/IC616/doc/plot`有具体文档

在原理图 / 版图选择File - Print，在弹出界面设置打印区域，并在Plot Options选择一个plotter（如果没有plotter可能是`.cdsplotinit`文件有误），勾选Send Plot To File并设置保存文件名。保存的是EPS文件，可以用linux的`ps2pdfwr`指令转换为pdf，使用例：`ps2pdfwr p.eps p.pdf`

2021.11.27：不知道为什么存下来的都是单色图片。而且转为pdf之后是空白页

## 去除上锁文件

**注意：有可能误删文件。请务必小心**

```bash
find ./ -i name "*.cdslck*" -exec rm -rf "{}" \;
```

## `.cdsinit`和`.cdsenv`

`.cdsinit`与`.cdsenv`文件位于工作目录，前者是一个Skill脚本，在软件启动时自动运行；后者是Cadence环境设置
