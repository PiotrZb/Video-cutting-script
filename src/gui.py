import customtkinter as ctk
from src.Pages.Menu import Menu


# TODO: Clear code, new functions, files, comments and descriptions...
# TODO: Random color generator for bounding boxes. (for now every box has the same color)


class App:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.menu = Menu()

    def run(self):
        self.menu.mainloop()