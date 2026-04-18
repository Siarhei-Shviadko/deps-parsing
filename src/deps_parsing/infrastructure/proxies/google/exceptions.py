from deps_parsing.domain.exceptions import ParsingException

__all__ = ["DocumentAIEngineDisabled"]


class DocumentAIEngineDisabled(ParsingException):
    code = "document_ai_engine_disabled"
