from PySide6 import QtWidgets, QtGui
from FileOrganizer import FileOrganizer
import sys
import os

class SystemTray:
    def __init__(self, file_organizer: FileOrganizer):
        # Reference to file organizer instance
        self.file_organizer = file_organizer
        # Gets the path of the current file
        self.cur_path = os.path.dirname(os.path.abspath(__file__)) + "/"

        # Creates a system tray and adds 4 elements to it:
        # Checkmark - to check if user wants to auto organize files
        # Second checkmark - to allow the user to choose if he wants to sort contents that are inside the folders
        # Button to organize files once
        # Button to exit
        def create_system_tray():
            nonlocal self
            app = QtWidgets.QApplication(sys.argv)
            system_tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon(self.cur_path + "organizer.png"), app)
            menu = QtWidgets.QMenu()

            auto_organize = menu.addAction("Auto-Organize")
            auto_organize.setCheckable(True)
            auto_organize.triggered.connect(lambda: self.set_auto_organize(auto_organize))

            organize_folders = menu.addAction("Organize Folders")
            organize_folders.setCheckable(True)
            organize_folders.triggered.connect(lambda: self.set_organize_folders(organize_folders))

            organize_desktop = menu.addAction("Organize Desktop")
            organize_desktop.triggered.connect(self.file_organizer.organize_files)

            exit_btn = menu.addAction("Exit")
            exit_btn.triggered.connect(self.close_system_tray)

            system_tray.setToolTip("Right click to access settings")
            system_tray.setContextMenu(menu)
            system_tray.show()
            sys.exit(app.exec())

        create_system_tray()

    # Sets the file organizer's auto sort flag
    def set_auto_organize(self, checkmark: QtGui.QAction):
        self.file_organizer.set_auto_sort(checkmark.isChecked())

    # Sets the file organizer's sort folders flag
    def set_organize_folders(self, checkmark: QtGui.QAction):
        self.file_organizer.set_sort_folders(checkmark.isChecked())

    # Closes the application
    def close_system_tray(self):
        # Sets the exit flag for the real time file organize loop
        self.file_organizer.set_exit_flag()
        # Closes the app
        exit()