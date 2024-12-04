from typing import List


def is_empty(lst: List[any]):
    return lst is None or len(lst) == 0


def is_not_empty(lst: List[any]):
    return not is_empty(lst)


def remove_duplicates(lst: List[any], key: any = None):
    if is_empty(lst):
        raise ValueError("List is empty")
    if isinstance(lst[0], dict) and key is not None:
        st = {}
        for item in lst:
            if item[key] not in st:
                st[item[key]] = item
        return list(st.values())
    return list(set(lst))
