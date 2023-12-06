from pprint import pprint
import re
from caie_vm import caie_vm
from typing import Any, Self, Callable

class caie_assembler():

    def __init__(self, source_file: str) -> None:
        with open(source_file, 'r') as source:
            raw_lines = source.readlines()
            self.lines = []
            for line in raw_lines:
                self.lines.append(line.strip())
            self.__symbols__()
    
    def __symbols__(self) -> None:
        self.punc_label = ':'
        self.punc_comment = ';'
        self.punc_dec = '#'
        self.punc_bin = 'B'
        self.punc_hex = '&'
        funcs = dir(caie_vm)
        self.mnemonics = ['END', 'ACC', 'IX']
        for f in funcs:
            if len(f) == 2 or len(f) == 3:
                self.mnemonics.append(f)

    def is_valid_label(self, s: str) -> bool:
        pattern = '^[A-Za-z_][A-Za-z0-9_]*$'
        return bool(re.match(pattern, s)) and (s not in self.mnemonics)

    def is_valid_opcode(self, s: str) -> bool:
        return s in self.mnemonics
    
    def is_valid_operand(self, s: str) -> bool:
        p_bin = f'(^{self.punc_bin}[01]+$)'
        p_dec = f'(^{self.punc_dec}[0-9]+$)'
        p_hex = f'(^{self.punc_hex}[A-Fa-f0-9]+$)'
        pattern = f'{p_bin}|{p_dec}|{p_hex}'
        return (bool(re.match(pattern, s)) or self.is_valid_label(s) 
                or s in ['ACC', 'IX'])

    def instant(self, s: str) -> int:
        match s[0]:
            case '#':
                return int(s[1:])
            case '&':
                return int(s[1:], 16)
            case 'B':
                return int(s[1:], 2)
            case _:
                raise Exception('Not an instant number!')

    def lexical(self, line: str) -> dict:
        tokens = {}
        line = line.split(self.punc_comment)[0]
        if self.punc_label in line:
            label_statement = line.split(self.punc_label)
            if len(label_statement) > 2:
                raise Exception(f'\'{line}\' has too many {self.punc_label}\'s.')
            if self.is_valid_label(label_statement[0]):
                tokens['label'] = line.split(self.punc_label)[0]
            else:
                raise Exception(f'{label_statement[0]} isn\'t a valid label.')
            if len(label_statement) == 2:
                statement = label_statement[1].split()
        else:
            statement = line.split()
        if len(statement) == 1:
            if self.is_valid_opcode(statement[0]):
                tokens['opcode'] = statement[0]
            elif self.is_valid_operand(statement[0]):
                tokens['operand'] = statement[0]
            else:
                raise Exception(f'\'{statement[0]}\' is invalid.')
        elif len(statement) == 2:
            if self.is_valid_opcode(statement[0]):
                tokens['opcode'] = statement[0]
            else:
                raise Exception(f'\'{statement[0]}\' is not a valid opcode.')
            if self.is_valid_operand(statement[1]):
                tokens['operand'] = statement[1]
            else:
                raise Exception(f'\'{statement[1]}\' is not a valid operand.')
        return tokens

    def parse(self, base: int, data: int) -> list:
        parsed = []
        address = base

        for line in self.lines:
            if line[0] != self.punc_comment:
                parsed.append([address, self.lexical(line)])
                if 'opcode' in parsed[-1][1] and parsed[-1][1]['opcode'] == 'END':
                    parsed[-1][1]['address'] = address
                    address = data
                else:
                    address += 1

        label_list = []
        for parsed_line in parsed:
            if 'label' in parsed_line[1]:
                label_list.append([parsed_line[0], parsed_line[1]['label']])

        for parsed_line in parsed:
            if 'operand' in parsed_line[1] and self.is_valid_label(parsed_line[1]['operand']):
                parsed_line[1]['operand'] = list(filter(lambda x: x[1] == parsed_line[1]['operand'], label_list))[0][0]
        
        return [line[1] for line in parsed]
        # pprint(parsed)
        # pprint(label_list)

    def generate(self, base: int, data: int):
        parsed = self.parse(base, data)
        exe = []
        for pline in parsed:
            if 'opcode' in pline:
                if pline['opcode'] == 'END':
                    exe.append(['END'])
                    blanks = data - pline['address'] - 1
                    exe.extend([None]*blanks)
                elif pline['opcode'] in caie_vm.bimodeop():
                    if isinstance(pline['operand'], int):
                        exe.append([pline['opcode'], pline['operand']])
                    else:
                        exe.append([pline['opcode'], 
                                    self.instant(pline['operand']), False])
                elif 'operand' in pline:
                    exe.append([pline['opcode'], pline['operand']])
                else:
                    exe.append([pline['opcode']])
            else:
                if 'operand' in pline:
                    exe.append(self.instant(pline['operand']))
                else:
                    exe.append(None)
        return exe