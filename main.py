import cv2 as cv
from pytube import YouTube
from pathlib import Path
import os

LOCAL_PATH = Path(__file__).parent.absolute().__str__()


if os.name == 'nt':
    SAVE_FILES_DESTINATION_PATH = LOCAL_PATH + '\\Downloads'
    SAVE_WRONG_URL_DESTINATION_PATH = LOCAL_PATH + '\\Res\\wrong_url_list.txt'
    URL_FILE_PATH = LOCAL_PATH + '\\Res\\url_list.txt'
else:
    SAVE_FILES_DESTINATION_PATH = LOCAL_PATH + '/Downloads'
    SAVE_WRONG_URL_DESTINATION_PATH = LOCAL_PATH + '/Res/wrong_url_list.txt'
    URL_FILE_PATH = LOCAL_PATH + '/Res/url_list.txt'


def displayer(vcp):
    """
    vcp -> cv2.VideoCapture object
    Function displays movie in opencv window.
    """

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
    """
    file_path -> path to the file with url addresses \n
    destination_path -> path to the file where movies will be store \n
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


def cut_video(time_span,file_path,destination_path):
    """
    time_span -> tuple (start time, stop time) in seconds
    file_path -> path to the .mp4 file
    destination_path -> path to the folder where frames will be store
    some description here
    """

    start_time, stop_time = time_span
    vcp = cv.VideoCapture(file_path)
    fps = int(vcp.get(cv.CAP_PROP_FPS))  # frames per seconds
    first_frame = fps * start_time
    last_frame = fps * stop_time

    count = 0
    for frame_index in range(0,last_frame):
        read_success, frame = vcp.read()

        if read_success:
            print(count)
            if count > first_frame:
                path = destination_path + f'/frame{count}.png' # or jpg
                cv.imwrite(path,frame)
            cv.waitKey(5)
        count += 1
    vcp.release()


def main():

    #load_all_from_txt()

    # UWAGA!!! Nawet krótki przedział czasowy powoduje zapisanie masy plików png, więc jak nie chcecie zasyfić sobie
    # kompa to polecam ogarnąć dobrze ścieżkę zapisu ... wiem co mówie xd
    # można dodać linijkę kodu tak aby zapisywane były tylko niektóre klatki z przedziału np. co piąta
    # filmy na yt mają fps = 30 więc każda sekunda filmu to 30 klatek -> 30 plików .png!!!!
    cut_video((10,11),'Downloads/pliktestowy.mp4','test')
    pass


if __name__ == "__main__":
    main()
