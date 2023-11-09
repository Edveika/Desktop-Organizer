from FileOrganizer import FileOrganizer
from PySide6 import QtWidgets, QtGui
import sys

class SystemTray:
    def __init__(self):
        # Todo: message box in case of exception
        self.file_organizer = FileOrganizer()

        # Creates a system tray and adds 4 elements to it:
        # Checkmark - to check if user wants to auto organize files
        # Second checkmark - to allow the user to choose if he wants to sort contents that are inside the folders
        # Button to organize files once
        # Button to exit
        def create_system_tray():
            nonlocal self
            app = QtWidgets.QApplication([])
            system_tray = QtWidgets.QSystemTrayIcon(QtGui.QIcon("icon.png"), app)
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
            exit_btn.triggered.connect(exit)

            system_tray.setToolTip("Right click to access settings")
            system_tray.setContextMenu(menu)
            system_tray.show()
            sys.exit(app.exec())

        create_system_tray()

    def set_auto_organize(self, checkmark: QtGui.QAction):
        if checkmark.isChecked():
            print("checked")
        else:
            print("unchecked")

    def set_organize_folders(self, checkmark: QtGui.QAction):
        if checkmark.isChecked():
            print("checked")
        else:
            print("unchecked")

tray = SystemTray()