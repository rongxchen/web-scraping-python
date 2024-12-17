from enum import Enum


class MissingDataStrategy(Enum):
    FILL_MEAN = "fill_mean"
    FILL_MEDIAN = "fill_median"
    FILL_MODE = "fill_mode"
    DROP = "drop"
    IGNORE = "ignore"
