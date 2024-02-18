import customtkinter as ctk

class StatusFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.default_regs = ['ACC', 'BR', 'PC', 'IX', 'flag']
        self.labels = []
        self.vals = []

        self.logo_label = ctk.CTkLabel(
            self, text="Status", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(
            row=0, column=0, padx=(0, 10), pady=(10, 0), columnspan=2,
            sticky="s")
        self.register_label = ctk.CTkLabel(
            self, text="Register", font=ctk.CTkFont(size=18, weight="bold"))
        self.register_label.grid(
            row=1, column=0, padx=(10, 50), pady=(10, 10), sticky="s")
        self.value_label = ctk.CTkLabel(
            self, text="Value", font=ctk.CTkFont(size=18, weight="bold"))
        self.value_label.grid(
            row=1, column=1, padx=20, pady=(10, 10), sticky="s")
        self.init_status()

    def init_status(self):
        for index, reg in enumerate(self.default_regs):
            self.labels.append(ctk.CTkLabel(
                self, text=reg, font=ctk.CTkFont(
                    family='Ubuntu Mono', size=16)))
            self.vals.append(ctk.CTkLabel(
                self, text = '0', font=ctk.CTkFont(
                    family='Ubuntu Mono', size=16)))
            self.labels[-1].grid(
                row=2+index, column=0, padx=0, pady=(5, 5), sticky="s")
            self.vals[-1].grid(
                row=2+index, column=1, padx=(10, 10), pady=(5, 5), sticky="s")
    
    def update(self, regs: dict):
        for index, value in enumerate(list(regs.values())):
            self.vals[index].configure(text=f'{value}')