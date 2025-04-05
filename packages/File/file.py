from pathlib import Path
from .fileerror import FileError

class File:
    def __init__(self, path):
        if isinstance(path, File):
            path = path.path
        self.path = Path(path).resolve()

    def exists(self):
        return self.path.exists()

    def size(self):
        if not self.exists():
            raise FileError(f"File not found: {self.path}")
        return self.path.stat().st_size

    def abspath(self):
        return str(self.path)

    def __str__(self):
        return f"File({self.abspath()})"