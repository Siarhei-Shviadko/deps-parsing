from deps_document_layout.model import ParsingType

from .base_service import BaseDepsParsingService

__all__ = [
    "TesseractParsingService",
    "EasyocrParsingService",
    "PaddleocrParsingService",
    "CraftTesseractParsingService",
]


class TesseractParsingService(BaseDepsParsingService):
    parsing_type = ParsingType.TESSERACT


class EasyocrParsingService(BaseDepsParsingService):
    parsing_type = ParsingType.EASYOCR


class CraftTesseractParsingService(BaseDepsParsingService):
    parsing_type = ParsingType.CRAFT_TESSERACT


class PaddleocrParsingService(BaseDepsParsingService):
    parsing_type = ParsingType.PADDLEOCR
