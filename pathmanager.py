import os
from pathlib import Path


class PathManager:
    _LOCAL_PATH = Path(__file__).parent.absolute().__str__()

    _CURRENT_SYSTEM_NAME = os.name

    _SAVE_FILES_DESTINATION_PATH = _LOCAL_PATH
    _SAVE_WRONG_URL_DESTINATION_PATH = _LOCAL_PATH
    _URL_FILE_PATH = _LOCAL_PATH
    _SAVE_FRAMES_DESTINATION_PATH = _LOCAL_PATH
    _VIDEOS_FILES_PATH = _LOCAL_PATH

    if _CURRENT_SYSTEM_NAME == 'nt':
        _SAVE_FILES_DESTINATION_PATH += '\\Downloads'
        _SAVE_WRONG_URL_DESTINATION_PATH += '\\Res\\wrong_url_list.txt'
        _URL_FILE_PATH += '\\Res\\url_list.txt'
        _SAVE_FRAMES_DESTINATION_PATH += '\\Frames'
        # TODO PATH TO CHANGE
        _VIDEOS_FILES_PATH += '\\Videos\\test_file.mp4'
    elif _CURRENT_SYSTEM_NAME == 'posix':
        _SAVE_FILES_DESTINATION_PATH += '/Downloads'
        _SAVE_WRONG_URL_DESTINATION_PATH += '/Res/wrong_url_list.txt'
        _URL_FILE_PATH += '/Res/url_list.txt'
        _SAVE_FRAMES_DESTINATION_PATH += '/Frames'
        # TODO PATH TO CHANGE
        _VIDEOS_FILES_PATH += '/Videos/test_file.mp4'
    else:
        print("Your system is not supported")
        exit()

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


