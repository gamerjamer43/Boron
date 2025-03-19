from rich.prompt import Prompt
from datetime import datetime
from decimal import Decimal
from typing import Union
from rich import print

# length
def length(value):
    try:
        if type(value) == int:
            return len(str(value))
        return len(value)
    except TypeError:
        raise ValueError("Object has no length.")

# print
def out(data: str) -> None:
    print(f"[white]{data}[/white]")

# logging (also print)
def log(category: str, message: str) -> None:
    print(f"[blue][{category}, {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}][/blue] {message}")

# input
def inp(data: str) -> str:
    try:
        return Prompt.ask(data)
    except KeyboardInterrupt:
        print(f"[bold red]KeyboardInterrupt[/bold red]")
        exit(0)

# error
def err(typ: str, data: str) -> None:
    print(f"[bold red]{typ}Error: {data}[/bold red]")

# conversions
def toInt(string: str) -> int:
    try:
        return int(string)
    except ValueError:
        print(f"[red]StringError: The string: '{string}' cannot validly be converted to an integer. Possibly not an int value, or contains characters?'[/red]")
        exit(0)

def toStr(value: Union[int, Decimal]) -> str:
    return str(value)

def toDec(string: str) -> Decimal:
    try:
        return Decimal(string)
    except ValueError:
        print("[red]StringError\n", f"The string\n'{string}\ncannot validly be converted to an decimal. Possibly not an decimal/int value, or contains characters?'[/red]")
        exit(0)

def toBool(string: str) -> bool:
    try:
        return bool(string)
    except ValueError:
        print("[red]StringError\n", f"The string\n'{string}\ncannot validly be converted to an boolean. Possibly not a boolean value, or contains other characters?'[/red]")
        exit(0)

#! system operations
def _exit(code: int) -> None:
    exit(code)

def _isinstance(obj: object, info: object) -> bool:
    # make this work, info broken
    return bool(isinstance(obj, info))

# make this work too, classes = dict
def _type(obj: object) -> str:
    return type(obj).__name__

def sort(lst: list) -> list:
    return sorted(lst)

def contains(text: str, substring: str) -> bool:
    return substring in text

BUILTINS = {
    "inp": inp,
    "out": out,
    "err": err,

    "length": length,

    "toInt": toInt,
    "toStr": toStr,
    "toDec": toDec,
    "toBool": toBool,

    "exit": _exit,
    "isinstance": _isinstance,
    "type": _type,

    "sort": sort,
    "contains": contains,
}