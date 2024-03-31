from Setting import Setting
import platform
import dirs
import os

class SettingsCache:
  def __init__(self) -> None:
    os_name = platform.system()

    match os_name:
      case "Windows": self.cache_path = dirs.WINDOWS_SETTINGS_DIR
      case "Linux": self.cache_path = dirs.LINUX_SETTINGS_DIR
      case "Darwin": self.cache_path = dirs.MACOS_SETTINGS_DIR
      case _:
        raise Exception("Unsupported Operating System")

    if not os.path.exists("self.cache_path"):
      os.makedirs(self.cache_path)
