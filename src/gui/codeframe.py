import customtkinter as ctk
from tkinter import filedialog as fd

class CodeFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.logo_label = ctk.CTkLabel(
            self, text="Code", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(
            row=0, column=0, padx=20, pady=(10, 10), sticky="s")
        
        self.open = ctk.CTkButton(
            self, text="Open", command=self.open_event)
        self.open.grid(row=4, column=0, padx=20, pady=10)

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
        filename = fd.askopenfilename()
        if filename:
            with open(filename, "r", encoding='utf-8') as file:
                self.code.delete("1.0", "end")  # Clear the Text widget
                self.code.insert("end", file.read())  # Insert file content
        self.code.tag_add("start", "1.0","2.0")
        self.code.tag_config("start", background="dark red", foreground="white")