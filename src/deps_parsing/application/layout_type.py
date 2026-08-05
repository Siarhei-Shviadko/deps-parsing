from enum import Enum

__all__ = ["LayoutType"]


class LayoutType(str, Enum):
    DOCUMENT_LAYOUT = "DocumentLayout"
    TABULAR_LAYOUT = "TabularLayout"
    SEMANTIC_LAYOUT = "SemanticLayout"
