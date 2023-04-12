from datetime import datetime
from typing import Any

from colorama import Back, Fore, Style
from ..structs import Assistant, Example, Result, User

right = "❯❯❯"
left = "❮❮❮"


class NoColor:
    def __getattr__(self, *args):
        return ""


NoColor = NoColor()


def str_to_num(num_str):
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    chars = f"0123456789{alpha}{alpha.lower()}_"
    num = 0

    for i, c in enumerate(reversed(num_str)):
        num += chars.index(c) * (len(chars) ** i)

    return num


def debug(
    obj: dict,
    color: bool = True,
    line_length: int = 120,
    whitelist: list = [str, User, Result, Assistant],
) -> None:
    B = Back if color else NoColor
    F = Fore if color else NoColor
    S = Style if color else NoColor

    type_: str = obj["type"]
    payload: Any = obj["payload"]
    timestamp: datetime = obj["timestamp"]
    app: str = obj["app"]

    time: str = timestamp.strftime("%H:%M:%S")
    message_class = payload.__class__
    message_type: str = message_class.__name__
    direction: str = left if type_ == "input" else right

    if whitelist and message_class not in whitelist:
        return

    app_colors: list[str] = [
        F.YELLOW,
        F.MAGENTA,
        F.CYAN,
        F.GREEN,
        F.BLUE,
        F.RED,
        F.LIGHTRED_EX,
        F.LIGHTGREEN_EX,
        F.LIGHTBLUE_EX,
        F.LIGHTMAGENTA_EX,
    ]

    app_color: str = app_colors[str_to_num(app) % len(app_colors)]
    direction_color: str = F.BLUE if type_ == "input" else F.GREEN
    message_type_bg: str = B.BLUE if type_ == "input" else B.GREEN

    if hasattr(payload, "content"):
        message = payload.content

        if isinstance(message, dict):
            message = message.get("response", str(message))

    elif isinstance(payload, Example):
        message = (
            f"example(user):{payload.user}\nexample(assistant):{payload.assistant}"
        )
    else:
        message: str = str(payload)

    formatted = S.RESET_ALL.join(
        [
            S.DIM + F.LIGHTWHITE_EX + f"({time})",
            S.BRIGHT + direction_color + f" {direction} ",
            S.BRIGHT + message_type_bg + F.WHITE + f" {message_type} ",
            app_color + f" {message}",
        ]
    )

    suffix = B.BLACK + S.BRIGHT + app_color + f"[{app}]" + S.RESET_ALL

    # Add app name as right-aligned suffix
    formatted = formatted + " " * max(1, line_length - len(formatted) + 20) + suffix

    # Separator if multiline
    if "\n" in formatted:
        formatted += "\n" + "―" * line_length + "\n"

    print(formatted)
