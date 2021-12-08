#   Cadence组件简介

- DB Doctor：错误诊断、修复数据错误
- Design Entry CIS：板级原理图设计工具的启动器
  - OrCAD Capture CIS：主要的原理图设计工具
- Design Entry HDL：芯片开发原理图设计工具的启动器
- Pad Designer：编辑焊盘
- PCB Editor：PCB设计工具的启动器
  - Allegro Constraint Manager：约束管理器
  - Allegro PCB Editor：主要的PCB设计工具
- PCB Libraries：元件封装库编辑器
- PCB Router：自动布线工具
- PCB PI：电源完整性仿真
- PCB SI、SigXplorer：信号完整性仿真
- Project Manager：各种东西的启动器

# 原理图

打开原理图编辑器：

1. 打开Design Entry CIS
2. 在弹出的组件选择菜单中选择OrCAD Capture CIS

## 工程目录结构

在文件浏览器能看到以下几种文件：

- `.opj`：Project file，包含了Design Resources的信息
- `.dsn`：Design file，设计文件，包含原理图
- `.olb`：Library file，元件库

在工程管理窗口可以看到如下文件结构：

```bash
Design Resources
├─project.dsn
│ ├─SCHEMATIC     # 原理图文件夹。其中包含了若干页的原理图
│ └─Design Cache  # 原理图中用到的器件
├─project.olb
│ ├─part1         # 元件（一般不会在同一个工程中包含原理图和元件库）
│ ├─part2
│ ├─...
│ └─Library Cache
└─Library
  └─example.olb   # 导入的元件库（一般不必导入）
Outputs
Referenced Projects
```

## 流程

1. 创建工程：File - New - Project。种类一般选择schematic
2. 创建原理图：Design - New Schematic Page，或者在工程管理窗口选中SCHEMATIC文件夹，右键 - New Page
3. 放置元件：Place - Part
4. 连线：Place - Wire。不要把不同元件引脚相接代替连线，比较容易出bug
5. 不同页之间的连接：Place - Off-Page Connector。不同原理图页中名称相同的Connector在电气上互联
6. 元件编号：Tools - Annotate。如果用了multipart器件，记得设置physical packaging
7. 添加封装信息
   1. 在属性窗口编辑PCB Footprint属性。详见后面属性窗口部分（主要对于阻容等无源器件）
   2. 编辑元件库，然后在Design Cache更新元件。更新时选中Replace schematic part properties（比较少用）
8. DRC：Tools - Design Rules Check
9. 生成网表：Tools - Create Netlist，选择PCB Editor，Netlist Files填Allegro
10. 生成元件清单：选中`.dsn`文件，Report - CIS Bill of Materials - Standard，或Tools - Bill of Materials

注意：各种工具都是**上下文相关**的，如果没有选中合适的对象，工具将不可选中或者不显示。比如，必须激活原理图编辑菜单才能放置元件

## 快捷键

**Place**

| Key       | Usage                   | Description                                                  |
| --------- | ----------------------- | ------------------------------------------------------------ |
| P         | **P**art                | 放置元件                                                     |
| X         | No Connect              | 标记引脚不连接                                               |
| W         | **W**ire                | 引线                                                         |
| B         | **B**us                 | 总线。总线名称例`DATA[0:31]`                                 |
| E         | Bus **E**ntry           | 总线入口。接入信号名如`DATA[0]`。Ctrl+拖动可以复制并自动递增信号编号 |
| N         | **N**et Alias           | 线网别名。一个原理图页内同名网络在电气上互联                 |
| R         | **R**otate              | 旋转。选中元件之后才能旋转，可能切断连接关系                 |
| T         | **T**ext                | 文字                                                         |

**Edit**
| Key       | Usage                   | Description                                                  |
| --------- | ----------------------- | ------------------------------------------------------------ |
| H         | Mirror **H**orizontally | 左右翻转                                                     |
| V         | Mirror **V**ertically   | 上下反转                                                     |
| Alt+拖动  |                         | 移动元件，会切断连接关系                                     |
| Ctrl+拖动 |                         | 复制元件                                                     |

## 编辑

- 浏览工程：选中工程文件，Edit - Browse - Parts
- 搜索对象：Edit - Find，快捷键Ctrl + F。搜索框右边望远镜图标再右边的三角图标可以打开搜索选项
- 批量更换/更新元件：选中Design Cache中的元件，右键 - Replace Cache / Update Cache

**属性窗口**

打开属性窗口：

1. 双击元件
2. 选中单个或多个元件，右键 - Properties，或Edit - Properties，或Ctrl + E
3. 选中工程文件或者原理图页面，右键 - Object Properties，或Edit - Object Properties

点击表格上方的Pivot按钮，或者选中整个表格 - 右键 - Pivot可以更改表格排列。单个元件竖排容易看，多个元件横排容易看

可以在表格内多选然后右键 - Edit批量编辑

## 元件库

1. 创建元件库：File - New - Library
2. 添加元件：Design - New Part，或者选中.olb文件夹，右键 - New Part。Multipart选项可以将一个芯片分成若干个部分
   1. Parts per Pkg：分成多少个部分
   2. Package Type：Homogeneous表示各部分相同，比如一个芯片的两个通道，编辑其中一个part时好像是按某种规则同步修改其他part；Hetrogeneous表示各部分不同，比如一个FPGA的多个IO Bank
   3. 编号方式。建议用alphabet
   4. View - Package和View - Part可以切换显示方式。Ctrl+N、Ctrl+B在不同part之间切换
3. 添加管脚：Place - Pin，或者从Toolbar选择。在弹出窗口设置好管脚名等参数之后确认，然后点击要放置的位置。之后双击可以编辑。或者用Place - Pin Array批量添加
4. 批量修改管脚：选中需要改的管脚，右键 - Edit Properties。注意不要选到管脚以外的东西
5. 编辑全部管脚：View - Package，然后Edit - Properties。完了之后可以把View改回Part。（此方法无法编辑管脚类型）
6. 加形状：Place - Line, Rectangle, etc，并调整边框
7. 封装信息：Options - Package Properties - PCB Footprint
8. 其他属性：Options - Part Properties, Package Properties，或者在Part View或者Package View双击打开。如果是Multipart，给每部分的Part Properties添加一个属性用于区分不同芯片，比如叫package（注意group是PCB Editor的保留字，不可以用）

默认各种东西（线条，文字，etc）只能放到格点，可以在Options - Preferences - Grid Display - Pointer snap to grid设置

# PCB

打开PCB设计软件：

1. 打开PCB Editor
2. 选择Allegro PCB Design XL

窗口（Toolbar在View - Cutomize Toolbar设置，另外几个在View - Windows设置）：

- 主窗口
- Toolbar
- Options：激活指令之后有对应设置
- Find：控制你能选中哪些对象
- Visibility：控制显示哪些对象
- World View：缩略图。中键+拖动或者Shift+左键拖动能够移动显示区域
- Command：命令行&命令信息

Class和Subclass：Allegro有若干类（比如：Pin、Board Geometry），每个类拥有若干子类（如，大部分电气连线都有子类Top、Board Geometry类有子类Silkscreen Top），每个对象都属于某个子类。比如说，走线的类是etch，子类是它所在的层；元件包含了焊盘、丝印等部分，各自属于不同的类和子类。Display - Visibility可以调整不同类的显示

## 流程

（教程Part16有更完整的流程）

1. 创建电路板：File - New，Drawing Type选择Board。（或者用Board Wizard，但后者创建方法不太一样）
2. 调整绘图区尺寸：Setup - Design Parameters - Design，调整图纸大小
   1. Size：单位是mil时Accuracy设1~2足够了。Size选项选Other（另外几个是预设大小，不一定合适）
   2. Extents：图纸左下角坐标&图纸宽度、高度。左下角最好是负数坐标，因为一般把原点作为电路板左下角，而电路板边框紧贴图纸边缘不好看。图纸要比电路板大一些，因为1) 布局时可以把器件放到一边，2) 留出空间放drill legend。一般比板子宽100mm / 4000mil足够
3. 添加电路板板框：Add - Line，Class/Subclass设为Board Geometry, Outline。最好用x, ix, iy指令直接输入坐标。画好后最好倒角防止电路板割手：Manufacture - Drafting - Chamfer或Fillet（Chamfer倒45度角，Fillet倒圆弧形），然后选择角的两条边
4. 设置布局区：Setup - Areas - Package Keepin。布局布线与板边缘要留一定距离，因此布局布线布线区比板框要小
5. 设置布线区：Setup - Areas - Route Keepin同上绘制。或者或者Edit - Z-Copy，Copy to Calss/Sublcass设置为Route Keepin, ALL，然后点击Package Keepin的Shape（记得在Find面板选中Shape）
6. 放置安装孔（装铜柱的孔）：Place - Manully，Advanced Settings选中Library，Placement List选Mechanical Symbols
7. 设置板层：Setup - Cross Section。设置好平面层之后可以直接填充
   1. Type：布线层Conductor、介质层Dielectric、平面层（电源平面，地平面等）Plane
   2. Negative：是否负片。好像是平面层负片，信号层正片



1. 导入网表：File - Import - Logic
2. 摆放元件：Place - Manually。右键 - Mirror或者Options - Mirror，就会把元件沿纵轴翻转180°放到底层

类似OrCAD，Allegro的的工具也是上下文相关的，需要选中相应对象 / 激活相应指令才能使用。另外，在Allegro进行绝大多数操作，需要先激活命令，执行操作，然后结束命令（通常是右键 - Done）。命令结束之后回到Idle状态，无法进行操作

## 元件封装

教程20~26讲。目前只学了最基础的

1. 编辑焊盘。运行Pad Designer
   1. Parameter：略。主要是通孔的设置，不经常用
   2. Layers：首先选择Layer，然后编辑下面的选项。尺寸可以参考[贴片元件封装IPC7351标准](https://www.ipc.org/TOC/IPC-7351.pdf)
   3. 保存为`.pad`文件
2. 运行Allegro PCB Editor，File - New，Drawing Type选Package Symbol
3. 放置焊盘：Layout - Pins
4. 绘制元件框：Add - Line，Class和Subclass设置为Package Geometry - Assembly Top
5. 绘制place bound、丝印等

## PCB和原理图联动

1. 同时打开原理图工程和PCB工程
2. OrCAD - Options - Preferences - Miscellaneous - 勾选Enable Intertool Communication
3. 在Allegro激活place manual指令，然后在原理图选中元件，再回到Allegro就能直接放置

## 常用指令

```bash
# 鼠标点击&移动
x 0 0
ix 3
iy -4
```

## 布局布线基础知识

1. 数字器件要远离模拟器件；模数混合器件的数字部分也要朝着数字器件
2. 滤波电容到引脚的走线和接地的线都要尽量短（更具体地，滤波回路与电源平面围成面积尽量小），使寄生电感最小
3. 多个电容滤波时，从大到小按顺序摆放，小电容最靠近引脚（平面去耦时电容有一定去耦半径，而小电容的去耦半径最小）
4. 首先保证小电容靠近引脚，然后让匹配电阻也尽量靠近引脚

教程没看的部分

1. 20~26讲：元件封装
2. 37~46讲：约束。和16.6设置方法不一样
   1. 第37讲：约束规则设置对话框简介，各部分关系
   2. 第38讲：约束规则设置方法
   3. 第39讲：线宽线距约束规则设置示例
   4. 第40讲：区域约束规则设置示例
   5. 第41讲：设置器件模型，加载模型库，赋予器件模型；constraint manager objects显示设置；创建总线
   6. 第42讲：设置拓扑约束（方法1）
   7. 第43讲：设置拓扑约束（方法2）
   8. 第44讲：线长约束规则设置
   9. 第45讲：相对延时约束规则设置
   10. 第46讲：差分约束规则设置
