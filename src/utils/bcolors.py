from rich import print


def succes(msg):
    print(f"[bold green]{str(msg)}[/]")  # GREEN


def warging(msg):
    print(f"[bold yellow]{str(msg)}[/]")  # YELLOW


def error(msg):
    print(f"[bold red]{str(msg)}[/]")  # RED


def info(msg):
    print(f"[bold green]{str(msg)}[/]")  # RESET COLOR
