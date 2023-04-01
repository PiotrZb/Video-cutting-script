import customtkinter as ctk
import os
import cv2 as cv
import math
import numpy as np
import threading
from src.settings import path_manager, VIDEO_FILE_EXTENSIONS


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
