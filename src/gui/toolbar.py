import customtkinter as ctk

class Toolbar(ctk.CTkFrame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.back_button = ctk.CTkButton(
            self, width=30, text="◀", command=self.back)
        self.back_button.grid(row=0, column=0, padx=2, pady=5)
        self.single_step_button = ctk.CTkButton(
            self, width=30, text="▶", command=self.single_step)
        self.single_step_button.grid(row=0, column=1, padx=2, pady=5)
    
    def back(self):
        print("Back!")
    
    def single_step(self):
        print("Forward!")