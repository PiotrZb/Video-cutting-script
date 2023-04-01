import os

# Modules
from src.pathmanager import PathManager


# Path manager object
path_manager = PathManager()

MENU_OPTIONS = {
    '1': 'Load all videos from .txt file.',
    '2': 'Cut frames from videos.'
}


def clear_console():
    if path_manager.get_system_name == 'posix':
        _ = os.system('clear')
    elif path_manager.get_system_name == 'nt':
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
