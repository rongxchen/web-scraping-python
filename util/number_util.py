from typing import Union


def is_number(number: Union[str, int, float]):
    if isinstance(number, int) or isinstance(number, float):
        return True
    try:
        float(number)
        return True
    except Exception:
        return False


def to_number(number: Union[str, int, float], to_float: bool = False):
    num = -1
    if isinstance(number, int) or isinstance(number, float):
        num = number
    if isinstance(number, str):
        if number.endswith("万"):
            num = int(float(number[:-1]) * 10000)
        if number.endswith("亿"):
            num = int(float(number[:-1]) * 100000000)
        if not is_number(num):
            raise ValueError("Invalid number string")
    if to_float:
        return float(num)
    return int(float(num))
