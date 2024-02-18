import customtkinter as ctk

class MemFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.labels = []
        self.vals = []

        self.logo_label = ctk.CTkLabel(
            self, text="Memory", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(
            row=0, column=0, padx=(0, 10), pady=(10, 0), columnspan=2,
            sticky="s")
        self.addr_label = ctk.CTkLabel(
            self, text="Address", font=ctk.CTkFont(size=18, weight="bold"))
        self.addr_label.grid(
            row=1, column=0, padx=(10, 50), pady=(10, 10), sticky="s")
        self.value_label = ctk.CTkLabel(
            self, text="Value", font=ctk.CTkFont(size=18, weight="bold"))
        self.value_label.grid(
            row=1, column=1, padx=20, pady=(10, 10), sticky="s")
    
    def init_mem(self, mem: list):
        for index, m in enumerate(mem):
            self.labels.append(ctk.CTkLabel(
                self, text=f'{m[0]}', font=ctk.CTkFont(
                    family='Ubuntu Mono', size=16)))
            self.vals.append(ctk.CTkLabel(
                self, text=f'{m[1]}', font=ctk.CTkFont(
                    family='Ubuntu Mono', size=16)))
            self.labels[-1].grid(
                row=2+index, column=0, padx=0, pady=(5, 5), sticky="s")
            self.vals[-1].grid(
                row=2+index, column=1, padx=(10, 10), pady=(5, 5), sticky="s")
    
    def update(self, mem: list):
        for index, m in enumerate(mem):
            self.vals[index].configure(text=f'{m[1]}')