from deps_document_layout.model import ParsingType

from .base_service import BaseDepsParsingService

__all__ = ["TesseractParsingService"]


class TesseractParsingService(BaseDepsParsingService):
    parsing_type = ParsingType.TESSERACT
