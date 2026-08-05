from enum import Enum

__all__ = ["SemanticParsingType"]


class SemanticParsingType(str, Enum):
    LLAMAINDEX = "llamaindex"
