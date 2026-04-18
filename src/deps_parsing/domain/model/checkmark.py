from enum import Enum

__all__ = ["CheckmarkValue"]


class CheckmarkValue(str, Enum):
    CHECKED = "checked"
    UNCHECKED = "unchecked"
