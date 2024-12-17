import pandas as pd


def is_numeric(series: pd.Series):
    if series.dtype == "object":
        return False
    try:
        pd.to_numeric(series)
        return True
    except Exception as e:
        return False


def to_numeric(series: pd.Series):
    if is_numeric(series):
        return pd.to_numeric(series)
    return series
