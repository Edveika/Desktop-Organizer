from Setting import Setting
import platform
import dirs
import os
import json

class SettingsCache:
  def __init__(self) -> None:
    self.get_cache_path()
  
  def get_cache_path(self): 
    os_name = platform.system()

    match os_name:
      case "Windows": self.cache_path = dirs.WINDOWS_SETTINGS_DIR
      case "Linux": self.cache_path = dirs.LINUX_SETTINGS_DIR
      case "Darwin": self.cache_path = dirs.MACOS_SETTINGS_DIR
      case _:
        raise Exception("Unsupported Operating System")
      
    if not os.path.exists(self.cache_path):
      os.mkdir(self.cache_path)
      
  def save_setting(self, setting: Setting):
    with open(str(self.cache_path + dirs.CACHE_FILE_NAME), "w") as cache_file:
      value = {
        "name": setting.get_name(),
        "value": setting.get_value()
      }
      json.dump(value, cache_file)
  
  def get_setting(self, setting: Setting) :
    pass