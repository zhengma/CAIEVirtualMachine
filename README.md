# “CAIE指令集架构”仿真器

**马正**

**渊学通教育广州分校**
**上海科桥教育**

本仓库包含一个基于《CAIE A level 计算机科学》 (`9618`) 的考试大纲里面“汇编语言”一节编写的仿真器，主要用途是帮助学生熟练掌握该部分考试内容。该仿真器可以模拟运行根据上述文档规范编写的程序，并在单步执行中观察寄存器和内存状态的变化。

## 缘起

国内主流的国际高中课程体系全都开设有计算机科学课，但CAIE是唯一用较大篇幅，在相当深度上讲授汇编语言基础知识。近几年的考试中，涉及汇编语言常有颇为复杂的代码阅读和代码编写的题目。因此，这部分也被很多考生看作A level 计算机最难啃的一块硬骨头，相关题目得分率历年都是偏低的。

造成这种难度的部分原因，是CAIE考试局为讲授和考察这个模块，专门编造了一套简化版的“玩具”指令集架构，借鉴现实中实用的架构的基础上进行了大幅度削减，力求让考生理解基本原理的同时不需要记忆背诵太多复杂的细节。因此，这套架构也俗称 **“CAIE指令集”** 。

对考生来说，削弱难度本来是好消息，问题是：没有任何真实的芯片是基于CAIE指令集设计制造的。学习比如Java或Python时，考生可以大量编写代码，并在自己的电脑上随时观察运行效果，迅速入门和提高。但是学到汇编语言这一章，考生在阅读代码和亲手书写代码时，只能凭自己的理解推演运行效果，缺乏实时的正误反馈，对学习效果非常不利。

因此，我决定编写一个仿真器，模拟一台处理器基于 “CAIE指令集” 的电脑的工作过程，并为其配套一个汇编器。这样，教材中和往年真题里的相关示例代码，以及遵循考试大纲第4.2节《汇编语言》所描述的规范编写的所有代码，都可以在这套仿真器上模拟运行。学生就可以像学习真实存在的高级语言一样，通过“多写多跑代码”备考这部分内容了。

## “CAIE指令集架构” 简述

该架构混合借鉴了CISC和RISC的设计理念。一方面，它的很多算术指令都能直接访问内存，而且只有一个通用寄存器；另一方面，它指令很少（特别是没有专门的乘法和除法指令），格式比较规整简洁，长度均匀。

### 寄存器

该架构只含有一个通用寄存器：累加器 `ACC`.  此外还有一个索引寄存器 `IX`.  程序计数器 `PC` 可以通过跳转指令修改.  基址寄存器`BR`的值在加载程序时固定，程序运行过程中不能直接修改.

在进行按位运算时，默认每个寄存器的容量为8位.

### 指令清单

该指令集包含的指令清单如下：

		
| 操作码 | 操作数         | 解释                                                                                    |
| :----- | :------------- | :-------------------------------------------------------------------------------------- |
| `LDM`  | `#n`           | 将立即数 `n` 载入到 `ACC` 中.                                                           |
| `LDD`  | `<address>`    | 直接寻址. 将指定地址处的内容载入到 `ACC` 中.                                            |
| `LDI`  | `<address>`    | 间接寻址. 指定地址存放的内容是另一处数据所在的地址. 将后者处的内容载入到 `ACC` 中.      |
| `LDX`  | `<address>`    | 索引寻址. 把指定地址加上 `IX` 寄存器的内容, 将所得地址处的内容载入到 `ACC` 中.          |
| `LDR`  | `#n`           | 将立即数 `n` 载入到 `IX` 中                                                             |
| `MOV`  | `<register>`   | `MOV ACC` 将 `IX` 的内容复制到 `ACC` 中. `MOV IX` 则相反.                               |
| `STO`  | `<address>`    | 将 `ACC` 的内容写入指定地址.                                                            |
| `STX`* | `<address>`    | 索引寻址. 把指定地址加上 `IX` 寄存器的内容, 将 `ACC` 的内容写入所得地址处.              |
| `STI`* | `<address>`    | 间接寻址. 指定地址存放的内容是另一处数据所在的地址. 将 `ACC` 的内容写入后者处.          |
| `ADD`  | `<address>`    | 在 `ACC` 原有值的基础上加上指定地址处的内容.                                            |
| `ADD`  | `#n`/`Bn`/`&n` | 在 `ACC` 原有值的基础上加上立即数 `n`                                                   |
| `SUB`  | `<address>`    | 从 `ACC` 的原有值中减去指定地址处的内容.                                                |
| `SUB`  | `#n`/`Bn`/`&n` | 从 `ACC` 的原有值中减去立即数`n`.                                                       |
| `INC`  | `<register>`   | 在指定寄存器 (`ACC` 或 `IX`)的原有值的基础上加1.                                        |
| `DEC`  | `<register>`   | 在指定寄存器 (`ACC` 或 `IX`)的原有值的基础上减1.                                        |
| `JMP`  | `<address>`    | 跳转到指定地址.                                                                         |
| `CMP`  | `<address>`    | 比较 `ACC` 的值与指定地址处的值是否相等                                                 |
| `CMP`  | `#n`           | 比较 `ACC` 的值与立即数`n`是否相等                                                      |
| `CMI`  | `<address>`    | 间接寻址. 指定地址存放的内容是另一处数据所在的地址. 比较 `ACC` 的值与后者处的值是否相等 |
| `JPE`  | `<address>`    | 在比较指令后，若比较结果为相等，则跳转到指定地址处.                                     |
| `JPN`  | `<address>`    | 在比较指令后，若比较结果为不相等，则跳转到指定地址处.                                   |
| `AND`  | `#n`/`Bn`/`&n` | 把 `ACC` 的值与立即数 `n` 进行按位与运算, 结果存入 `ACC`.                               |
| `AND`  | `<address>`    | 把 `ACC` 的值与指定地址处的值进行按位与运算, 结果存入 `ACC`.                            |
| `XOR`  | `#n`/`Bn`/`&n` | 把 `ACC` 的值与立即数 `n` 进行按位异或运算, 结果存入 `ACC`.                             |
| `XOR`  | `<address>`    | 把 `ACC` 的值与指定地址处的值进行按位异或运算, 结果存入 `ACC`.                          |
| `OR`   | `#n`/`Bn`/`&n` | 把 `ACC` 的值与立即数 `n` 进行按位或运算, 结果存入 `ACC`.                               |
| `OR`   | `<address>`    | 把 `ACC` 的值与指定地址处的值进行按位异或运算, 结果存入 `ACC`.                          |
| `LSL`  | `#n`           | 把 `ACC` 的值按位左移 `n` 位，右边用零补齐.                                             |
| `LSR`  | `#n`           | 把 `ACC` 的值按位右移 `n` 位，左边用零补齐.                                             |
| `IN`   |                | 从键盘读入一个按键，将其 ASCII 码存入 `ACC`.                                            |
| `OUT`* |                | 在屏幕上输出一个字符，其`ASCII`码为 `ACC` 的值.                                         |
| `END`  |                | 结束程序.                                                                               |
|        |                |                                                                                         |

* `STX` 和 `STI` 两条指令是剑桥大学出版的教材中添加的，考试大纲里没有提及
* `#n` 表示十进制数，`&n` 表示十六进制数，`Bn` 表示二进制数.
* 为了方便观察，本仿真器中的 `OUT` 可以选择输出数字或字符.