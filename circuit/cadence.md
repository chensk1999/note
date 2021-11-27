#   Cadence组件简介

- Design Entry CIS：板级原理图设计（HDL：芯片开发原理图设计）
- PCB Editor：PCB布局布线
- PCB Libraries：元件封装库编辑器
- PCB Router：自动布线工具
- PCB SI、SigXplorer：信号完整性仿真

# 原理图

1. 打开Design Entry CIS
2. 在弹出的组件选择菜单中选择OrCAD Capture CIS
3. 创建工程：File - New - Project。种类一般选择schematic
4. 创建原理图：Design - New Schematic Page，或者在工程管理窗口选中SCHEMATIC文件夹，右键 - New Page
5. 放置元件
6. 元件编号：Tools - Annotate。如果用了multipart器件，记得设置physical packaging

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
7. 其他属性：Options - Part Properties, Package Properties，或者在Part View或者Package View双击打开。如果是Multipart，给每部分的Part Properties添加一个属性用于区分不同芯片，比如叫package（注意group是PCB Editor的保留字，不可以用）

默认各种东西（线条，文字，etc）只能放到格点，可以在Options - Preferences - Grid Display - Pointer snap to grid设置