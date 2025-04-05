from .fileerror import FileError
from .file import File

class FileWriter:
    def __init__(self, file: File):
        self.file = file

    def write(self, data, encoding='utf-8', overwrite=True):
        mode = 'w' if overwrite else 'a'
        with self.file.path.open(mode, encoding=encoding) as f:
            f.write(data)

    def append(self, data, encoding='utf-8'):
        self.write(data, encoding, overwrite=False)

    def delete(self):
        if not self.file.exists():
            raise FileError(f"File not found: {self.file.path}")
        self.file.path.unlink()