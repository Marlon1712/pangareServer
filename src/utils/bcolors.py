def succes(msg):
    print(f"\033[92m{msg}")  # GREEN


def warging(msg):
    print(f"\033[93m{msg}")  # YELLOW


def error(msg):
    print(f"\033[91m{msg}")  # RED


def info(msg):
    print(f"\033[0m{msg}")  # RESET COLOR
