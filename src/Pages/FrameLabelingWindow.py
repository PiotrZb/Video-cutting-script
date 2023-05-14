import customtkinter as ctk
import os
import cv2 as cv
from src.settings import CLASS_ID, IMAGE_FILE_EXTENSIONS, path_manager


class FrameLabelingWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        # Window settings
        self._WINDOW_WIDTH = 530
        self._WINDOW_HEIGHT = 250

        self.geometry(f'{self._WINDOW_WIDTH}x{self._WINDOW_HEIGHT}')
        self.resizable(False, False)
        self.title('Frame labeling tool')
        self.grab_set()  # setting focus on new window

        self.files = self.load_frames()
        self.files.sort()
        self.selected_file = None
        self.frame = None
        self.frame_with_rect = None
        self.final_frame = None
        self.dragging_active = False
        self.rect_color = (0, 255, 0)
        self.rect_top_left = None
        self.rect_bottom_right = None
        self.changes_saved = True
        self.labels = []
        self.selected_class_id = list(CLASS_ID.keys())[0]

        # Widgets
        self.exit_btn = ctk.CTkButton(master=self, text='Exit',
                                      font=ctk.CTkFont(size=20),
                                      width=150, height=30,
                                      command=self.exit_btn_onclick)
        self.next_btn = ctk.CTkButton(master=self, text='>',
                                      font=ctk.CTkFont(size=20),
                                      width=150, height=30,
                                      command=self.next_btn_onclick)
        self.save_btn = ctk.CTkButton(master=self, text='Save',
                                      font=ctk.CTkFont(size=20),
                                      width=150, height=30,
                                      command=self.save_label_onclick)
        self.clear_btn = ctk.CTkButton(master=self, text='Clear',
                                       font=ctk.CTkFont(size=20),
                                       width=150, height=30,
                                       command=self.clear_btn_onclick)
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

        self.cm_box_class_id = ctk.CTkComboBox(master=self, values=list(CLASS_ID.keys()), state='readonly',
                                               command=self.cmbox_callback_select_class,
                                               width=200, justify='center')
        self.cm_box_class_id.set(self.selected_class_id)

        self.label_class_id = ctk.CTkLabel(master=self, text=f'Selected class id')

        self.exit_btn.grid(row=3, column=3, pady=15, padx=5)
        self.previous_btn.grid(row=2, column=1, pady=15, padx=5)
        self.load_btn.grid(row=2, column=2, pady=15, padx=5)
        self.next_btn.grid(row=2, column=3, pady=15, padx=5)
        self.save_btn.grid(row=3, column=1, pady=15, padx=5)
        self.clear_btn.grid(row=3, column=2, pady=15, padx=5)
        self.label_class_id.grid(row=4, column=1, pady=15)
        self.cm_box_class_id.grid(row=4, column=2, pady=15)
        self.cm_box.grid(row=1, column=1, pady=15, padx=15, columnspan=3)

        # Key Binds
        self.bind('<KP_Left>', self.previous_btn_onclick())
        self.bind('<KP_Right>', self.next_btn_onclick())

    # Methods
    def mouse_callback(self, event, x, y, flags, param):

        # TODO fix for unix clicking btn
        if event == cv.EVENT_LBUTTONDOWN:
            self.dragging_active = True
            self.rect_top_left = (x, y)

        elif event == cv.EVENT_LBUTTONUP:
            self.dragging_active = False

            if self.selected_class_id != '':
                self.changes_saved = False
                self.rect_bottom_right = (x, y)
                self.frame_with_rect = self.final_frame.copy()

                cv.rectangle(self.frame_with_rect, self.rect_top_left, self.rect_bottom_right, self.rect_color, 2)
                self.final_frame = self.frame_with_rect
                self.frame_with_rect = self.frame
                cv.imshow('Frame', self.final_frame)

                # checking if corners are correctly defined
                if self.rect_top_left[0] > self.rect_bottom_right[0]: # x are switched
                    top_left = (self.rect_bottom_right[0], self.rect_top_left[1])
                    bottom_right = (self.rect_top_left[0], self.rect_bottom_right[1])
                    self.rect_top_left = top_left
                    self.rect_bottom_right = bottom_right

                if self.rect_top_left[1] > self.rect_bottom_right[1]: # y are switched
                    top_left = (self.rect_top_left[0], self.rect_bottom_right[1])
                    bottom_right = (self.rect_bottom_right[0], self.rect_top_left[1])
                    self.rect_top_left = top_left
                    self.rect_bottom_right = bottom_right

                frame_shape = self.frame.shape
                width = abs(self.rect_bottom_right[0] - self.rect_top_left[0]) / frame_shape[1]
                height = abs(self.rect_bottom_right[1] - self.rect_top_left[1]) / frame_shape[0]
                centerx = (self.rect_top_left[0] + (self.rect_bottom_right[0] - self.rect_top_left[0]) / 2) / \
                          frame_shape[1]
                centery = (self.rect_top_left[1] + (self.rect_bottom_right[1] - self.rect_top_left[1]) / 2) / \
                          frame_shape[0]

                self.labels.append([CLASS_ID[self.selected_class_id], centerx, centery, width, height])
            else:
                self.frame_with_rect = self.final_frame.copy()
                cv.imshow('Frame', self.final_frame)

        elif event == cv.EVENT_MOUSEMOVE and self.dragging_active:
            self.frame_with_rect = self.final_frame.copy()
            cv.rectangle(self.frame_with_rect, self.rect_top_left, (x, y), self.rect_color, 3)
            cv.imshow('Frame', self.frame_with_rect)

    def load_frames(self):
        return [file for file in os.listdir(path_manager.get_frames_destination_path)
                if file.endswith(IMAGE_FILE_EXTENSIONS)]

    def clear_all(self):
        self.labels.clear()
        self.final_frame = self.frame.copy()
        self.frame_with_rect = self.frame.copy()
        self.rect_top_left = None
        self.rect_bottom_right = None
        self.changes_saved = True

    # OnClick methods

    def clear_btn_onclick(self):
        self.clear_all()
        cv.imshow('Frame', self.frame)

    def save_label_onclick(self):
        if self.frame is not None and not self.changes_saved:
            file_name = self.selected_file.split('.')[0]

            with open(f'{path_manager.get_labels_destination_path}/{file_name}.txt', 'w') as file:
                for label in self.labels:
                    string_to_save = str(label[0]) + ' ' + str(label[1]) + ' ' + str(label[2]) + ' ' + str(
                        label[3]) + ' ' + str(label[4]) + '\n'

                    file.write(string_to_save)

            self.changes_saved = True

    def load_btn_onclick(self):
        if self.selected_file is not None:
            frame_path = path_manager.set_current_frame_path(self.selected_file)
            self.frame = cv.imread(frame_path)
            self.clear_all()
            cv.imshow('Frame', self.frame)
            cv.setMouseCallback('Frame', self.mouse_callback)

    def previous_btn_onclick(self):
        if self.selected_file is not None:
            current_frame_index = self.files.index(self.selected_file)
            if current_frame_index > 0:
                self.selected_file = self.files[current_frame_index - 1]
                path = path_manager.get_frames_destination_path + '\\' + self.selected_file
                self.frame = cv.imread(path)
                self.cm_box.set(self.selected_file)
                self.clear_all()
                cv.imshow('Frame', self.frame)
                cv.setMouseCallback('Frame', self.mouse_callback)

    def next_btn_onclick(self):
        if self.selected_file is not None:
            current_frame_index = self.files.index(self.selected_file)
            if current_frame_index < len(self.files) - 1:
                self.selected_file = self.files[current_frame_index + 1]
                path = path_manager.get_frames_destination_path + '\\' + self.selected_file
                self.frame = cv.imread(path)
                self.cm_box.set(self.selected_file)
                self.clear_all()
                cv.imshow('Frame', self.frame)
                cv.setMouseCallback('Frame', self.mouse_callback)

    def exit_btn_onclick(self):
        cv.destroyAllWindows()
        self.destroy()

    def cmbox_callback(self, selected):
        self.selected_file = selected

    def cmbox_callback_select_class(self, selected):
        self.selected_class_id = selected
