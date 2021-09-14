# 概述

* **History of NES**

红白机是任天堂生产的游戏机，1983年在日本发售，称ファミリーコンピュータ（Family Computer），简称ファミコン / FamiCom / FC，1985年在欧美以Nintendo Entertainment System（NES）发行

* **A Brief Introduction on Simulation**

当今的计算机都是图灵完备的，故当然可以相互模拟。一般有以下几种方式模拟（假设用通用图灵机B模拟通用图灵机A）：

1. Convertion：将A机的软件的每条指令翻译成等效的B机指令，在B机上运行转换后的软件，运行结果如同在A机运行的结果。运行速度相对较快，需要对每个软件单独转换
2. Emulation：在运行时读入A机指令，然后转换为B机指令并执行。相当于一个解释器，运行效率比较低

当然，各种游戏机都会防备玩家的破解，因此这只是原则上可行，实际上困难重重。另外， simulation 和 emulation 在语义上有一点微妙的区别：前者强调模拟系统的状态，后者强调模拟系统的行为

* **Hardware Overview** ![](./images/NES_MotherBoard.jpg)
    * CPU：负责游戏程序运行和声音处理
    * PPU：处理图像并产生视频信号，形式是composite TV signal，提供给模拟电视
    * Video Ram (VRAM)：存储图像
    * Work Ram (WRAM)：储存游戏代码和运行时的数据
    * Lockout Chip：检查校验码和地区码，正版校验通过才能加载游戏
    * Generic Logic Chip：没看懂，好像是辅助CPU向PPU传输数据

# CPU

使用Ricoh 6502 的升级版 2A03，内置了声音处理器（pseudo Audio Process Unit，pAPU）

## 存储器组织

<img src="./images/NES_CPU.png" style="zoom:67%;" />

NES的RAM，ROM和IO都是统一编址，方式如下图。另外，由于地址线宽度刚好是数据线的两倍，不是像x86那样分段，而是两个字表示一个地址。它的存储器中有大量的镜像：文档中解释0x0800~0x1FFF是0x0000~0x07FF内容的重复，向0x0000写入时0x0800、0x1000、0x1800都会被写入同样的内容。我推测RAM只有2kB的空间，这四个地址被译码到同一个存储单元

![](./images/NES_CPU_memory_map.png)

PRG-ROM位于游戏卡带（cartridge），一个卡带一般包含若干个PRG-ROM芯片，每个16kB。当游戏容量小于16kB时，它运行时被装入RAM（0x0200~0x0800）；当卡带有两片PRG-ROM时，一片被装入RAM，另一片被映射到PRG-ROM Lower Bank；当有两片以上的PRG-ROM时，第一片被装入RAM，第二片映射到PRG-ROM Lower Bank，剩下的被memory mapper（硬件，位于游戏卡带上，也叫做Memory Manage Chip，MMC）动态映射到Upper Bank

## 寄存器

* 专用寄存器（Special Purpose Register）
  * Program Counter (PC)：16 bit寄存器，存储要执行的下一条指令的地址
  * Stack Pointer (SP)：8 bit 寄存器，栈顶相对0100的偏移地址。堆栈工作方式类似x86
  * Processor Status (P)：8 bit，类似x86的Flag寄存器
* 通用寄存器（General Purpose Register）
  * Accumulator (A)：8 bit，暂存运算结果
  * Index Register X (X)：8 bit，做计数器或者暂存偏移地址
  * Index Register Y (Y)：同X
* 标志寄存器（Flag Register）
  * <img src="./images/NES_CPU_Flag.png" style="zoom:67%;" />
  * C：Carry Flag，上一次操作是否向上进位
  * Z：Zero Flag，上一条指令运算结果是否为0
  * I：Interrupt Disable Flag，是否屏蔽IRQ中断请求
  * D：Decimal Mode，无效
  * B：Break Command，引发IRQ
  * V：Overflow Flag，是否溢出
  * N：Negative Flag，结果是否为负数

## 中断

中断源可以是NMI，IRQ，Reset

IRQ（Interrupt Request，可屏蔽中断）可以由memory mapper产生，也可以软件执行BRK指令引发，跳转执行0xFFFE和0xFFFF的指令

NMI（Non Maskable Interrupt，不可屏蔽中断）由PPU产生，每帧结束后的V-Blank（vertical blank interval，垂直消隐期，扫描线从一帧的右下角转移到下一帧的左上角期间的空白画面。因为这段时间不需要显示东西，且间隔合适，经常被用来处理特殊事件或者传输额外数据）引发一次，跳转执行0xFFFA和0xFFFB的指令

Reset在开机或者重启时触发，跳转执行0xFFFC和0xFFFD的指令

## 指令集

6502有56种指令，一条指令长1~3字节，第一个字节是机器码，第二和第三个是操作数

http://www.6502.org/tutorials/6502opcodes.html

## 寻址

* Zero Page

指令长2字节，第二给字节是操作数相对0x0000的偏移量（即，在zero page种的地址）

```assembly
and $ab         ; 操作数是0x00ab单元存储的值
```

* Indexed Zero Page

在zero page寻址的基础上加上 X 或者 Y 寄存器的值做偏移量

```assembly
and $ab, X      ; 操作数是0x00ab + X单元存储的值
```

* Absolute

指令长3字节，第一个字节是机器码，第二个是操作数地址低字节，第三个是高字节

```assembly
and $abcd       ; 操作数是0xabcd单元的值
```

* Absolute Indexed：在Absolute寻址上加 X 或者 Y 作为偏移量

* Indirect

指令长3字节，后两个字节指向的存储单元的值再指向的存储单元的值是操作数。相当于x86的存储器寻址

```assembly
and ($abcd)     ; 操作数是0xab单元指向的单元（双字）的值
```

* Indexed Indirect：Indirect的第一次寻址加上 X 或者 Y 偏移量
* Indirect Indexed：Indirect的第二次寻址加上 X 或者 Y 偏移量

* Implied：指令隐含了操作数，比如 CLI 指令就是操作标志寄存器中断无效位的
* Accumulator：使用A寄存器的值
* Immediate：立即数。前缀井号，如`and #$12`
* Relative

仅用于Branch instruction（相当于x86的条件跳转指令），长度2字节

如果不满足条件，PC + 2；如果满足条件，PC + 2 + 第二个字节的值，类似于x86的近转移

# PPU

使用Ricoh 2C02

## CPU与PPU通信

* **IO端口**

CPU可以将PPU视作IO设备，通过IO端口访问。访问VRAM的方法是先从0x2006口写地址（一次8bit，需要写两次），然后从0x2007口读写数据，一次读写之后地址自动增加1或者32。也可以从IO端口控制PPU（0x2000和0x2001口），读取PPU状态（0x2002口）

* **DMA**

大批量传输数据时使用DMA进行，比如传输sprite数据时，写首地址高8位到0x4014口，然后DMA设备就会将从此处开始的256个字传输到SPR-RAM。这个过程需要512个周期

## 存储器组织

![](./images/NES_PPU_memory_map.png)

NES可以显示52种颜色，存储一种颜色需要1个字节

* **Palette**（调色板）：Image Palette和Sprite Palette分别记录背景的可用颜色、精灵的可用颜色。其中0x3F00，0x3F04，0x3F08一直到0x3F1C都是透明色（这些存储单元都是mirror），总计可用颜色13种
* **Pattern Table**：存储一个8 x 8像素的图案，Pattern Table 0和Pattern Table 1分别存储Sprite Palette对应颜色最低位和第二低位。一个字节对应一行像素，最低字节对应最靠上的一行
* **Name Table & Attribute Table**：

# SimpleNES阅读笔记

