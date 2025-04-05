from .fileerror import FileError
from .file import File

class FileReader:
    def __init__(self, file: File):
        if hasattr(file, 'file'):
            file = file.file

        if not hasattr(file, 'exists') or not file.exists():
            raise FileError(f"File not found or invalid file provided: {file}")
        
        self.file = file

    def read(self, encoding='utf-8'):
        with self.file.path.open('r', encoding=encoding) as f:
            return f.read()

    def readlines(self, encoding='utf-8'):
        lines = []
        with self.file.path.open('r', encoding=encoding) as f:
            for line in f:
                lines.append(line)
        return lines