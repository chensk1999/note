Synopsys是一个EDA公司，本笔记记录使用Synopsys产品进行数字前、后端设计的流程。并且许多内容都基于郭东磊的模板

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