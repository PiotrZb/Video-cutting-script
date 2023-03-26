import os
from pathlib import Path


class PathManager:
    def __init__(self):
        self._LOCAL_PATH = Path(__file__).parent.absolute().__str__()

        self._CURRENT_SYSTEM_NAME = os.name

        self._SAVE_FILES_DESTINATION_PATH = self._LOCAL_PATH
        self._SAVE_WRONG_URL_DESTINATION_PATH = self._LOCAL_PATH
        self._URL_FILE_PATH = self._LOCAL_PATH
        self._SAVE_FRAMES_DESTINATION_PATH = self._LOCAL_PATH
        self._VIDEOS_FILES_PATH = self._LOCAL_PATH

        if self._CURRENT_SYSTEM_NAME == 'nt':
            self._SAVE_FILES_DESTINATION_PATH += '\\Downloads'
            self._SAVE_WRONG_URL_DESTINATION_PATH += '\\Res\\wrong_url_list.txt'
            self._URL_FILE_PATH += '\\Res\\url_list.txt'
            self._SAVE_FRAMES_DESTINATION_PATH += '\\Frames'
            # TODO PATH TO CHANGE
            self._VIDEOS_FILES_PATH += '\\Videos\\test_file.mp4'
        elif self._CURRENT_SYSTEM_NAME == 'posix':
            self._SAVE_FILES_DESTINATION_PATH += '/Downloads'
            self._SAVE_WRONG_URL_DESTINATION_PATH += '/Res/wrong_url_list.txt'
            self._URL_FILE_PATH += '/Res/url_list.txt'
            self._SAVE_FRAMES_DESTINATION_PATH += '/Frames'
            # TODO PATH TO CHANGE
            self._VIDEOS_FILES_PATH += '/Videos/test_file.mp4'
        else:
            print("Your system is not supported")
            exit()

        self.frame_path = self._SAVE_FRAMES_DESTINATION_PATH

    # Getters
    @property
    def get_files_destination_path(self):
        return self._SAVE_FILES_DESTINATION_PATH

    @property
    def get_wrong_url_destination_path(self):
        return self._SAVE_WRONG_URL_DESTINATION_PATH

    @property
    def get_url_file_path(self):
        return self._URL_FILE_PATH

    @property
    def get_frames_destination_path(self):
        return self._SAVE_FRAMES_DESTINATION_PATH

    @property
    def get_video_files_path(self):
        return self._VIDEOS_FILES_PATH

    @property
    def get_system_name(self):
        return self._CURRENT_SYSTEM_NAME

    @property
    def get_local_path(self):
        return self._LOCAL_PATH

    @property
    def get_selected_frame_path(self):
        return self.frame_path

    # Set frame path
    def set_current_frame_path(self, selected_frame):
        if self._CURRENT_SYSTEM_NAME == 'nt':
            self.frame_path = self._SAVE_FRAMES_DESTINATION_PATH + f'\\{selected_frame}'
        elif self._CURRENT_SYSTEM_NAME == 'posix':
            self.frame_path = self._SAVE_FRAMES_DESTINATION_PATH + f'/{selected_frame}'

        return self.frame_path


