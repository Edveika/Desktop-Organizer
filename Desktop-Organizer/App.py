from FileOrganizer import FileOrganizer
from GUIManager import SystemTray, MessageBox
from PySide6 import QtWidgets, QtGui
import threading

def main():
    messagebox = MessageBox()

    try:
        # Creates file organizer instance
        file_organizer = FileOrganizer()
    except Exception as e:
        # If exception was caught, show a message and exit the program
        messagebox.show_messagebox("Error", str(e))
        exit()

    # Starts real time sorting thread
    sort_thread = threading.Thread(target=file_organizer.organize_real_time)
    sort_thread.start()

    try:
        # Starts the system tray
        SystemTray(file_organizer)
    except Exception as e:
        # If exception was caught, show a message and exit the program
        messagebox.show_messagebox("Error", str(e))
        exit()

main()