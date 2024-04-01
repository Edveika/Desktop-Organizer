from PySide6 import QtWidgets, QtGui
from FileOrganizer import FileOrganizer
from Setting import Setting
from CacheManager import CacheManager
import sys
import os

class MessageBox:
    def __init__(self):
        pass

    # Shows a message in messagebox with selected title
    def show_messagebox(self, title, message):
        # QApplication has to be constructed before QtWidget
        app = QtWidgets.QApplication([])
        # Create messagebox
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle(title)
        message_box.setText(message)
        message_box.exec()

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
            if not system_tray.isSystemTrayAvailable():
                raise Exception("Your system does not support QSystemTrayIcon functionality")
            menu = QtWidgets.QMenu()

            self.auto_organize = menu.addAction("Auto-Organize")
            self.auto_organize.setCheckable(True)
            self.auto_organize.triggered.connect(lambda: self.set_auto_organize(self.auto_organize))
            self.organize_folders = menu.addAction("Organize Folders")
            self.organize_folders.setCheckable(True)
            self.organize_folders.triggered.connect(lambda: self.set_organize_folders(self.organize_folders))
            organize_desktop = menu.addAction("Organize Desktop")
            organize_desktop.triggered.connect(self.file_organizer.organize_files)

            exit_btn = menu.addAction("Exit")
            exit_btn.triggered.connect(self.close_system_tray)

            system_tray.setToolTip("Right click to access settings")
            system_tray.setContextMenu(menu)
            system_tray.show()

            def load_settings(): 
                nonlocal self
                settings= self.cache_manager.get_settings()

                if not settings:
                    return
                
                self.auto_organize.setChecked(bool(settings["auto_sort"]))
                self.organize_folders.setChecked(bool(settings["sort_folders"]))

            load_settings()

            sys.exit(app.exec())

        self.cache_manager = CacheManager()

        create_system_tray()
            

    # Sets the file organizer's auto sort flag
    def set_auto_organize(self, checkmark: QtGui.QAction):
        self.file_organizer.set_auto_sort(checkmark.isChecked())
        self.cache_manager.save_setting(Setting("auto_sort", int(checkmark.isChecked())))

    # Sets the file organizer's sort folders flag
    def set_organize_folders(self, checkmark: QtGui.QAction):
        self.file_organizer.set_sort_folders(checkmark.isChecked())
        self.cache_manager.save_setting(Setting("sort_folders", int(checkmark.isChecked())))

    # Closes the application
    def close_system_tray(self):
        # Sets the exit flag for the real time file organize loop
        self.file_organizer.set_exit_flag()
        # Closes the app
        exit()