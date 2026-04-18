from deps_parsing.domain.exceptions import BusinessException, ParsingException

__all__ = [
    "UnifierProxyRequestError",
    "OCRProxyRequestError",
    "TablesProxyRequestError",
    "DocumentProxyRequestError",
    "FileProxyRequestError",
    "EntityNotFoundError",
    "ParsingCsvError",
    "AIFusionProxyRequestError",
    "PageCountMismatchError",
]


class UnifierProxyRequestError(ParsingException):
    pass


class OCRProxyRequestError(ParsingException):
    pass


class TablesProxyRequestError(ParsingException):
    pass


class DocumentProxyRequestError(ParsingException):
    pass


class FileProxyRequestError(ParsingException):
    pass


class EntityNotFoundError(ParsingException):
    pass


class AIFusionProxyRequestError(ParsingException):
    pass


class ParsingCsvError(BusinessException):
    pass


class PageCountMismatchError(ParsingException):
    pass
