import cv2 as cv
from pytube import YouTube
from pathlib import Path
import os

local_path = Path(__file__).parent.absolute().__str__()


if os.name == 'nt':
    SAVE_FILES_DESTINATION_PATH = local_path + '\\Downloads'
    SAVE_WRONG_URL_DESTINATION_PATH = local_path + '\\Res\\wrong_url_list.txt'
    URL_FILE_PATH = local_path + '\\Res\\url_list.txt'
else:
    SAVE_FILES_DESTINATION_PATH = local_path + '/Downloads'
    SAVE_WRONG_URL_DESTINATION_PATH = local_path + '/Res/wrong_url_list.txt'
    URL_FILE_PATH = local_path + '/Res/url_list.txt'


def displayer(vcp):
    while True:
        retval, image = vcp.read()

        if retval:
            cv.imshow('Movie', image)

            if cv.waitKey(25) == ord('q'): # press q to quit
                break
        else:
            break

    vcp.release()
    cv.destroyAllWindows()


def load_all_from_txt(file_path=URL_FILE_PATH, destination_path=SAVE_FILES_DESTINATION_PATH):

    wrong_urls = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        lines_count = len(lines)
        for index, url in enumerate(lines):
            try:
                movie = YouTube(url)
                print(f"{index + 1} : {lines_count} -> Downloading file: \""
                      f"{movie.streams[0].title}\"")
                movie.streams.get_highest_resolution().download(
                    output_path=destination_path)
            except Exception as exc:
                wrong_urls.append(url)
                print(exc)

    file.close()

    with open(SAVE_WRONG_URL_DESTINATION_PATH, 'w') as file:
        file.writelines(wrong_urls)

    file.close()


def main():

    # first argument - path to file with links to download
    # second argument - path to folder where movies should be store
    load_all_from_txt()

    # url = 'http://youtube.com/watch?v=2lAe1cqCOXo'
    #
    # yt = YouTube(url)
    # print(yt.title)


    #stream = yt.streams.get_highest_resolution().download()

    #displayer(cv.VideoCapture(stream))

if __name__ == "__main__":
    main()