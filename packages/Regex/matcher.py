import re
from typing import Optional

class Matcher:
    def __init__(self, match: Optional[re.Match]):
        self.match = match
        self.env = {}

    def group(self, index: int = 0) -> Optional[str]:
        return self.match.group(index) if self.match else None

    def start(self) -> Optional[int]:
        return self.match.start() if self.match else None

    def end(self) -> Optional[int]:
        return self.match.end() if self.match else None

    def span(self) -> Optional[tuple]:
        return self.match.span() if self.match else None