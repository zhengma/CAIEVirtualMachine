import customtkinter as ctk
from gui.toolbar import Toolbar
from gui.codeframe import CodeFrame
from gui.statusframe import StatusFrame
from gui.memframe import MemFrame

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("CAIE指令集架构仿真器 v2.0")
        self.geometry(f"{1100}x{800}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(0, weight=1)
        # self.grid_rowconfigure(4, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)

        self.code_frame = CodeFrame(
            master=self, border_width=2, border_color="green")
        self.code_frame.grid(row=0, column=0, padx=(20, 40), rowspan=4,
                             sticky="nsew")

        self.toolbar = Toolbar(
            master=self
        )
        self.toolbar.grid(row=0, column=1, padx=(0, 20), pady=(0, 30),
                          sticky="nsew")

        self.status_frame = StatusFrame(
            master=self, width=400, height=100,
            border_width=2, border_color="red")
        self.status_frame.grid(row=1, column=1, padx=(0, 20), pady=(0, 30),
                               sticky="nsew")

        self.mem_frame = MemFrame(
            master=self, width=400, height=100,
            border_width=2, border_color="blue")
        self.mem_frame.grid(row=2, column=1, padx=(0, 20), pady=(0, 30),
                            sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()