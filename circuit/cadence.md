#   Cadence组件简介

- Design Entry CIS：板级原理图设计（HDL：芯片开发原理图设计）
- PCB Editor：PCB布局布线
- PCB Libraries：元件封装库编辑器
- PCB Router：自动布线工具
- PCB SI、SigXplorer：信号完整性仿真

# 原理图

## 工程目录结构

在文件浏览器能看到以下几种文件：

- `.opj`：Project file，包含了Design Resources的信息
- `.dsn`：Design file，设计文件，包含原理图
- `.olb`：Library file，元件库

在工程管理窗口可以看到如下文件结构：

```bash
Design Resources
├─project.dsn
│ ├─SCHEMATIC     # 原理图
│ └─Design Cache  # 原理图中用到的器件
├─project.olb
│ ├─part          # 元件（一般不会在同一个工程中包含原理图和元件库）
│ └─Library Cache
└─Library
  └─example.olb   # 导入的元件库（一般不必导入）
Outputs
Referenced Projects
```

## 流程

1. 打开Design Entry CIS
2. 在弹出的组件选择菜单中选择OrCAD Capture CIS
3. 创建工程：File - New - Project。种类一般选择schematic
4. 创建原理图：Design - New Schematic Page，或者在工程管理窗口选中SCHEMATIC文件夹，右键 - New Page
5. 放置元件：Place - Part
6. 连线：Place - Wire。不要把不同元件引脚相接代替连线，比较容易出bug
7. 不同页之间的连接：Place - Off-Page Connector。不同原理图页中名称相同的Connector在电气上互联
8. 元件编号：Tools - Annotate。如果用了multipart器件，记得设置physical packaging
9. 添加封装信息
   1. 在属性窗口编辑PCB Footprint属性。详见后面属性窗口部分（主要对于阻容等无源器件）
   2. 编辑元件库，然后在Design Cache更新元件。更新时选中Replace schematic part properties（比较少用）
10. DRC：Tools - Design Rules Check
11. 生成网表：Tools - Create Netlist，选择PCB Editor，Netlist Files填Allegro
12. 生成元件清单：选中`.dsn`文件，Report - CIS Bill of Materials - Standard

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