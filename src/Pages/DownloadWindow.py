import customtkinter as ctk
from pytube import YouTube
from src.settings import path_manager


class DownloadWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.geometry('700x600')
        self.resizable(False, False)
        self.title('Download videos')
        self.grab_set()  # setting focus on new window

        self.urls, self.wrong_urls = self.load_urls()

        # widgets
        self.text_box = ctk.CTkTextbox(master=self, height=150)
        self.text_box.insert('1.0', ''.join(
            self.urls))  # init textBox with ulrs from file
        self.download_btn = ctk.CTkButton(master=self, text='Download all',
                                          font=ctk.CTkFont(size=20),
                                          command=self.download_btn_onclick,
                                          width=200, height=50)
        self.exit_btn = ctk.CTkButton(master=self, text='Exit',
                                      font=ctk.CTkFont(size=20),
                                      command=self.exit_btn_onclick, width=200,
                                      height=50)
        self.save_btn = ctk.CTkButton(master=self, text='Save',
                                      font=ctk.CTkFont(size=20),
                                      command=self.save_btn_onclick, width=200,
                                      height=50)
        self.text_box2 = ctk.CTkTextbox(master=self, height=100)
        self.text_box2.insert('1.0', ''.join(self.wrong_urls))
        self.label1 = ctk.CTkLabel(master=self, text='Wrong urls',
                                   font=ctk.CTkFont(size=20, weight='bold'),
                                   height=10)
        self.label2 = ctk.CTkLabel(master=self, text='Urls',
                                   font=ctk.CTkFont(size=20, weight='bold'),
                                   height=10)
        self.label3 = ctk.CTkLabel(master=self, text='Terminal',
                                   font=ctk.CTkFont(size=20, weight='bold'),
                                   height=10)
        self.terminal = ctk.CTkTextbox(master=self, height=100)
        self.terminal.configure(state='disabled')

        # layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.label2.grid(row=0, sticky=ctk.S, pady=5)
        self.text_box.grid(row=1, sticky=ctk.NSEW, pady=10, padx=10)
        self.label1.grid(row=2, sticky=ctk.S)
        self.text_box2.grid(row=3, sticky=ctk.NSEW, pady=10, padx=10)
        self.label3.grid(row=4, sticky=ctk.S)
        self.terminal.grid(row=5, sticky=ctk.NSEW, pady=10, padx=10)
        self.download_btn.grid(row=1, column=1, padx=20)
        self.save_btn.grid(row=3, column=1, padx=20)
        self.exit_btn.grid(row=5, column=1, padx=20)

        self.protocol("WM_DELETE_WINDOW", self.exit_btn_onclick)

    # methods
    def load_urls(self):
        try:
            with open(path_manager.get_url_file_path, 'r') as file:
                urls = file.readlines()
            with open(path_manager.get_wrong_url_destination_path, 'r') as file:
                wrong_urls = file.readlines()
        except Exception as e:
            self.update_terminal('Wrong file path (load_urls)')
            self.update_terminal(str(e))
        return [x for x in urls if x != '\n'], [x for x in wrong_urls if
                                                x != '\n']

    def update_terminal(self, message):
        self.terminal.configure(state='normal')
        self.terminal.insert(ctk.END, message + '\n')
        self.terminal.configure(state='disabled')

    # onClick methods
    def exit_btn_onclick(self):
        self.destroy()

    def save_btn_onclick(self):
        self.urls = self.text_box.get('1.0', ctk.END).splitlines(True)
        self.wrong_urls = self.text_box2.get('1.0', ctk.END).splitlines(True)

        with open(path_manager.get_wrong_url_destination_path, 'w') as file:
            file.writelines([x for x in self.wrong_urls if x != '\n'])

        with open(path_manager.get_url_file_path, 'w') as file:
            file.writelines([x for x in self.urls if x != '\n'])

    def download_btn_onclick(self):
        lines = self.text_box.get('1.0', ctk.END).split('\n')
        self.text_box2.delete('1.0', ctk.END)

        used_urls = []

        lines_count = len(lines)
        for index, url in enumerate(lines):
            if url not in used_urls:
                try:
                    movie = YouTube(url)

                    self.update_terminal(
                        f"{index + 1} : {lines_count} -> Downloading file:"
                        f" {movie.streams[0].title}")
                    stream = movie.streams.get_highest_resolution()
                    stream.download(
                        filename_prefix=f'{index}. ',
                        output_path=path_manager.get_files_destination_path)
                    used_urls.append(url)
                except Exception as exc:
                    self.wrong_urls.append(url + '\n')
                    self.update_terminal(
                        f'Exception occurred at line {index + 1}: {url}')
                    self.update_terminal(str(exc))
            else:
                self.update_terminal(
                    f'Duplicat occurred at line {index + 1}: {url}')

        self.text_box2.insert('1.0', ''.join(self.wrong_urls))
