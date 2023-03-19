import cv2 as cv
import customtkinter as ctk
from pytube import YouTube
from pathlib import Path
import os

LOCAL_PATH = Path(__file__).parent.absolute().__str__()

SYSTEM_NAME = os.name

SAVE_FILES_DESTINATION_PATH = LOCAL_PATH
SAVE_WRONG_URL_DESTINATION_PATH = LOCAL_PATH
URL_FILE_PATH = LOCAL_PATH
SAVE_FRAMES_DESTINATION_PATH = LOCAL_PATH
VIDEOS_FILES_PATH = LOCAL_PATH

if SYSTEM_NAME == 'nt':
    SAVE_FILES_DESTINATION_PATH = LOCAL_PATH + '\\Downloads'
    SAVE_WRONG_URL_DESTINATION_PATH = LOCAL_PATH + '\\Res\\wrong_url_list.txt'
    URL_FILE_PATH = LOCAL_PATH + '\\Res\\url_list.txt'
    SAVE_FRAMES_DESTINATION_PATH = LOCAL_PATH + '\\Frames'
    # TODO PATH TO CHANGE
    VIDEOS_FILES_PATH = LOCAL_PATH + '\\Videos\\test_file.mp4'
elif SYSTEM_NAME == 'posix':
    SAVE_FILES_DESTINATION_PATH = LOCAL_PATH + '/Downloads'
    SAVE_WRONG_URL_DESTINATION_PATH = LOCAL_PATH + '/Res/wrong_url_list.txt'
    URL_FILE_PATH = LOCAL_PATH + '/Res/url_list.txt'
    SAVE_FRAMES_DESTINATION_PATH = LOCAL_PATH + '/Frames'
    # TODO PATH TO CHANGE
    VIDEOS_FILES_PATH = LOCAL_PATH + '/Videos/test_file.mp4'
else:
    print("Your system is not supported")
    exit()

MENU_OPTIONS = {
    '1': 'Load all videos from .txt file.',
    '2': 'Cut frames from videos.'
}


def clear_console():
    if SYSTEM_NAME == 'posix':
        _ = os.system('clear')
    elif SYSTEM_NAME == 'nt':
        _ = os.system('cls')
    else:
        return False


def contains_certain_characters(response):
    characters = set("".join(MENU_OPTIONS.keys()))
    return all(char in characters for char in response)


def show_menu():
    print("Select option:")
    for (key, value) in MENU_OPTIONS.items():
        print(f"{key}. {value}")
    resposne = input("Enter value: ")
    while True:
        if contains_certain_characters(resposne):
            break
        else:
            print("Invalid option")
            resposne = input("Enter value: ")
    clear_console()
    return resposne


def displayer(cap):
    """
    cap -> cv2.VideoCapture object
    Function displays movie in opencv window.
    """

    while True:
        ret, frame = cap.read()

        if ret:
            cv.imshow('Movie', frame)
            # press q to quit
            if cv.waitKey(25) == ord('q'):
                break
        else:
            break

    cap.release()
    cv.destroyAllWindows()


def load_all_from_txt(file_path=URL_FILE_PATH,
                      destination_path=SAVE_FILES_DESTINATION_PATH):
    """
    file_path -> path to the file with url addresses
    destination_path -> path to the file where movies will be store
    Function downloads movies from urls that are stored in txt file.
    """

    wrong_urls = []
    used_urls = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines_count = len(lines)
        for index, url in enumerate(lines):
            if url not in used_urls:
                try:
                    movie = YouTube(url)
                    print(f"{index + 1} : {lines_count} -> Downloading file: \""
                          f"{movie.streams[0].title}\"")
                    stream = movie.streams.get_highest_resolution()
                    stream.download(
                        filename_prefix=f'{index}. ',
                        output_path=destination_path)
                    used_urls.append(url)
                except Exception as exc:
                    wrong_urls.append(url)
                    print(f"Exception occurred at line {index + 1}: {url} ")
                    print(exc)
            else:
                print(f"Duplicat occurred at line {index + 1}: {url}")

    file.close()

    with open(SAVE_WRONG_URL_DESTINATION_PATH, 'w') as file:
        file.writelines(wrong_urls)

    file.close()


def cut_video(time_span, file_path, destination_path):
    """
    time_span -> tuple (start time, stop time) in seconds
    file_path -> path to the .mp4 file
    destination_path -> path to the folder where frames will be store
    some description here
    """

    # TODO
    # iterowanie filmow w danej sciezce

    start_time, stop_time = time_span
    cap = cv.VideoCapture(file_path)
    fps = int(cap.get(cv.CAP_PROP_FPS))  # frames per seconds
    first_frame = fps * start_time
    last_frame = fps * stop_time

    for frame_index in range(0, last_frame):
        read_success, frame = cap.read()

        if read_success:
            if frame_index > first_frame:
                # PNG or JPG format
                path = destination_path + f'/frame{frame_index}.png'
                cv.imwrite(path, frame)
            cv.waitKey(5)
    cap.release()


class CutWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry('700x500')
        self.resizable(False, False)
        self.title('Extract frames')
        self.grab_set()  # setting focus on new window


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
        self.text_box.insert('1.0', ''.join(self.urls))  # init textBox with ulrs from file
        self.download_btn = ctk.CTkButton(master=self, text='Download all', font=ctk.CTkFont(size=20),
                                          command=self.download_btn_onclick, width=200, height=50)
        self.exit_btn = ctk.CTkButton(master=self, text='Exit', font=ctk.CTkFont(size=20),
                                      command=self.exit_btn_onclick, width=200, height=50)
        self.save_btn = ctk.CTkButton(master=self, text='Save', font=ctk.CTkFont(size=20),
                                      command=self.save_btn_onclick, width=200, height=50)
        self.text_box2 = ctk.CTkTextbox(master=self, height=100)
        self.text_box2.insert('1.0', ''.join(self.wrong_urls))
        self.label1 = ctk.CTkLabel(master=self, text='Wrong urls', font=ctk.CTkFont(size=20, weight='bold'), height=10)
        self.label2 = ctk.CTkLabel(master=self, text='Urls', font=ctk.CTkFont(size=20, weight='bold'), height=10)
        self.label3 = ctk.CTkLabel(master=self, text='Terminal', font=ctk.CTkFont(size=20, weight='bold'), height=10)
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

    # methods
    def load_urls(self):
        try:
            with open(URL_FILE_PATH, 'r') as file:
                urls = file.readlines()
            with open(SAVE_WRONG_URL_DESTINATION_PATH, 'r') as file:
                wrong_urls = file.readlines()
        except Exception as e:
            self.update_terminal('Wrong file path (load_urls)')
            self.update_terminal(str(e))
        return [x for x in urls if x != '\n'], [x for x in wrong_urls if x != '\n']

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

        with open(SAVE_WRONG_URL_DESTINATION_PATH, 'w') as file:
            file.writelines([x for x in self.wrong_urls if x != '\n'])

        with open(URL_FILE_PATH, 'w') as file:
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
                    self.update_terminal(f"{index + 1} : {lines_count} -> Downloading file: {movie.streams[0].title}")
                    stream = movie.streams.get_highest_resolution()
                    stream.download(
                        filename_prefix=f'{index}. ',
                        output_path=SAVE_FILES_DESTINATION_PATH)
                    used_urls.append(url)
                except Exception as exc:
                    self.wrong_urls.append(url + '\n')
                    self.update_terminal(f'Exception occurred at line {index + 1}: {url}')
                    self.update_terminal(str(exc))
            else:
                self.update_terminal(f'Duplicat occurred at line {index + 1}: {url}')

        self.text_box2.insert('1.0', ''.join(self.wrong_urls))


class Menu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry('400x500')
        self.resizable(False, False)
        self.title('Menu')

        # widgets
        self.download_btn = ctk.CTkButton(master=self, text='Download videos', font=ctk.CTkFont(size=30),
                                          command=self.download_btn_onclick)
        self.cut_btn = ctk.CTkButton(master=self, text='Cut video', font=ctk.CTkFont(size=30),
                                     command=self.cut_btn_onclick)
        self.exit_btn = ctk.CTkButton(master=self, text='Exit', font=ctk.CTkFont(size=30),
                                      command=self.exit_btn_onclick)
        self.label = ctk.CTkLabel(master=self, text='MENU', font=ctk.CTkFont(size=90, weight='bold'))

        # layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.download_btn.grid(row=1, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.cut_btn.grid(row=2, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.exit_btn.grid(row=3, sticky=ctk.EW, padx=40, pady=15, ipady=15)
        self.label.grid(row=0, sticky=ctk.N, pady=30)

        # other windows
        self.download_win = None
        self.cut_win = None

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


class App:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.menu = Menu()

    def run(self):
        self.menu.mainloop()


def main():
    program = App()
    program.run()


if __name__ == "__main__":
    main()
