import cv2 as cv
from pytube import YouTube
import os

# Modules
from pathmanager import PathManager
import gui

# Path manager object
path_manager = PathManager()

MENU_OPTIONS = {
	'1': 'Load all videos from .txt file.',
	'2': 'Cut frames from videos.'
}


def clear_console():
	if path_manager.SYSTEM_NAME == 'posix':
		_ = os.system('clear')
	elif path_manager.SYSTEM_NAME == 'nt':
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


def load_all_from_txt(file_path=path_manager.get_url_file_path(),
                      destination_path=path_manager.get_files_destination_path()):
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

	with open(path_manager.get_wrong_url_destination_path(), 'w') as file:
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


def main():
	program = gui.App()
	program.run()


if __name__ == "__main__":
	main()
