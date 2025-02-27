from decimal import Decimal
from typing import Union
from rich import print

@staticmethod
def toInt(string: str) -> int:
    try:
        return int(string)
    except ValueError:
        print(f"[red]StringError: The string: '{string}' cannot validly be converted to an integer. Possibly not an int value, or contains characters?'[/red]")
        exit(0)

@staticmethod
def toStr(value: Union[int, Decimal]) -> str:
    return str(value)

@staticmethod
def toDec(string: str) -> Decimal:
    try:
        return Decimal(string)
    except ValueError:
        print("[red]StringError\n", f"The string\n'{string}\ncannot validly be converted to an decimal. Possibly not an decimal/int value, or contains characters?'[/red]")
        exit(0)