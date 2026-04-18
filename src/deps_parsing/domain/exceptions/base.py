__all__ = ["ParsingException", "BusinessException", "NotFoundError", "UnifiedDataNotFound", "UnsupportedParsingType"]


class ParsingException(Exception):
    code = "parsing_exception"


class BusinessException(ParsingException):
    code = "business_exception"


class NotFoundError(BusinessException):
    code = "not_found_error"


class UnifiedDataNotFound(BusinessException):
    code = "unified_data_not_found"


class UnsupportedParsingType(ParsingException):
    code = "unsupported_parsing_type"
