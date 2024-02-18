import customtkinter as ctk

class Toolbar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.counter = 1

        btnfont = ctk.CTkFont(family="Segoe UI Emoji", size=22, weight="bold")
        txtfont = ctk.CTkFont(size=18, weight="bold")

        self.open_button = ctk.CTkButton(
            self, width=45, height=45, text="📂", font=btnfont,
            command=self.master.code_frame.open_event)
        self.save_button = ctk.CTkButton(
            self, width=45, height=45, text="💾", font=btnfont,
            command=self.generate_test)
        self.gen_button = ctk.CTkButton(
            self, width=45, height=45, text="⏺", font=btnfont,
            command=self.master.load)
        self.base_label = ctk.CTkLabel(
            self, text='Base Address: ', font=txtfont)
        self.base_entry = ctk.CTkEntry(
            self, width=60, height=40,
            placeholder_text=f'{self.master.default_base}', font=txtfont)
        self.data_label = ctk.CTkLabel(
            self, text='Data Address: ', font=txtfont)
        self.data_entry = ctk.CTkEntry(
            self, width = 60, height=40,
            placeholder_text=f'{self.master.default_data}', font=txtfont)
        self.back_button = ctk.CTkButton(
            self, width=45, height=45, text="◀", font=btnfont,
            command=self.back)
        self.single_step_button = ctk.CTkButton(
            self, width=45, height=45, text="▶", font=btnfont,
            command=self.master.next)

        self.open_button.grid(row=0, column=0, padx=2, pady=5)
        self.save_button.grid(row=0, column=1, padx=2, pady=5)
        self.gen_button.grid(row=0, column=2, padx=2, pady=5)
        self.base_label.grid(row=0, column=3, pady=5)
        self.base_entry.grid(row=0, column=4, pady=5, padx=(0, 5))
        self.data_label.grid(row=0, column=5, pady=5)
        self.data_entry.grid(row=0, column=6, pady=5, padx=(0, 5))
        self.back_button.grid(row=0, column=7, padx=2, pady=5)
        self.single_step_button.grid(row=0, column=8, padx=2, pady=5)
    
    def back(self):
        self.counter -= 1
        self.master.code_frame.hightlight(self.counter)
    
    def generate_test(self):
        if self.base_entry.get():
            print(int(self.base_entry.get()) + int(self.data_entry.get()))
        else:
            print('Empty!')