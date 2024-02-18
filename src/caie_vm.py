"""
模拟“CAIE指令系统”的虚拟机

最初在上海科桥讲授《CAIE A level 计算机科学》(9618) 的课堂上编写.

主要教学目的:
1.  协助讲解第5章《处理器基础常识》里面的部分知识点.
2.  在讲授第6章《汇编语言程序设计》和第28章《低级语言程序设计》的时候, 
让学生可以亲手模拟运行其中的示例代码或自己编写的代码. 这允许学生实时检验自己 
对相关知识点的理解，并增加趣味性.
3. 演示第6.04节 "Two-pass Assembler" 中提到的工作原理.
4. 加深对第18.2节 "虚拟机" 的理解.

作者: 马正
组织: 渊学通教育广州分校, 上海科桥教育
创建日期: Dec. 01, 2023
最后修改日期: Dec. 04, 2023
Python版本: 3.11
"""

from typing import Any, Self, Callable
from readchar import readkey, key


class caie_vm():

    __acc: int
    __pc: int
    __ix: int
    __br: int
    __flag: bool
    __ext: bool # 是否调用外界的UI，False则直接在命令行或Jupyter Notebook里运行
    __mem: list
    __flag_interrupt: int
    # 中断寄存器取值的涵义
    # 0 - 无中断
    # 1 - 有输出
    # 2 - 等待输入
    __stdout: str

    def __init__(self, base: int, program: list, ext: bool = False) -> None:
        self.__br = base
        self.__pc = base
        self.__mem = program.copy()
        self.__acc = 0
        self.__ix = 0
        self.__flag = False
        self.__ext = ext
        if not self.__ext:
            self.welcome()
        self.__flag_interrupt = 0
        self.__stdout = ''

    def welcome(self):
        str_output = f"""
{'*'*10} CAIE指令集架构仿真器 v1.0 {'*'*10}
*{' '*45}*
*{' '*20}马 正 {' '*19}*
*{' '*6} 渊学通教育广州分校, 上海科桥教育 {' '*5}*
{'*'*47}
"""
        print(str_output)

    def show_status(self) -> None:
        str_output = f"""{'-'*10} Registers: {'-'*10}
ACC: {self.__acc}

BR: {self.__br}
PC: {self.__pc}
IX: {self.__ix}
flag: {self.__flag}
"""
        print(str_output)
    
    def get_status(self) -> dict:
        return {'ACC': self.__acc,
               'BR': self.__br,
               'PC': self.__pc,
               'IX': self.__ix,
               'flag': self.__flag}

    def bimodeop() -> list:
        return ['ADD', 'SUB', 'CMP', 'AND', 'XOR', 'OR']

    def show_memory(self, range: list = None) -> None:
        if range:
            start = self.__offset__(range[0])
            end = self.__offset__(range[1]) + 1
            print(self.__mem[start:end])
        else:
            print(self.__mem)
    
    def get_memory(self, offset, start: int = None, end: int = None):
        if not start:
            start = 0
        if not end:
            end = len(self.__mem)
        return [[i + offset, self.__mem[i]] for i in range(start, end)]
    
    def get_interrupt(self) -> int:
        return self.__flag_interrupt
    
    def stdin(self, value: int) -> None:
        self.__flag_interrupt = 0
        self.__acc = value
    
    def stdout(self) -> str:
        self.__flag_interrupt = 0
        return self.__stdout

    def LDM(self, number) -> None:
        self.__acc = number

    def __offset__(self, address: int) -> int:
        offset = address - self.__br
        if offset > len(self.__mem):
            raise IndexError(address)
        return offset

    def LDD(self, address: int) -> None:
        try:
            self.__acc = self.__mem[self.__offset__(address)]
        except IndexError:
            raise Exception(f'Address {address} does not exist!')

    def __ptr__(self, address) -> int:
        offset = self.__offset__(address)
        address2 = self.__mem[offset]
        offset2 = address2 - self.__br
        if offset2 > len(self.__mem):
            raise IndexError(address2)
        return offset2

    def LDI(self, address) -> None:
        try:
            self.__acc = self.__mem[self.__ptr__(address)]
        except IndexError as ie:
            raise Exception(f'Address {ie} does not exist!')

    def LDX(self, address) -> None:
        try:
            self.__acc = self.__mem[self.__offset__(address + self.__ix)]
        except IndexError:
            raise Exception(f'Address {address + self.__ix} does not exist!')

    def LDR(self, number) -> None:
        self.__ix = number

    def MOV(self, register: str) -> None:
        match register:
            case 'ACC':
                self.__acc = self.__ix
            case 'IX':
                self.__ix = self.__acc
            case _:
                raise Exception(f'{register} does not exist or cannot be MOVed!')


    def STO(self, address) -> None:
        try:
            self.__mem[self.__offset__(address)] = self.__acc
        except IndexError:
            raise Exception(f'Address {address} does not exist!')

    def STX(self, address) -> None:
        offset = address + self.__ix - self.__br
        try:
            self.__mem[offset] = self.__acc
        except IndexError:
            raise Exception(f'Address {address + self.__ix} does not exist!')

    def STI(self, address) -> None:
        try:
            self.__mem[self.__ptr__(address)] = self.__acc
        except IndexError as ie:
            raise Exception(f'Address {ie} does not exist!')

    def bimode(func: Callable) -> Callable:
        def decorated_func(self, operand: int, isAddress: bool = True) -> None:
            if isAddress:
                try:
                    func(self, self.__mem[self.__offset__(operand)])
                except IndexError as ie:
                    raise Exception(f'Address {ie} does not exist!')
            else:
                func(self, operand)

        return decorated_func

    @bimode
    def ADD(self, value: int) -> None:
        self.__acc += value

    @bimode
    def SUB(self, value: int) -> None:
        self.__acc -= value

    def INC(self, register: str) -> None:
        match register:
            case 'ACC':
                self.__acc += 1
            case 'IX':
                self.__ix += 1
            case 'PC':
                self.__pc += 1
            case _:
                raise Exception(f'No register named {register}!')

    def DEC(self, register: str) -> None:
        match register:
            case 'ACC':
                self.__acc -= 1
            case 'IX':
                self.__ix -= 1
            case 'PC':
                self.__pc -= 1
            case _:
                raise Exception(f'No register named {register}!')

    def JMP(self, address: int) -> None:
        try:
            self.__pc = address
        except IndexError as ie:
            raise Exception(f'Address {ie} does not exist!')        

    @bimode
    def CMP(self, value: int) -> None:
            self.__flag = self.__acc == value

    def CMI(self, address: int) -> None:
        try:
            self.__flag = self.__acc == self.__mem[self.__ptr__(address)]
        except IndexError as ie:
            raise Exception(f'Address {ie} does not exist!')

    def JPE(self, address: int) -> None:
        if self.__flag:
            self.JMP(address)
        else:
            self.__pc += 1

    def JPN(self, address: int) -> None:
        if not self.__flag:
            self.JMP(address)
        else:
            self.__pc += 1

    def IN(self) -> None:
        if self.__ext:
            self.__flag_interrupt = 2
        else:
            self.__acc = ord(readkey())

    def OUT(self) -> None:
        out = chr(self.__acc)
        if self.__ext:
            self.__stdout =  out
            self.__flag_interrupt = 1
        else:
            print(out, end='')

    def OUI(self) -> None:
        out = str(self.__acc)
        if self.__ext:
            self.__stdout =  out + '\n'
            self.__flag_interrupt = 1
        else:
            print(out)

    @bimode
    def AND(self, value: int) -> None:
        self.__acc = self.__acc & value

    @bimode
    def XOR(self, value: int) -> None:
        self.__acc = self.__acc ^ value

    @bimode
    def OR(self, value: int) -> None:
        self.__acc = self.__acc | value

    def LSL(self, n: int) -> None:
        self.__acc = self.__acc << n

    def LSR(self, n: int) -> None:
        self.__acc = self.__acc >> n

    def single_step(self, debugging: bool = True) -> bool:
        if self.__mem[self.__offset__(self.__pc)][0] == 'END':
            return False
        line = self.__mem[self.__offset__(self.__pc)]
        if debugging:
            print(line)
        op = line[0]
        operand = line[1:]
        instruction = getattr(self, op)
        match len(operand):
            case 0:
                instruction()
            case 1:
                instruction(operand[0])
            case 2:
                instruction(operand[0], operand[1])
        if debugging:
            self.show_status()
            self.show_memory()
        if op[0] != 'J':
            self.__pc += 1
        return True
    
    def restart(self) -> None:
        self.__pc = self.__br

    def execute(self) -> None:
        print('Result:')
        while self.__mem[self.__offset__(self.__pc)][0] != 'END':
            self.single_step(False)

# if __name__ == '__main__':
#    print('Hello World!')