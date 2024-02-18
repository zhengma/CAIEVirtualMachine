import customtkinter as ctk
from tkinter import filedialog as fd
from os import path

class CodeFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.set_title()

        self.code = ctk.CTkTextbox(
            master=self, width=600, height=480, 
            font=('Ubuntu Mono', 16), corner_radius=0, wrap='none')
        self.code.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.code.insert("0.0", f"""
{'*'*10} CAIE指令集架构仿真器 v2.0 {'*'*10}
*{' '*45}*
*{' '*20}马 正 {' '*19}*
*{' '*6} 渊学通教育广州分校, 上海科桥教育 {' '*5}*
{'*'*47}
""")
    
    def open_event(self):
        self.master.filename = fd.askopenfilename()
        if self.master.filename:
            with open(self.master.filename, "r", encoding='utf-8') as file:
                self.code.delete("1.0", "end")  # Clear the Text widget
                self.code.insert("end", file.read())  # Insert file content
                self.set_title(path.basename(self.master.filename))
        self.highlight()
    
    def highlight(self, line=1):
        self.code.tag_delete('current')
        self.code.tag_add('current', f'{line}.0', f'{line+1}.0')
        self.code.tag_config('current', background="dark red", foreground="white")
    
    def set_title(self, content='Code'):
        self.title = ctk.CTkLabel(
            self, text=content, font=ctk.CTkFont(size=20, weight="bold"))
        self.title.grid(
            row=0, column=0, padx=20, pady=(10, 0), sticky="s")