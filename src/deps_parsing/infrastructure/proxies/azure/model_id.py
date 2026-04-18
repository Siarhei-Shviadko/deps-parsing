from enum import Enum

__all__ = ["ModelId"]


class ModelId(str, Enum):
    PREBUILT_DOCUMENT = "prebuilt-document"
    PREBUILT_LAYOUT = "prebuilt-layout"
