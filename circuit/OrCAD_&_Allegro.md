#   Cadence组件简介

- DB Doctor：错误诊断、修复数据错误
- **Design Entry CIS**：板级原理图设计工具的启动器
  - **OrCAD Capture CIS**：主要的原理图设计工具
- Design Entry HDL：芯片开发原理图设计工具的启动器
- Pad Designer：编辑焊盘
- **PCB Editor**：PCB设计工具的启动器
  - Allegro Constraint Manager：约束管理器
  - **Allegro PCB Editor**：主要的PCB设计工具
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
│ ├─SCHEMATIC1    # 原理图文件夹
│ │ └─PAGE1       # 原理图的一页
│ └─Design Cache  # 原理图中用到的器件
├─project.olb
│ ├─part1         # 元件（一般不会在同一个工程中包含原理图和元件库）
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
6. 元件编号：Tools - Annotate
   1. 选中`.dsn`文件，Tools - Annotate，Action选择Reset part references to "?"，清除原有编号
   2. Action选择Unconditional reference update，重新编号。如果用了multipart器件，记得设置physical packaging

7. 添加封装信息
   - 方法1：在属性窗口编辑PCB Footprint属性。详见后面属性窗口部分（主要对于阻容等无源器件）
   - 方法2：编辑元件库，然后在Design Cache更新元件。更新时选中Replace schematic part properties（比较少用）
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
2. 添加元件：Design - New Part，或者选中`.olb`文件夹，右键 - New Part。Multipart选项可以将一个芯片分成若干个部分
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

## 其他

元件自动编号后再手动编号，导致编号显示下划线：右键器件 - User Assigned Reference - Unset

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

**Class和Subclass**：Allegro有若干类（比如：Pin、Board Geometry），每个类拥有若干子类（如，大部分电气连线都有子类Top、Board Geometry类有子类Silkscreen Top），每个对象都属于某个子类。比如说，走线的类是etch，子类是它所在的层；元件包含了焊盘、丝印等部分，各自属于不同的类和子类。Display - Visibility可以调整不同类的显示

**Allegro操作逻辑**：Allegro的的工具是上下文相关的，需要选中相应对象 / 激活相应指令才能使用。绝大多数操作流程为：激活命令，执行操作，然后结束命令（通常是右键 - Done）。命令结束之后回到Idle状态，无法进行操作

## 绘制焊盘和封装

教程20~26讲。目前只学了最基础的

**绘制焊盘**

1. 编辑焊盘。运行Pad Designer
   1. Parameter：略。主要是通孔的设置，不经常用
   2. Layers：首先选择Layer，然后编辑下面的选项。尺寸可以参考[贴片元件封装IPC7351标准](https://www.ipc.org/TOC/IPC-7351.pdf)
   3. 保存为`.pad`文件

**绘制封装**

1. 运行Allegro PCB Editor，File - New，Drawing Type选Package Symbol
2. 放置焊盘：Layout - Pins，在Option窗口中，Padstack设置要用的焊盘
3. 元件框：Add - Line，Class和Subclass设置为Package Geometry - Assembly Top
4. 丝印层：Package Geometry - Silkscreen Top
5. 安装区：Package Geometry - Place Bound Top
6. 参考编号：Layout - Labels - RefDes，Class和Subclass设置为Ref Des - Silkscreen Top，输入编号（通常输入REF，画版图时自动被替换为元件编号）
7. 保存，得到`.dra`文件和`.psm`文件

完成之后，将焊盘和封装添加到库里：Setup - User Preferences，Categories - Paths - Library，将`.dra`、`.psm`、`.pad`文件放到同一个文件夹，并将此文件夹添加到padpath和psmpath

## 布局布线前准备

1. 创建电路板：File - New，Drawing Type选择Board（或者用Board Wizard，但后者创建方法不太一样；又或者在原理图创建网表时勾选Create or Update PCB Editor Board）
2. 调整绘图区尺寸：Setup - Design Parameters - Design，调整图纸大小
   1. Size：单位一般选mil，Accuracy设1~2。Size选项选Other（另外几个是预设大小，不一定合适）
   2. Extents：图纸左下角坐标&图纸宽度、高度。左下角最好是负数坐标，因为一般把原点作为电路板左下角，而电路板边框紧贴图纸边缘不好看。图纸要比电路板大一些，因为1) 布局时可以把器件放到一边，2) 留出空间放drill legend。一般比板子宽100mm / 4000mil足够
3. 设置板层：Setup - Cross Section。设置好平面层之后可以直接填充
   1. Type：布线层Conductor、介质层Dielectric、平面层（电源平面，地平面等）Plane
   2. Negative：是否负片。通常平面层负片，信号层正片
4. 设置格点：Setup - Grids
   - Non-Etch：非电气层的栅格点，比如Board Geometry，安装孔
   - All Etch：电气层栅格点，放置器件和走线都在栅格点上
   - 各层：该层的栅格
5. 选择过孔：Setup - Constraints - Physical，在弹出菜单表格中找到VIA，双击，选择Via加入到Via list中
5. 定义电源地：Logic - Identify DC Nets，给电源、地设置电压值。做了这一步之后电源地的鼠线变成一个方框符号，布局布线时不会太乱

## 布局

1. 导入网表：File - Import - Logic。Import logic type选择Design entry CIS，Import directory选择原理图生成网表的位置，默认是`原理图位置/allegro`文件夹
2. 摆放元件：Place - Manually。右键 - Mirror或者Options - Mirror，就会把元件沿纵轴翻转180°放到底层

## 布线

1. Route - Connect
2. 添加过孔：双击，或右键 - Add Via
1. 一次布多根线：Route - Connect - 右键 - Temp Group，选择多个管脚，右键 - Done
3. Options - Bubble：调整新的线和已有的线如何互动。Hug不动已经布好的线，当新的线被挡住时紧靠已有的线；Shove推挤原有的线，为新的线腾出空间。如果选shove via，过孔也可以被推挤（Full优先推挤过孔，Manual优先推挤线而保持过孔不动）

## 绘制板框、铺铜

1. 绘制`Board Geometry / Outline`以及`Route Keepin / All`。两者距离30~40mil
2. Shape - Rectangular，`Etch / 要铺铜的层`，Type选Dynamic Copper，Assign net name选要铺的网络名，然后画形状（可以直接画比Route Keepin更大的方框，Allegro会自动把它限制到和Route Keepin同样大）
3. 电源平面分割：Add - Line，画Anti Etch，宽度20~30mil；Edit - Split Plane - Create，然后为分割后每部分选择网络，分割成功后删除Anti Etch
3. 放置安装孔（装铜柱的孔）：Place - Manully，Advanced Settings选中Library，Placement List选Mechanical Symbols

## 其他

**PCB和原理图联动**

1. 同时打开原理图工程和PCB工程
2. OrCAD - Options - Preferences - Miscellaneous - 勾选Enable Intertool Communication
2. 如果联动失败，重新导出网表：Tools - Create Netlist，选中Create or Update PCB Editor Board
3. 在Allegro激活place manual指令，然后在原理图选中元件，再回到Allegro就能直接放置

**布局布线基础知识**

1. 数字器件要远离模拟器件；模数混合器件的数字部分也要朝着数字器件
2. 滤波电容到引脚的走线和接地的线都要尽量短（更具体地，滤波回路与电源平面围成面积尽量小），使寄生电感最小
3. 多个电容滤波时，从大到小按顺序摆放，小电容最靠近引脚（平面去耦时电容有一定去耦半径，而小电容的去耦半径最小）
4. 首先保证小电容靠近引脚，然后让匹配电阻也尽量靠近引脚

**常用指令**

```bash
# 鼠标点击&移动
x 0 0
ix 3
iy -4
```

**对齐器件**

1. 进入布局模式：Setup - Application Mode - Placement Edit，或者右键 - Application Mode - Placement Edit
2. 选中所有要对齐的器件
3. 对着对齐基准的器件，右键 - Align Components。然后还可以在Options中选择对齐设置
4. 回到普通模式：Setup - Application Mode - General Edit

**调整文字字号**

1. 设置预设字号：Setup - Design Parameter - Text - Setup text size，每个编号对应一个字号（通常不用自己设置）
2. 修改字号：Edit - Change，在Options中选中Text block，以及字号的编号
3. 选择要改变的丝印，右键 - Done

**隐藏某一层**

1. Manufacture - Artwork，应该会显示TOP，BOTTOM等各层。随便选一个，右键 - Add，如想显示顶层，需要的类为`REF DES / Silkscreen_Top`、`Pin / Top`、`Package Geometry / Silkscreen Top`、`Board Geometry / Outline`、`Board Geometry / Silkscreen Top`
2. Visibility窗口 - Views - 选择刚才新建的层
3. 显示全部层：Display - Color/Visibility - Global Visibility，或者新建一个显示全部层的View

**杂项**

走线拐角显示断开：Setup - Design Parameters - Display - Enhanced display modes - Connect line endcaps

调整形状：Shape - Select Shape or Void/Cavity

# 教程目录

教程：于争博士cadence视频教程

没看的部分：20~26封装库、37~46约束规则设置、47显示设置、p51~60

## 基础

- 第1讲 课程介绍，学习方法，了解CADENCE软件

## 原理图

- 第2讲 创建工程，创建元件库
- 第3讲 multipart元件的制作方法
- 第4讲 正确使用heterogeneous类型的元件
- 第5讲 加入元件库，放置元件
- 第6讲 同一个页面内建立电气互连
- 第7讲 总线的使用方法、在不同页面之间建立电气连接
- 第8讲 browse命令的使用技巧
- 第9讲 搜索操作使用技巧
- 第10讲 元件的替换与更新
- 第11讲 对原理图中对象的基本操作
- 第12讲
  1、修改元件的VALUE及索引编号方法
  2、属性值位置调整
  3、放置文本
  4、文本的移动、旋转、拷贝、粘贴、删除
  5、编辑文字的大小、字体、颜色
  6、放置图形
- 第13讲 如何添加封装信息
- 第14讲 生成网表
- 第15讲 生成元件清单、打印原理图

## PCB设计

- 第16讲 高速电路设计流程，本教程使用的简化流程
- 第17讲 Allegro常用软件模块介绍，各个软件模块之间的关系
- 第18讲 Allegro PCB Editor 软件操作界面介绍
- 第19讲 allegro中两个重要的概念：class和subclass是什么

**封装库**

- 第20讲：封装制作基础；
- 第21讲：BGA272封装制作，TI DSP6713；怎样设置引脚名称，怎样修改引脚布局；
- 第22讲：怎样创建自定义形状焊盘；
- 第23讲：SOIC类型封装制作；
- 第24讲：PQFP类型封装制作，学习引脚的旋转方法；
- 第25讲：包含通孔类引脚的零件制作，元件制作向导的使用；
- 第26讲：包含非电气引脚的零件制作方法；

**布局**

- 第27讲：创建电路板；
- 第28讲：设置叠层结构，创建内层电源和地平面；
- 第29讲：导入网表，栅格点的设置，Drawing Option的设置；
- 第30讲：手工摆放元件；
- 第31讲：使用原理图进行交互式摆放；
- 第32讲：按原理图页面进行摆放；
- 第33讲：使用Allegro pcb editor按room摆放；
- 第34讲：使用OrCAD Capture CIS按room摆放；
- 第35讲：快速布局，摆放过程中如何自动定位找到元件；
- 第36讲：pcb布局基本知识简单介绍；

**约束**

- 第37讲：约束规则设置对话框简介，各部分关系；
- 第38讲：约束规则设置方法；
- 第39讲：线宽线距约束规则设置示例；
- 第40讲：区域约束规则设置示例；
- 第41讲
  1、设置器件模型，加载模型库，赋予器件模型
  2、Constraint manager objects显示设置
  3、创建总线
- 第42讲 设置拓扑约束（方法1）
- 第43讲 置拓扑约束（方法2）
- 第44讲 线长约束设置
- 第45讲 相对延迟设置
- 第46讲 差分规则设置

**布线**

- 第47讲 布线准备：栅格点、显示设置等
- 第48讲 BGA零件的自动扇出
- 第49讲 手工布线、控制面板中内容解释
- 第50讲 走线
- 第51讲 群组布线
- 第52讲 布线时信息显示
  1、布线时显示延迟以及相对延迟信息
  2、动态显示走线长度
- 第53讲 差分布线方法
  1、伴随走线
  2、单根走线模式
  3、添加过孔
  4、自动分离与靠拢
- 第54讲 两种高速布线形式
  1、含T形连接点的网络走线方法
  2、蛇形走线方法
  3、修线
- 第55讲 铺铜操作
  1、内电层铺铜
  2、外层铺铜
  3、编辑shape的边界
  4、指定网络
  5、手工void
  6、删除孤岛
  7、铺静态铜皮
  8、铜皮的合并
- 第56讲 电源层分割
- 第57讲 后处理：重新编号，back annotate，查看报告，数据库检查等杂散操作。
- 第58讲 丝印处理
- 第59讲 NC DRILL 相关操作
- 第60讲 制作光绘文件的方法步骤
