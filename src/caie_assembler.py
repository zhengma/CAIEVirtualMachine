from pprint import pprint
import re
from caie_vm import caie_vm
from typing import Any, Self, Callable

class caie_assembler():

    def __init__(self, source_file: str, base: int, data: int = 0, 
                 debug_mode: bool = False) -> None:
        self.source = source_file
        with open(source_file, 'r', encoding='utf-8') as source:
            raw_lines = source.readlines()
            self.lines = []
            for line in raw_lines:
                self.lines.append(line.strip())
        self.__symbols__()
        self.__baseaddr = base
        self.__dataaddr = data
        self.__parsed = None
        self.__linenums = None
        self.__label_list = {}
        if not debug_mode:
            self.parse(base, data)
    
    def __symbols__(self) -> None:
        self.punc_label = ':'
        self.punc_comment = ';'
        self.punc_dec = '#'
        self.punc_bin = 'B'
        self.punc_hex = '&'
        funcs = dir(caie_vm)
        self.mnemonics = ['END']
        for f in funcs:
            if len(f) == 2 or len(f) == 3:
                self.mnemonics.append(f)
        self.mnemonics.sort(reverse=True)
        self.reserved = self.mnemonics + ['ACC', 'IX']
    
    def get_address(self) -> tuple[int]:
        return (self.__baseaddr, self.__dataaddr)

    def is_valid_label(self, s: str) -> bool:
        pattern = '^[A-Za-z_][A-Za-z0-9_]*$'
        return bool(re.match(pattern, s)) and (s not in self.reserved)

    def is_valid_opcode(self, s: str) -> bool:
        return s in self.mnemonics
    
    def is_valid_operand(self, s: str) -> bool:
        p_bin = f'(^{self.punc_bin}[01]+$)'
        p_dec = f'(^{self.punc_dec}[0-9]+$)'
        p_hex = f'(^{self.punc_hex}[A-Fa-f0-9]+$)'
        pattern = f'{p_bin}|{p_dec}|{p_hex}'
        return (bool(re.match(pattern, s)) or self.is_valid_label(s) 
                or s in ['ACC', 'IX'])

    def _instant(self, s: str) -> int:
        match s[0]:
            case '#':
                return int(s[1:])
            case '&':
                return int(s[1:], 16)
            case 'B':
                return int(s[1:], 2)
            case _:
                raise Exception(f'\'{s}\' is not an instant number!')

    def _lex_comment(self, tokens: dict, line: str) -> (dict, str):
        line = line.split(self.punc_comment)[0]
        return (tokens, line)
    
    def re_label(self) -> str:
        return '[A-Za-z_][A-Za-z0-9]*'
    
    def re_opcode(self) -> str:
        opcodes = ''
        for key in self.mnemonics:
            opcodes += f'{key}|'
        return opcodes[:-1]

    def re_operand(self) -> str:
        p_bin = f'{self.punc_bin}[01]+'
        p_dec = f'{self.punc_dec}[0-9]+'
        p_hex = f'{self.punc_hex}[A-Fa-f0-9]+'
        p_address = f'[0-9]+'
        return f'{p_bin}|{p_dec}|{p_hex}|{p_address}|{self.re_label()}'

    def lex_pattern(self) -> str:
        return f"\\s*((?P<label>{self.re_label()}):)?\
(\\s*(?P<opcode>{self.re_opcode()})?\
(\\s*(?P<operand>{self.re_operand()}))?)?"

    def lexical(self, line: str) -> dict:
        m = re.match(self.lex_pattern(), line)
        if m and m.end() > m.start():
            return m.groupdict()
        else:
            return {}

    def parse(self, base: int, data: int = None) -> None:
        parsed = []
        line_numbers = {}
        address = base

        for num, line in enumerate(self.lines):
            tokens = self.lexical(line)
            if tokens:
                parsed.append([address, tokens])
                line_numbers[address] = num + 1
                if (data and parsed[-1][1]['opcode'] == 'END'):
                    parsed[-1][1]['address'] = address
                    address = data
                else:
                    address += 1

        for pline in parsed:
            if pline[1]['label']:
                if pline[1]['label'] in self.__label_list:
                    raise Exception(f'{pline[1]["label"]} already exists!')
                self.__label_list[pline[1]['label']] = pline[0]

        for pline in parsed:
            if pline[1]['operand'] and self.is_valid_label(pline[1]['operand']):
                try:
                    pline[1]['operand'] = self.__label_list[pline[1]['operand']]
                except IndexError:
                    print(pline[1]['operand'])
        
        self.__parsed =  [line[1] for line in parsed]
        self.__linenums = line_numbers
    
    def instruction_block(self) -> str:
        lines = []
        for pline in self.__parsed:
            if 'opcode' in pline and pline['opcode'] == 'END':
                break
            else:
                instruction = f'{pline["opcode"]}'
                if pline['operand']:
                    instruction += f' {pline["operand"]}'
                lines.append(instruction)
        return "\n".join(lines)

    def line_number(self, address: int) -> int:
        return self.__linenums[address]
    
    def line_num_list(self) -> list:
        return self.__linenums.copy()

    def generate(self):
        exe = []
        for pline in self.__parsed:
            if not pline['opcode'] and not pline['operand']:
                exe.append(None)
            else:
                exe.append([])
            if pline['opcode']:
                exe[-1].append(pline['opcode'])
                if pline['opcode'] == 'END' and self.__dataaddr:
                    blanks = self.__dataaddr - pline['address'] - 1
                    exe.extend([None]*blanks)
            if pline['operand']:
                if (isinstance(pline['operand'], int) or 
                    pline['operand'] in ['ACC', 'IX']):
                    exe[-1].append(pline['operand'])
                else:
                    exe[-1].append(self._instant(pline['operand']))
                    if pline['opcode'] in caie_vm.bimodeop():
                        exe[-1].append(False)
            if isinstance(exe[-1], list) and isinstance(exe[-1][0], int):
                exe[-1] = exe[-1][0]
        return exe