# 输出放大器

主要参考资料：P. E. Allen, D. R. Holberg, CMOS Analog Circuit Design 3rd edition, 236-247 (section 5.5)

此处讨论的输出放大器（Output Amplifier）是单级放大器，主要用作运放输出级

输出放大器具有驱动小电阻（50~1000Ω）和 / 或大电容（5~1000pF）能力。重要参数包括输出电流（驱动电容的能力）、输出电阻（驱动电阻的能力）、一般放大器的重要参数（带宽、摆幅等）

## Class-A

最大的拉电流（sourcing current）或灌电流（sinking current）等于静态电流。普通的共源极、源极跟随器都属于Class-A。线性度较好，但提高驱动能力需要提高静态电流，驱动大负载时功耗非常大

定义放大器的效率（Efficiency）为输出功率与总功率之比。假设输出为正弦波，则输出功率为$\frac{V_{PP}^2}{8 R_L}$，其中$V_{PP}$为输出信号峰峰值；电路消耗功率为$(V_{DD} - V_{SS}) \times I_Q$，其中$I_Q$为尾电流。摆幅最大为$V_{PP} = V_{DD} - V_{SS}$，尾电流取最小值为$I_Q = \frac{V_{PP}}{2 R_L}$，此时效率取最大值$\eta = \frac{V_{PP}}{4(V_{DD} - V_{SS})} = 25 \%$

## Class-B & Class-AB

Class-B和Class-AB的输出电流并不受限于静态电流。下图是(a) 推拉式源极跟随器输出原理框图，(b) 其电路实现

![](../images/analog_CMOS_push-pull_SF.png)

当Vin很大时，M1饱和，充当源极跟随器，M2截止，电流从M1流向RL；Vin很小时，反之。对于Class-B，两种状态没有交叠，Vin不大不小时M1和M2都截止，输出电流为0；对于Class-AB，其偏置电压Vbias比Class-B的小，两种状态有交叠，交叠区M1和M2均有电流。降低功耗的代价是线性度降低，且摆幅受限

对于B类放大器，假设输出信号为正弦波，则效率$\eta = \frac{V_{out} I_D}{V_{DD} I_D}$，类似Class-A的计算，可以得到效率$\eta = \frac{\pi}{4} = 78.5 \%$

简单的总结一下：

| 类型     | 功耗 | 线性度         |
| -------- | ---- | -------------- |
| Class-A  | 高   | 高             |
| Class-B  | 低   | 低（交越失真） |
| Class-AB | 中等 | 中等           |

另一种常用的电路结构是推拉式共源放大器