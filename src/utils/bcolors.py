from rich import print


def succes(msg):
    print(f"[green]{str(msg)}[/]")  # GREEN


def warging(msg):
    print(f"[yellow]{str(msg)}[/]")  # YELLOW


def error(msg):
    print(f"[red]{str(msg)}[/]")  # RED


def info(msg):
    print(f"[green]{str(msg)}[/]")  # RESET COLOR
