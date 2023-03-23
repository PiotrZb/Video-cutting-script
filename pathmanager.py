import os
from pathlib import Path


class PathManager:
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

    def get_files_destination_path(self):
        return self.SAVE_FILES_DESTINATION_PATH

    def get_wrong_url_destination_path(self):
        return self.SAVE_WRONG_URL_DESTINATION_PATH

    def get_url_file_path(self):
        return self.URL_FILE_PATH

    def get_frames_destination_path(self):
        return self.SAVE_FRAMES_DESTINATION_PATH

    def get_video_files_path(self):
        return self.VIDEOS_FILES_PATH

    def get_system_name(self):
        return self.SYSTEM_NAME

    def get_local_path(self):
        return self.LOCAL_PATH


