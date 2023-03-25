import customtkinter as ctk
import os
from pathmanager import PathManager
from pytube import YouTube
import cv2 as cv
import math
import numpy as np
import threading

VIDEO_FILE_EXTENSIONS = ('.mp4', '.m4v', '.m4p')
IMAGE_FILE_EXTENSIONS = ('.jpg', 'jpeg', '.png')

path_manager = PathManager()


class FrameLabelingWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        # Window settings
        self._WINDOW_WIDTH = 530
        self._WINDOW_HEIGHT = 180

        self.geometry(f'{self._WINDOW_WIDTH}x{self._WINDOW_HEIGHT}')
        self.resizable(False, False)
        self.title('Frame labeling tool')
        self.grab_set()  # setting focus on new window

        self.files = self.load_frames()
        self.selected_file = None

        # Widgets
        self.exit_btn = ctk.CTkButton(master=self, text='Exit',
                                      font=ctk.CTkFont(size=20),
                                      width=150, height=30,
                                      command=self.exit_btn_onclick)
        self.next_btn = ctk.CTkButton(master=self, text='>',
                                      font=ctk.CTkFont(size=20),
                                      width=150, height=30,
                                      command=self.next_btn_onclick)
        self.previous_btn = ctk.CTkButton(master=self, text='<',
                                          font=ctk.CTkFont(size=20),
                                          width=150, height=30,
                                          command=self.previous_btn_onclick)
        self.load_btn = ctk.CTkButton(master=self, text='Load',
                                      font=ctk.CTkFont(size=20),
                                      width=150, height=30,
                                      command=self.load_btn_onclick)
        self.cm_box = ctk.CTkComboBox(master=self, values=self.files,
                                      state='readonly',
                                      command=self.cmbox_callback,
                                      width=500)
        self.cm_box.set('')

        # Layout
        self.exit_btn.grid(row=3, column=2, pady=15, padx=5)
        self.previous_btn.grid(row=2, column=1, pady=15, padx=5)
        self.load_btn.grid(row=2, column=2, pady=15, padx=5)
        self.next_btn.grid(row=2, column=3, pady=15, padx=5)
        self.cm_box.grid(row=1, column=1, pady=15, padx=15, columnspan=3)

    # Methods

    def load_frames(self):
        return [file for file in os.listdir(path_manager.get_frames_destination_path)
                if file.endswith(IMAGE_FILE_EXTENSIONS)]

    # OnClick methods

    def load_btn_onclick(self):
        frame_path = path_manager.get_frames_destination_path + '\\' + self.selected_file
        self.frame = cv.imread(frame_path)
        cv.imshow('Frame',self.frame)

    def previous_btn_onclick(self):
        pass

    def next_btn_onclick(self):
        pass

    def exit_btn_onclick(self):
        cv.destroyAllWindows()
        self.destroy()

    def cmbox_callback(self, selected):
        self.selected_file = selected


class CutWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        # Window settings
        self._WINDOW_WIDTH = 700
        self._WINDOW_HEIGHT = 600

        self.geometry(f'{self._WINDOW_WIDTH}x{self._WINDOW_HEIGHT}')
        self.resizable(False, False)
        self.title('Extract frames tool')
        self.grab_set()  # setting focus on new window

        # Variables Video
        self.files_path = []
        self.cap = None
        self.video_start_time_min = 0
        self.video_end_time_max = 0
        self.fps = 0
        self.frames = 0

        # Variables Slider settings
        self.slider_start_min = 0
        self.slider_start_max = 0
        self.slider_end_min = 1
        self.slider_end_max = 0

        # Variables Frames
        self.max_frame_width = 400
        self.start_frame_image = None
        self.end_frame_image = None

        for file in os.listdir(path_manager.get_files_destination_path):
            if file.endswith(VIDEO_FILE_EXTENSIONS):
                self.files_path.append(file)

        self.files = self.files_path
        self.selected_file = ''

        # Widgets
        # layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Combo Box
        self.cm_box = ctk.CTkComboBox(master=self, values=self.files,
                                      state='readonly',
                                      command=self.cmbox_callback,
                                      width=500)
        self.cm_box.set('')
        self.cm_box.grid(row=0, column=0, pady=20, padx=20, columnspan=2)

        # Text boxes
        self.start_time_txtbox = ctk.CTkTextbox(master=self, height=10)
        self.end_time_txtbox = ctk.CTkTextbox(master=self, height=10)

        # Sliders
        self.slider_start = ctk.CTkSlider(master=self, from_=self.slider_start_min, to=self.slider_start_max,
                                          command=self.slider_start_event, width=self._WINDOW_WIDTH - 200,
                                          state='disabled')
        self.slider_end = ctk.CTkSlider(master=self, from_=self.slider_end_min, to=self.slider_end_max,
                                        command=self.slider_end_event, width=self._WINDOW_WIDTH - 200,
                                        state='disabled')

        self.slider_start.grid(row=2, column=0, pady=20, padx=20, columnspan=2)
        self.slider_end.grid(row=4, column=0, pady=20, padx=20, columnspan=2)

        self.label_start_time = ctk.CTkLabel(master=self, text=f'Start time {0} s')
        self.label_end_time = ctk.CTkLabel(master=self, text=f'End time {0} s')

        self.label_start_time.grid(row=1, columnspan=2, pady=10, padx=20, sticky=ctk.S)
        self.label_end_time.grid(row=3, columnspan=2, pady=10, padx=20, sticky=ctk.S)

        # Buttons
        self.extract_frames_btn = ctk.CTkButton(master=self,
                                                text='Extract frames',
                                                font=ctk.CTkFont(size=20),
                                                width=200, height=50,
                                                command=self.extract_frames_btn_onclick)
        self.exit_btn = ctk.CTkButton(master=self, text='Exit',
                                      font=ctk.CTkFont(size=20),
                                      width=200, height=50,
                                      command=self.exit_btn_onclick)

        self.extract_frames_btn.grid(row=5, column=0, columnspan=2, pady=20,
                                     padx=20)
        self.exit_btn.grid(row=6, column=1, pady=20, padx=20)

        # Progress Bar
        self.progress_bar = ctk.CTkProgressBar(master=self,
                                               height=20, width=self._WINDOW_WIDTH - 200)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=7, column=0, pady=20, padx=20, columnspan=2)

        self.protocol("WM_DELETE_WINDOW", self.exit_btn_onclick)

    # methods
    def read_current_frame(self, frame_position=0):
        self.cap.set(cv.CAP_PROP_POS_FRAMES, frame_position)
        read_success, frame = self.cap.read()
        if read_success:
            width = self.max_frame_width
            height = int((frame.shape[0] / frame.shape[1]) * frame.shape[0])
            dsize = (width, height)
            return cv.resize(frame, dsize)

    def update_frames_window(self):
        frames = np.concatenate((self.start_frame_image, self.end_frame_image), axis=1)
        cv.imshow('Frames window', frames)

    def configure_slider(self):
        # Set slider settings
        self.video_end_time_max = math.floor(self.frames / self.fps)
        self.slider_start_max = self.video_end_time_max - 1
        self.slider_end_max = self.video_end_time_max
        self.slider_start.configure(state='normal', to=self.slider_start_max, number_of_steps=self.slider_start_max)
        self.slider_end.configure(state='normal', to=self.video_end_time_max, number_of_steps=self.slider_start_max)
        self.slider_start.set(0)
        self.slider_end.set(self.video_end_time_max)
        self.label_end_time.configure(text=f'End time {self.slider_end.get()} s')

    def release_cap(self):
        if self.cap is not None:
            self.cap.release()

    def cmbox_callback(self, choice):
        self.selected_file = choice
        self.release_cap()
        try:
            # Get video data
            self.cap = cv.VideoCapture(
                path_manager.get_files_destination_path + '/' + self.selected_file)

            self.fps = int(self.cap.get(cv.CAP_PROP_FPS))
            self.frames = self.cap.get(cv.CAP_PROP_FRAME_COUNT)

            # Set slider settings
            self.configure_slider()

            # Create Images
            cv.destroyAllWindows()
            cv.namedWindow('Frames window', 0)
            self.start_frame_image = self.read_current_frame(0)
            self.end_frame_image = self.read_current_frame(self.frames - 1)
            self.update_frames_window()
        except Exception as exc:
            print(exc)

    def extract_frames(self):
        try:
            first_frame = self.slider_start.get() * self.fps
            last_frame = self.slider_end.get() * self.fps
            total_frames = last_frame - first_frame
            self.slider_end.configure(state='disabled')
            self.slider_start.configure(state='disabled')
            self.cap.set(cv.CAP_PROP_POS_FRAMES, first_frame)
            for frame_index in range(int(first_frame), int(last_frame)):
                read_success, frame = self.cap.read()
                self.progress_bar.set((frame_index - first_frame + 1) / total_frames)
                if read_success:
                    if frame_index > first_frame:
                        # 	# PNG or JPG format
                        path = path_manager.get_frames_destination_path + f'/frame{frame_index}.png'
                        cv.imwrite(path, frame)
                    # cv.waitKey(5)
            self.slider_end.configure(state='normal')
            self.slider_start.configure(state='normal')
        except Exception as exc:
            print(exc)

    # Events Slider
    def slider_start_event(self, value):
        self.slider_end_min = value + 1
        if value >= self.slider_end.get():
            self.slider_end.set(self.slider_end_min)
            self.label_end_time.configure(text=f'End time {self.slider_end_min} s')
            self.end_frame_image = self.read_current_frame(self.slider_end_min * self.fps)

        self.label_start_time.configure(text=f'Start time {value} s')
        self.start_frame_image = self.read_current_frame(value * self.fps)
        self.update_frames_window()

    def slider_end_event(self, value):
        if value <= self.slider_start.get():
            self.slider_end.set(self.slider_end_min)
            self.label_end_time.configure(text=f'End time {self.slider_end_min} s')
            self.end_frame_image = self.read_current_frame(self.slider_end_min * self.fps)
            self.update_frames_window()
        else:
            self.label_end_time.configure(text=f'End time {value} s')
            self.end_frame_image = self.read_current_frame(value * self.fps)
            self.update_frames_window()

    # onClick methods
    def exit_btn_onclick(self):
        self.destroy()
        self.release_cap()
        cv.destroyAllWindows()

    def extract_frames_btn_onclick(self):
        self.progress_bar.set(0)
        thread_extract_frames = threading.Thread(target=self.extract_frames())
        thread_extract_frames.start()
        thread_extract_frames.join()


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


class App:
    def __init__(self):
        ctk.set_appearance_mode('dark')
        ctk.set_default_color_theme('dark-blue')

        self.menu = Menu()

    def run(self):
        self.menu.mainloop()
