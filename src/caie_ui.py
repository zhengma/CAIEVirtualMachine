from rich.console import Console
from rich.syntax import Syntax
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich import box 
from rich.live import Live
from time import sleep

from caie_vm import caie_vm
from caie_assembler import caie_assembler

from readchar import readkey, key

class caie_ui():

    def __init__(self, assembler: caie_assembler = None, vm: caie_vm = None):
        self.__assembler = assembler
        self.__vm = vm
        self.__layout = None
        self.__make_layout()
        self.__disp_mode = {'code': False, 'mem': True}
    
    def __refresh(self):
        status = self.__get_status()
        self.__layout["state"].update(self.state_viewer(status))
        self.__layout["memory"].update(self.mem_viewer(self.__get_mem()))
        self.__layout["code"].update(self.code_viewer(
            self.__get_current(status['PC'])))
        self.__layout["footer"].update(self.disp_console(self.__vm.stdout()))

    def disp(self):
        self.__layout["header"].update(self.disp_header())
        self.__layout["code"].update(self.code_viewer(self.__assembler.get_address()[0]))

        with Live(self.__layout, refresh_per_second=10, screen=True):
            while self.__vm.single_step(debugging=False):
                self.__refresh()
                # sleep(0.2)
                readkey()
            readkey()
    
    def __make_layout(self) -> None:
        self.__layout = Layout(name="root")

        self.__layout.split(
            Layout(name="header", size=3),
            Layout(name="main", ratio=1),
            Layout(name="footer", size=7),
        )

        self.__layout["main"].split_row(
            Layout(name="code", ratio=2, minimum_size=40),
            Layout(name="view"),
        )
        self.__layout["view"].split(Layout(name="state"), Layout(name="memory"))

    def disp_header(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="center", ratio=1)
        grid.add_column(justify="right")
        grid.add_row("[b]CAIE指令集架构仿真器[/b] v1.0", 
                    "[b]马正 渊学通广州[/b]")
        return Panel(grid, style="white on blue")

    def code_viewer(self, current: int) -> Panel:
        if self.__disp_mode['code']:
            syntax = Syntax.from_path(self.__assembler.source, 
                                      line_numbers = True, 
                                      highlight_lines = {current})
        else:
            syntax = Syntax(self.__assembler.instruction_block(), None,
                            line_numbers = True,
                            start_line = self.__assembler.get_address()[0],
                            highlight_lines = {current})
        return Panel(syntax, border_style="green", title = f'{self.__assembler.source}')
    
    def disp_console(self, s: str) -> Panel:
        return Panel(s, border_style="white", title= 'Command Line')
    
    def __get_status(self) -> dict:
        return self.__vm.get_status()
    
    def __get_mem(self) -> list:
        if self.__disp_mode['mem']:
            base, data = self.__assembler.get_address()
            return self.__vm.get_memory(base, data - base)
        else:
            return None
    
    def __get_current(self, pc: int):
        if self.__disp_mode['code']:
            return self.__assembler.line_number(pc)
        else:
            return pc
   
    def state_viewer(self, regs: dict) -> Panel:
        state = Table(expand=True, box=box.SIMPLE_HEAVY)
        state.add_column('Register', justify='left', min_width=5)
        state.add_column('Value', justify='right', min_width=9)
        for r, v in regs.items():
            state.add_row(str(r), str(v))
        return Panel(state, border_style="red", title = 'Registers')

    def mem_viewer(self, memory: list) -> Panel:
        mem = Table(expand=True, box=box.SIMPLE_HEAVY)
        mem.add_column('Address', justify='left', min_width=4)
        mem.add_column('Data', justify='right', min_width=10)
        for m in memory:
            mem.add_row(str(m[0]), str(m[1]))
        return Panel(mem, border_style="blue", title = 'Memory')

if __name__ == "__main__":
    # file_name = "..\src\Examples\division.casm"
    # file_name = '..\src\Examples\\forloop.casm'
    file_name = "..\src\Examples\whileloop.casm"
    test_assemble = caie_assembler(file_name, 100, 200)
    exe = test_assemble.generate()
    test_run = caie_vm(100, exe, ext=True)

    test_ui = caie_ui(test_assemble, test_run)
    test_ui.disp()