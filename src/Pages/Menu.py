import customtkinter as ctk
from .CutWindow import CutWindow
from .DownloadWindow import DownloadWindow
from .FrameLabelingWindow import FrameLabelingWindow


class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('400x600')
        self.resizable(False, False)
        self.title('Menu')

        # widgets
        self.download_btn = ctk.CTkButton(master=self, text='Download videos',
                                          font=ctk.CTkFont(size=30),
                                          command=self.download_btn_onclick)
        self.cut_btn = ctk.CTkButton(master=self, text='Cut video',
                                     font=ctk.CTkFont(size=30),
                                     command=self.cut_btn_onclick)
        self.label_btn = ctk.CTkButton(master=self, text='Labeling tool',
                                       font=ctk.CTkFont(size=30),
                                       command=self.label_btn_onclick)
        self.exit_btn = ctk.CTkButton(master=self, text='Exit',
                                      font=ctk.CTkFont(size=30),
                                      command=self.exit_btn_onclick)
        self.label = ctk.CTkLabel(master=self, text='MENU',
                                  font=ctk.CTkFont(size=90, weight='bold'))

        # layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.download_btn.grid(row=1, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.cut_btn.grid(row=2, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.label_btn.grid(row=3, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.exit_btn.grid(row=4, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.label.grid(row=0, sticky=ctk.N, pady=30)

        # other windows
        self.download_win = None
        self.cut_win = None
        self.label_win = None

        self.protocol("WM_DELETE_WINDOW", self.exit_btn_onclick)

        self.bind('<Escape>', lambda event: self.exit_btn_onclick())

    # onClick methods
    def exit_btn_onclick(self):
        self.destroy()

    def cut_btn_onclick(self):
        if self.cut_win is None or not self.cut_win.winfo_exists():
            self.cut_win = CutWindow()
        else:
            self.cut_win.focus()

    def download_btn_onclick(self):
        if self.download_win is None or not self.download_win.winfo_exists():
            self.download_win = DownloadWindow()
        else:
            self.download_win.focus()

    def label_btn_onclick(self):
        if self.label_win is None or not self.label_win.winfo_exists():
            self.label_win = FrameLabelingWindow()
        else:
            self.label_win.focus()

