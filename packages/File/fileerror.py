class FileError(Exception):
    """Custom exception class with a message."""
    def __init__(self, message):
        super().__init__(message)
        self.message = "\033[31m" + message + "\033[0m"

    def __str__(self):
        return self.message