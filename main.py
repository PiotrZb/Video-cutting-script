import cv2 as cv
from pytube import YouTube
from pathlib import Path

local_path = Path(__file__).parent.absolute().__str__()


def displayer(vcp):
    while True:
        retval,image = vcp.read()

        if retval:
            cv.imshow('Movie',image)

            if cv.waitKey(25) == ord('q'): # press q to quit
                break
        else:
            break

    vcp.release()
    cv.destroyAllWindows()


def load_all_from_txt(file_path='links.txt',destination_path=local_path):

    wrongUrls = []

    with open(file_path,'r') as file:
        for url in file.readlines():
            try:
                YouTube(url).streams.get_highest_resolution().download(output_path=destination_path)
            except Exception as exc:
                wrongUrls.append(url)
                print(exc)

    file.close()

    with open(destination_path + '\Wrong urls.txt','w') as file:
        file.writelines(wrongUrls)

    file.close()


def main():

    # first argument - path to file with links to download
    # second argument - path to folder where movies should be store
    load_all_from_txt(destination_path='C:\GitHub\Video-cutting-script\pobrane')

    # url = 'http://youtube.com/watch?v=2lAe1cqCOXo'
    #
    # yt = YouTube(url)
    # print(yt.title)


    #stream = yt.streams.get_highest_resolution().download()

    #displayer(cv.VideoCapture(stream))

if __name__ == "__main__":
    main()