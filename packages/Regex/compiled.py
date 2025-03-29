import re
from .matcher import Matcher
from typing import Optional, List

class Compiled:
    def __init__(self, pattern: str):
        self.pattern = re.compile(pattern)
        self.env = {}

    def fullmatch(self, text: str) -> bool:
        return self.pattern.fullmatch(text) is not None

    def search(self, text: str) -> Optional["Matcher"]:
        match = self.pattern.search(text)
        return Matcher(match) if match else None

    def findall(self, text: str) -> List[str]:
        return self.pattern.findall(text)

    def sub(self, repl: str, text: str, count: int = 0) -> str:
        return self.pattern.sub(repl, text, count)

    def split(self, text: str) -> List[str]:
        return self.pattern.split(text)