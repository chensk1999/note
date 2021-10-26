# constraint

```tcl
set_property PACKAGE_PIN P21 [get_ports {SARAD_DB[11]}]
set_property IOSTANDARD LVCMOS33 [get_ports {SARAD_DB[11]}]
```

## LVDS

```tcl
set_property IOSTANDARD LVDS_25 [get_ports {MY_LVDS_P}]
set_property IOSTANDARD LVDS_25 [get_ports {MY_LVDS_N}]
set_property PACKAGE_PIN U12 [get_ports {MY_LVDS_P}]
set_property PACKAGE_PIN U11 [get_ports {MY_LVDS_N}];  #this N-side constraint is optional
set_property DIFF_TERM TRUE [get_ports {MY_LVDS_P}];   #gives internal termination for LVDS input
```

N-side constraint（第4行）不需要加，FPGA会自动选择对应的管脚（因为只有成对管脚才能输入/输出差分信号）。加上之后好像会增加优化时的计算量

# Buffer Primitives

| 原语    | 全名（？）                                  | 说明                                           |
| ------- | ------------------------------------------- | ---------------------------------------------- |
| IBUFG   | Input Global Buffer                         | 用于全局时钟输入缓冲器                         |
| IBUFGDS | Input Global Buffer for Differential Signal | 差分信号的全局时钟输入缓冲器                   |
| BUFG    | Global Buffer                               | 全局缓冲，其输出到FPGA各部分的延迟、抖动都较小 |
| BUFGCE  | Global Buffer with Clock Enable             | 有使能的全局缓冲                               |
| BUFGP   |                                             | IBUF + BUFG                                    |

使用例：

```verilog
IBUFDS instance_name (
    .O (user_O),        // 单端输出 
    .I (user_I),        // 差分信号正相输入
    .IB (user_IB)       // 差分信号反相输入
);
```

其中，在xdc里面配置`create_clock -period 32.000 -waveform {0.000 20.000} [get_ports clk]`就会自动生成全局时钟缓冲。除了差分缓冲器之外几种好像也有办法用约束生成