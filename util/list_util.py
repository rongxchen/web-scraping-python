from typing import List


def is_empty(lst: List[any]):
    return lst is None or len(lst) == 0


def is_not_empty(lst: List[any]):
    return not is_empty(lst)
