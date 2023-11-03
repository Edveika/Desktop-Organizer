class File:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
    
    def get_name(self):
        return self.file_name
    
    def get_path(self):
        return self.file_path