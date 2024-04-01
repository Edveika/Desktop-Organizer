from Setting import Setting
import platform
import dirs
import os
import json

class CacheManager:
  def __init__(self) -> None:
    def get_cache_path(): 
      os_name = platform.system()

      match os_name:
        case "Windows": self.cache_path = dirs.WINDOWS_SETTINGS_DIR
        case "Linux": self.cache_path = dirs.LINUX_SETTINGS_DIR
        case "Darwin": self.cache_path = dirs.MACOS_SETTINGS_DIR
        case _:
          raise Exception("Unsupported Operating System")

    # Gets cache dir based on os
    get_cache_path()

    # If cache dir does not exist, creates it
    if not os.path.exists(self.cache_path):
      os.mkdir(self.cache_path)

    # Full path to the cache file
    self.CACHE_FILE_PATH = str(self.cache_path + dirs.CACHE_FILE_NAME)

  # Saves a setting to a file 
  def save_setting(self, setting: Setting):
    # Load data
    data = {}
    try:
      with open(self.CACHE_FILE_PATH, "r") as file:
        data = json.load(file)
    except json.decoder.JSONDecodeError:
      pass

    # Overwrite existing name value or add it to the dict
    data[setting.get_name()] = setting.get_value()

    # Dict to json and to file
    json.dump(data, open(self.CACHE_FILE_PATH, "w"))

  # Returns a list of Setting objects from a JSON file
  def get_settings(self) -> list[Setting]:
    # Load data
    data = {}
    try:
      with open(str(self.cache_path + dirs.CACHE_FILE_NAME)) as file:
        data = json.load(file)
    except json.decoder.JSONDecodeError:
      return None

    settings: list[Setting] = []

    # Create a list of settings from json data
    for key in data:
      settings.append(Setting(str(key), str(data[key])))

    # Return settings list
    return settings