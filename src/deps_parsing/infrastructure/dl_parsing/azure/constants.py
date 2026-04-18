from enum import Enum

__all__ = ["AzureParsingStrategyEnum"]


class AzureParsingStrategyEnum(str, Enum):
    BY_PAGE = "by_page"
    BY_DOCUMENT = "by_document"
