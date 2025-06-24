
COLOR_MAP : dict = {
    "gray"      : 30,
    "red"       : 31,
    "green"     : 32,
    "yellow"    : 33,
    "blue"      : 34,
    "magenta"   : 35,
    "cyan"      : 36,
    "pure white": 37,
}

def cprint(
    *args,
    color : str = "none",
    **kwargs
):
    try:
        ansi_color_id = COLOR_MAP[color]
    except KeyError:
        ansi_color_id = 0

    print(f"\033[{ansi_color_id}m", end="")
    print(*args, "\033[0m", **kwargs)