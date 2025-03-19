import re
from typing import Optional, List, Pattern, Match

__all__ = ["Pattern", "Match", "comp", "fullmatch", "search", "findall", "sub", "split"]

def comp(pattern: str) -> Pattern:
    return re.compile(pattern)

def fullmatch(pattern: str, text: str) -> bool:
    return re.fullmatch(pattern, text) is not None

def search(pattern: str, text: str) -> Optional[Match[str]]:
    return re.search(pattern, text)

def findall(pattern: str, text: str) -> List[str]:
    return re.findall(pattern, text)

def sub(pattern: str, repl: str, text: str, count: int = 0) -> str:
    return re.sub(pattern, repl, text, count=count)

def split(pattern: str, text: str) -> List[str]:
    return re.split(pattern, text)