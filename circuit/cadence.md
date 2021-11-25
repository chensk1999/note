#   Cadence组件简介

- Design Entry CIS：板级原理图设计（HDL是芯片开发原理图设计）
- PCB Editor：PCB布局布线
- PCB Libraries：原件封装库编辑器
- PCB Router：自动布线工具
- PCB SI、SigXplorer：信号完整性仿真

# 原理图

1. 打开Design Entry CIS
2. 在弹出的组件选择菜单中选择OrCAD Capture CIS
3. 创建工程：File - New - Project。种类一般选择schematic
4. 创建原理图：Design - New Schematic Page，或者在工程管理窗口选中SCHEMATIC文件夹，右键 - New Page

## 元件库

1. 创建元件库：File - New - Library
2. 添加元件：Design - New Part，或者选中.olb文件夹，右键 - New Part
3. 添加管脚：Place - Pin，或者从Toolbar选择。在弹出窗口设置好管脚名等参数之后确认，然后点击要放置的位置。之后双击可以编辑
4. 批量添加管脚：Place - Pin Array
5. 批量修改管脚：选中需要改的管脚，右键 - Edit Properties。注意不要选到管脚以外的东西
6. 编辑全部管脚：View - Package，然后Edit - Properties。完了之后可以把View改回Part。（此方法无法编辑管脚类型）
7. 调整虚线框大小，然后加形状：Place - Rectangle
8. 其他属性：Options - Part Properties, Package Properties