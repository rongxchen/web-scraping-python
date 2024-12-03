from datetime import datetime


def to_datetime(date_str: str, pattern: str):
    return datetime.strptime(date_str, pattern)
    