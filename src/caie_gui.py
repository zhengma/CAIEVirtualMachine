import customtkinter as ctk
from gui.toolbar import Toolbar
from gui.codeframe import CodeFrame
from gui.statusframe import StatusFrame
from gui.memframe import MemFrame
from gui.outputframe import OutputFrame
from caie_vm import caie_vm
from caie_assembler import caie_assembler

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.default_base = 100
        self.default_data = 200
        self.base = None
        self.data = None
        self.filename = ''
        self.assembler = None
        self.vm = None
        self.stat = None

        # configure window
        self.title("CAIE指令集架构仿真器 v2.0")
        self.geometry(f"{1100}x{700}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_rowconfigure((1, 3), weight=0)

        self.code_frame = CodeFrame(
            master=self, border_width=2, border_color="green")
        self.code_frame.grid(
            row=1, column=0, rowspan=2, padx=(20, 40), pady=(10, 10),
            sticky="nsew")
        
        self.output_frame = OutputFrame(
            master=self, border_width=2, border_color="white")
        self.output_frame.grid(
            row=3, column=0, padx=(20, 40), pady=(0, 30), sticky="nsew")

        self.toolbar = Toolbar(
            master=self
        )
        self.toolbar.grid(
            row=0, column=0, columnspan=2, padx=(0, 20), pady=(10, 20), 
            sticky="nsew")

        self.status_frame = StatusFrame(
            master=self, width=400, height=100,
            border_width=2, border_color="red")
        self.status_frame.grid(row=1, column=1, padx=(0, 20), pady=(10, 20),
                               sticky="nsew")

        self.mem_frame = MemFrame(
            master=self, width=400, height=100,
            border_width=2, border_color="blue")
        self.mem_frame.grid(row=2, column=1, padx=(0, 20), pady=(0, 30),
                            rowspan=2, sticky="nsew")
    
    def load(self):
        self.base = (self.toolbar.base_entry.get() 
                     if self.toolbar.base_entry.get() else self.default_base)
        self.data = (self.toolbar.data_entry.get()
                     if self.toolbar.data_entry.get() else self.default_data)
        self.assembler = caie_assembler(self.filename, self.base, self.data)
        self.vm = caie_vm(self.base, self.assembler.generate(), ext=True)
        self.stat = self.vm.get_status()
        self.status_frame.update(self.stat)
        self.mem_frame.init_mem(self.vm.get_memory(
            self.base, self.data - self.base))
        self.output_frame.clear()
    
    def next(self):
        if self.vm.single_step(debugging=False):
            self.interrupt_dispatch()
            self.stat = self.vm.get_status()
            self.code_frame.highlight(self.assembler.line_number(self.stat['PC']))
            self.status_frame.update(self.vm.get_status())
            self.mem_frame.update(self.vm.get_memory(
                self.base, self.data - self.base))
    
    def interrupt_dispatch(self):
        match self.vm.get_interrupt():
            case 1:
                self.output_frame.append(self.vm.stdout())
            case 2:
                input_box = ctk.CTkInputDialog(
                    text="Feed in ONE character", title="Input")
                self.vm.stdin(ord(input_box.get_input()[0]))

if __name__ == "__main__":
    app = App()
    app.mainloop()