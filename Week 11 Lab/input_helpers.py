import math
from collections.abc import Callable


def _ask_until_valid(prompt: str, convert: Callable[[str], float],
                     is_valid: Callable[[float], bool],
                     range_message: str, format_message: str) -> float:
    # Keeps asking until the user gives a value that converts AND passes the rule.
    # Two different problems can happen, so they are handled separately:
    #   - convert() raises ValueError when the text is not a number (an exception)
    #   - is_valid() is a validation rule on a number that did convert (an if check)
    while True:
        try:
            value = convert(input(prompt))
        except ValueError:
            print(format_message)
            continue

        if not math.isfinite(value):  # "nan" and "inf" convert, but are not usable numbers
            print(format_message)
            continue

        if not is_valid(value):
            print(range_message)
            continue

        return value


def get_positive_float(prompt: str) -> float:
    # A number greater than zero, e.g. a price.
    return _ask_until_valid(
        prompt, float, lambda value: value > 0,
        "Please enter a number greater than zero.",
        "Please enter a valid number, e.g. 12.50"
    )


def get_non_negative_float(prompt: str) -> float:
    # A number that is zero or more, e.g. a weight or download size.
    return _ask_until_valid(
        prompt, float, lambda value: value >= 0,
        "Please enter a number that is not negative.",
        "Please enter a valid number, e.g. 12.50"
    )


def get_non_negative_int(prompt: str) -> int:
    # A whole number that is zero or more, e.g. a stock quantity.
    return int(_ask_until_valid(
        prompt, int, lambda value: value >= 0,
        "Please enter a whole number that is not negative.",
        "Please enter a valid whole number, e.g. 5"
    ))


def get_positive_int(prompt: str) -> int:
    # A whole number greater than zero, e.g. an order quantity.
    return int(_ask_until_valid(
        prompt, int, lambda value: value > 0,
        "Please enter a whole number greater than zero.",
        "Please enter a valid whole number, e.g. 5"
    ))
