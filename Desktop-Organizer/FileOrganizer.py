from File import File
from FileTypes import AUDIO_FORMATS, VIDEO_FORMATS, PICTURE_FORMATS, DOCUMENT_FORMATS, SHORTCUT_FORMATS
from threading import Thread
import platform
import os

# TODO: whitelist directory that the current app is in(if py files are on desktop for whatever reason, show an error)
# TODO: ability to organize files that are inside folders

class FileOrganizer:
    def __init__(self):
        # Empty list of desktop files
        self.desktop_files: list[File] = []
        # Will contain desktop folders
        self.desktop_folders: list[File] = []
        # Desktop files are going to be sorted into smaller lists for moving files to appropriate folders
        self.audio_files: list[File] = []
        self.video_files: list[File] = []
        self.picture_files: list[File] = []
        self.document_files: list[File] = []
        # Unknown files - files that are not in FileTypes.py and files without extension.
        # Will be moved to Downloads dir
        self.unknown_files: list[File] = []
        # Gets path of desktop folder based on the OS
        self.get_dir_paths()
        # Filter files into smaller lists
        self.filter_files()
    
    # Gets a paths to needed directories based on user's Operating System
    # Downloads and Desktop(obviously) folders are required for the app to work
    # Downloads is the default folder in case a dir does not exist or file extension is unknown
    def get_dir_paths(self):
        # Operating System name
        os_name = platform.system()

        match os_name:
            case "Windows":
                def get_path_windows(dir_name):
                    if os.path.exists(os.path.join(os.path.join(os.environ['USERPROFILE']), dir_name)):
                        return os.path.join(os.path.join(os.environ['USERPROFILE']), dir_name)
                    return None

                if not get_path_windows("Desktop/"):
                    raise Exception("Desktop directory does not exist")
                self.desktop_path = get_path_windows("Desktop/")

                if not get_path_windows("Downloads/"):
                    raise Exception("Downloads directory does not exist")
                self.download_path = get_path_windows("Downloads/")

                self.document_path = get_path_windows("Documents/")
                self.audio_path = get_path_windows("Music/")
                self.video_path = get_path_windows("Videos/")
                self.picture_path = get_path_windows("Pictures/")
            case "Linux":
                def get_path_linux(dir_name: str):
                    if os.path.exists(os.path.join(os.path.join(os.path.expanduser('~')), dir_name)):
                        return os.path.join(os.path.join(os.path.expanduser('~')), dir_name)
                    return None

                if not get_path_linux("Desktop/"):
                    raise Exception("Desktop directory does not exist")
                self.desktop_path = get_path_linux("Desktop/")

                if not get_path_linux("Downloads/"):
                    raise Exception("Downloads directory does not exist")
                self.download_path = get_path_linux("Downloads/")

                self.document_path = get_path_linux("Documents/")
                self.audio_path = get_path_linux("Music/")
                self.picture_path = get_path_linux("Pictures/")
                self.video_path = get_path_linux("Videos/")
            case "Darwin":
                def get_path_macos(dir_name):
                    if os.path.exists(os.path.expanduser(dir_name)):
                        return os.path.expanduser(dir_name)
                    return None

                if not get_path_macos("~/Desktop/"):
                    raise Exception("Desktop directory does not exist")
                self.desktop_path = get_path_macos("~/Desktop/")

                if not get_path_macos("~/Downloads/"):
                    raise Exception("Downloads directory does not exist")
                self.desktop_path = get_path_macos("~/Downloads/")

                self.document_path = get_path_macos("~/Documents/")
                self.audio_path = get_path_macos("~/Music/")
                self.picture_path = get_path_macos("~/Pictures/")
                # I dont know if Movies in macos language mean Videos
                # But this is where video files are going to be stored
                self.video_path = get_path_macos("~/Movies/")
            case _:
                raise Exception("Unsupported Operating System")

    # Makes a list of desktop folders
    def get_desktop_folders(self):
        for file in os.listdir(self.desktop_path):
            if os.path.isdir(self.desktop_path + file):
                self.desktop_folders.append(str(file + "/"))

    # Returns a list of sub folders in cur dir
    def get_sub_folders(self, cur_dir: str) -> list[str]:
        sub_folders: str = []

        for file in os.listdir(cur_dir):
            if os.path.isdir(cur_dir + file):
                sub_folders.append(cur_dir + str(file + "/"))
        
        return sub_folders

    # This is a recursive function that retrieves all of the sub directories from folder_dir
    # This function is called for every sub directory until there is no more sub directories in them
    # Then it returns all of the paths
    def get_folder_file_paths(self, folder_dir: str) -> list[str]:
        # Retrieves sub folders in current directory
        sub_folders = self.get_sub_folders(folder_dir)
        # If there are no more sub folders in this dir, return
        if not sub_folders:
            return

        # List of subfolders in sub folders
        sub_sub_folders = []
        for folder in sub_folders:
            # List of paths to sub directories of current directory
            sub_paths = self.get_folder_file_paths(folder)
            # If its not empty
            if sub_paths:
                # Append the sub folders of sub folder list
                for path in sub_paths:
                    sub_sub_folders.append(path)

        # Extends the current sub folder list
        sub_folders.extend(sub_sub_folders)

        # Returns it, then function down the stack does the same until end is reached
        return sub_folders

    # Filters the desktop file list into smaller lists
    # Audio files, document files, picture files, video files
    # If the file has no extension or has some kind of other extension, it will be moved into the downloads folder
    def filter_files(self): 
        desktop_files = os.listdir(self.desktop_path)

        for file in desktop_files:
            # If file has no extension it will return the last char of the file name
            # Thats ok, because all of the file extensions have . prefix in FileTypes.py
            # And even if it does have a file extensions that doesnt match anything, its an unknown file
            extension = file[file.rfind("."):].upper()
            # App shortcuts/macos apps are going to be ignored
            if extension in SHORTCUT_FORMATS:
                continue

            # Adds the file into the appropriate list
            if extension in AUDIO_FORMATS:
                self.audio_files.append(file)
            elif extension in VIDEO_FORMATS:
                self.video_files.append(file)
            elif extension in PICTURE_FORMATS:
                self.picture_files.append(file)
            elif extension in DOCUMENT_FORMATS:
                self.document_files.append(file)
            else:
                self.unknown_files.append(file)

    # Moves a list of files to wanted directory
    # After moving the files, will clear the file list
    # If dst dir does not exist, it will default to downloads dir
    def move_files(self, file_list, dst):
        src_dir = self.desktop_path
        dst_dir = dst
        if not os.path.exists(dst):
            dst_dir = self.download_path

        for file in file_list:
            src_file = src_dir + file
            dst_file = dst_dir + file
            # If file src_file file exists in dst, (file_num) will be added next to file name
            file_num = 1
            # Until we find file_num that does not exist, keep searching
            while os.path.exists(dst_file):
                dst_file = dst_dir + file + "(" +str(file_num) + ")"
                file_num += 1

            # Moves the file from src to dst
            os.replace(src_file, dst_file)
        
        file_list.clear()

    # Starts a thread for moving earch file type
    def organize_files(self):
        doc_thread = Thread(target=self.move_files, args=(self.document_files, self.document_path))
        doc_thread.start()

        download_thread = Thread(target=self.move_files, args=(self.unknown_files, self.download_path))
        download_thread.start()

        audio_thread = Thread(target=self.move_files, args=(self.audio_files, self.audio_path))
        audio_thread.start()

        pic_thread = Thread(target=self.move_files, args=(self.picture_files, self.picture_path))
        pic_thread.start()

        vid_thread = Thread(target=self.move_files, args=(self.video_files, self.video_path))
        vid_thread.start()
        
task_organizer = FileOrganizer()
print(task_organizer.get_folder_file_paths("/home/edveika/Desktop/"))