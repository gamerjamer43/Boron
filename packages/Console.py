from rich.prompt import Prompt
from rich import print

@staticmethod
def out(data: str) -> None:
    print(f"[white]{data}[/white]")

@staticmethod
def inp(data: str) -> str:
    try:
        return Prompt.ask(data)
    except KeyboardInterrupt:
        print(f"[bold red]KeyboardInterrupt[/bold red]")
        exit(0)

@staticmethod
def error(typ: str, data: str) -> None:
    print(f"[bold red]{typ}Error: {data}[/bold red]")