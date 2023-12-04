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

### 指令清单

该指令集包含的指令清单如下：

操作码	操作数	解释
| LDM  | #n           | Immediate addressing. Load the number n to ACC                                                                                                  |
| :--- | :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| LDD  | \<address>    | Direct addressing. Load the contents of the location at the given address to ACC                                                                |
| LDI  | \<address>    | Indirect addressing. The address to be used is at the given address. Load the contents of this second address to ACC                            |
| LDX  | \<address>    | Indexed addressing. Form the address from \<address> + the contents of the index register. Copy the contents of this calculated address to ACC   |
| LDR  | #n           | Immediate addressing. Load the number n to IX                                                                                                   |
| MOV  | \<register>   | Move the contents of the accumulator to the given register (IX)                                                                                 |
| STO  | \<address>    | Store the contents of ACC at the given address                                                                                                  |
| STX* | \<address>    | Indexed addressing. Form the address from \<address> + the contents of the index register. Copy the contents from ACC to this calculated address |
| STI* | \<address>    | Indirect addressing. The address to be used is at the given address. Store the contents of ACC at this second address                           |
| ADD  | \<address>    | Add the contents of the given address to the ACC                                                                                                |
| ADD  | #n/Bn/&n     | Add the number n to the ACC                                                                                                                     |
| SUB  | \<address>    | Subtract the contents of the given address from the ACC                                                                                         |
| SUB  | #n/Bn/&n     | Subtract the number n from the ACC                                                                                                              |
| INC  | \<register>   | Add 1 to the contents of the register (ACC or IX)                                                                                               |
| DEC  | \<register>   | Subtract 1 from the contents of the register (ACC or IX)                                                                                        |
| JMP  | \<address>    | Jump to the given address                                                                                                                       |
| CMP  | \<address>    | Compare the contents of ACC with the contents of \<address>                                                                                      |
| CMP  | #n           | Compare the contents of ACC with number n                                                                                                       |
| CMI  | \<address>    | Indirect addressing. The address to be used is at the given address.  Compare the contents of ACC with the contents of this second address      |
| JPE  | \<address>    | Following a compare instruction, jump to \<address> if the compare was True                                                                      |
| JPN  | \<address>    | Following a compare instruction, jump to \<address> if the compare was False                                                                     |
| AND  | #n / Bn / &n | Bitwise AND operation of the contents of ACC with the operand                                                                                   |
| AND  | \<address>    | Bitwise AND operation of the contents of ACC with the contents of \<address>                                                                     |
| XOR  | #n / Bn / &n | Bitwise XOR operation of the contents of ACC with the operand                                                                                   |
| XOR  | \<address>    | Bitwise XOR operation of the contents of ACC with the contents of \<address>                                                                     |
| OR   | #n / Bn / &n | Bitwise OR operation of the contents of ACC with the operand                                                                                    |
| OR   | \<address>    | Bitwise OR operation of the contents of ACC with the contents of \<address>                                                                      |
| LSL  | #n           | Bits in ACC are shifted logically n places to the left. Zeros are introduced on the right hand end                                              |
| LSR  | #n           | Bits in ACC are shifted logically n places to the right. Zeros are introduced on the left hand end                                              |
| IN   |              | Key in a character and store its ASCII value in ACC                                                                                             |
| OUT  |              | Output to the screen the character whose ASCII value is stored in ACC                                                                           |
| END  |              | Return control to the operating system                                                                                                          |
|      |              |                                                                                                                                                 |

* `STX` 和 `STI` 两条指令是剑桥大学出版的教材中添加的，考试大纲里没有提及
* `#n` 表示十进制数，`&n` 表示十六进制数，`Bn` 表示二进制数.