from FileOrganizer import FileOrganizer
from GUIManager import SystemTray
import threading

def main():
    # Creates file organizer instance
    file_organizer = FileOrganizer()

    # Starts real time sorting thread
    sort_thread = threading.Thread(target=file_organizer.organize_real_time)
    sort_thread.start()

    # Starts the system tray
    SystemTray(file_organizer)

main()