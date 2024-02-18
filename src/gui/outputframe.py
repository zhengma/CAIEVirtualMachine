import customtkinter as ctk

class OutputFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.output = ctk.CTkTextbox(
            master=self, width=600, height=120, 
            font=('Ubuntu Mono', 16), corner_radius=0, wrap='none')
        self.output.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
    
    def append(self, text: str) -> None:
        self.output.insert('end', text)
    
    def clear(self) -> None:
        self.output.delete("0.0", "end")