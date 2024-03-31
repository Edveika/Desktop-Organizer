import os

CACHE_FILE_NAME = "Settings.json"

LINUX_SETTINGS_DIR = os.path.expanduser("~/.config/DesktopOrganizer/")
MACOS_SETTINGS_DIR = os.path.expanduser("~/Library/Preferences/DesktopOrganizer/")
WINDOWS_SETTINGS_DIR = os.path.expandvars("C:\\Users\\%USERNAME%\\AppData\\Local\\DesktopOrganizer\\")