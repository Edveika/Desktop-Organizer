![Screenshot from 2024-03-31 15-22-25](https://github.com/Edveika/Desktop-Organizer/assets/113787144/0c524c70-c493-471d-b9ae-0ca58f1b2a6a)

# 🖥️ Desktop-Organizer

Desktop organizer is a Python application that organizes your desktop files. It has QT system tray that provides an easy way to interact with the program.

# 🔥 Features

* Manual sorting - sort files once with a click of a button
* Real-Time sorting - sorts files in real time
* File categorization - classifies files into categories such as audio, video, pictures, documents, and more.
* Cross-Platform Compatibility: supports Windows, Linux, and macOS.
* System tray - allows you to customize sorting settings

# 📔 Libraries used

* PySide6
* threading
* platform
* shutil
* json
* time
* sys
* os

# 🏃 Running the application

* Using python's interpreter in Desktop-Organizer/Desktop-Organizer/ dir:

```
python3 App.py
```

# 🏗️ TODO

* Save settings in a file. If user enables real time sorting and reboots he will not need to reenable it.
* GUI to whitelist files/undo actions

# ⌨️ Cool code showcase

* Recursive function that finds all subfolders from folder_dir. Super proud of this one.

```python
# This is a recursive function that retrieves all of the sub directories from folder_dir
# This function is called for every sub directory until there is no more sub directories in them
# Then it returns all of the paths
def get_sub_folder_paths(self, folder_dir: str) -> list[str]:
        # Retrieves sub folders in current directory
        sub_folders = self.get_sub_folders(folder_dir)

        # If there are no more sub folders in this dir, return
        if not sub_folders:
            return

        # List of subfolders in sub folders
        sub_sub_folders = []
        for folder in sub_folders:
            # List of paths to sub directories of current directory
            sub_paths = self.get_sub_folder_paths(folder)
            # If its not empty
            if sub_paths:
                # Append the sub folders of sub folder list
                for path in sub_paths:
                    sub_sub_folders.append(path)

        # Extends the current sub folder list
        sub_folders.extend(sub_sub_folders)

        # Returns it, then function down the stack does the same until end is reached
        return sub_folders
```

# 📜 License

This project is licensed under the GPL v2 [LICENSE](LICENSE).
