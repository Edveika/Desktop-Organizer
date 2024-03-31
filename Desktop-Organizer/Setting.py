class Setting:
  def __init__(self, name, value) -> None:
    self.name = name
    self.value = value

  def get_name(self):
    return self.name

  def get_value(self):
    return self.value

  def set_name(self, new_name):
    self.name = new_name

  def set_value(self, new_value):
    self.value = new_value