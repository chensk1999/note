Synopsys是一个EDA公司，本笔记记录使用Synopsys产品进行数字前端设计、并用Cadence公司的Innovus进行后端设计的流程。大部分内容基于郭东磊的模板

# VCS & Verdi

VCS是Verilog仿真器；Verdi是数字电路debug平台，可以用来查看VCS的仿真结果

## 使用模板

### 前仿真

1. 把Verilog代码放在`design/rtl`目录下
2. 将所有源代码路径加入`design/ft/rtl_filelist_sim.f`中（一行一个文件，例：`../rtl/counter.v`）
3. 将前仿真testbench代码放在`verify/tb_top`目录，源代码路径加入`verify/ft/tb_filelist.f`
4. 在testench顶层加入以下代码：

```verilog
`ifdef USE_FSDB	
    initial begin
        $fsdbDumpfile("inter.fsdb");
        $fsdbDumpvars;
        $fsdbDumpMDA;
    end
`endif
```

5. 打开终端，在`verify/sim`目录下执行`make fsdb`命令，用VCS进行仿真，将结果存到FSDB（Fast Signal Database）文件
6. 执行命令`make verdi`，用Verdi查看仿真结果

### 综合后仿真

1. 前仿真的1~2步
2. 综合，得到netlist
3. 将仿真testbench代码放在`verify_post_syn/tb_top`目录，testbench源代码、网表、库文件路径加入`verify_post_syn/ft/tb_filelist.f`
4. 在testbench顶层加入以下代码。将U0更改为顶层模块实例名

```verilog
`ifdef USE_FSDB	
    initial begin
        $fsdbDumpfile("inter.fsdb");
        $fsdbDumpvars;
        $fsdbDumpMDA;
    end
`endif

initial begin
    $sdf_annotate("../../syn/result/gray_counter.sdf", U0, , , "MAXIMUM");
end
```

5. 前仿真的5~6步

### 布局布线后仿真

和综合后仿真一致，只不过在`verify_post_apr`目录下进行

# Design Compiler

DC是verilog的RTL综合器

## 使用模板

1. 将文件列表添加到`design/ft/rtl_filelist_syn.f`
2. 在`syn/syndc.tcl`中设置顶层模块名（basename）、时序约束等综合参数
3. 运行`syn/run_dc.sh`
4. 生成的网表和延时信息文件分别是`syn/result/<name>_netlist.v`和`syn/result/<name>.sdc`

**时序约束**

主要包括三项：周期、input delay、output delay，单位为纳秒。其中，两个delay指时钟有效沿到数据稳定的时间

比如，时钟周期为10 ns，input delay为2 ns，output delay为3 ns。则0~1 ns，输入可能不稳定，1~10 ns输入保证稳定；10~12 ns，输出可能不稳定，12~20 ns，输出保证稳定

# Innovus

Innovus是Cadence公司的自动布局布线工具，用它进行电路布局布线，然后导入到virtuoso

## 使用模板

**准备工作**

1. 将综合生成的netlist文件、`.sdc`文件复制到`apr/INPUTS`，并且修改时序约束
2. 将`apr/INPUTS/inn_cof.globals`中的`basename`改为顶层模块名
3. 检查多模多角文件`apr/INPUTS/MMMC_lib.tcl`中的`.sdc`文件名
4. 启动innovus：

```
. bash_innovus
innovus
```

6. File - Import Design，Load，选择`apr/INPUTS/inn_cof.globals`

**平面规划、单元布局**

1. 平面规划：Floorplan - Specify Floorplan，需要设置Core Size（放器件区域的面积）和Die SIze（总面积）。一般让Core Utilization在0.6左右，Core to IO Boundary决定电源和地轨的宽度，按需设置
2. 电源环：Power - Power Planning - Add Ring，Nets填VDD、VSS，Ring Configuration设宽度，两者宽度之和略小于上一步设置的Core to IO Boundary
3. 电源条：Power - Power Planning - Add Stripes
4. 连接全局网络：Power - Connect Global Nets，将器件的电源地、Tie High、Tie Low分别连接到全局VDD、VSS
5. IO规划：按照模板填写`apr/INPUTS/RdToken.io`文件，然后File - Load - IO File（据师兄说，用gui修改容易出问题，因此直接用文本形式设置）
6. 保存Floorplan：File - Save - Floorplan，保存的`.fp`文件包含了以上几步的所有东西

**布局布线与优化**

1. ECO - Optimize design

**保存结果**

1. File - Save - GDS2/OASIS

**导入Virtuoso**

1. 建立一个新库。导入的时候会生成一些过孔之类的杂乱文件，最好把从Innovus导入的东西放在单独的库
2. Virtuoso - File - Import - Stream，加载导入设置模板，选择之前保存的`.gds2`文件。导入成功后应该能看见layout视图
3. Virtuoso - File - Import - Verilog，同上。完成之后应该能得到schematic，symbol，functional视图
4. 修改视图标签（加`VDD!`和`VSS!`，将总线的方括号改成尖括号）



