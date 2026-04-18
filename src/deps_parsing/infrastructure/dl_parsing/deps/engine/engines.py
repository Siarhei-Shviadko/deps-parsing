from deps_document_layout.model import ParsingType

from .base_engine import BaseDepsOCREngine

__all__ = ["TesseractParsingEngine", "EasyocrParsingEngine", "CraftTesseractParsingEngine", "PaddleocrParsingEngine"]


class TesseractParsingEngine(BaseDepsOCREngine):
    parsing_type = ParsingType.TESSERACT


class EasyocrParsingEngine(BaseDepsOCREngine):
    parsing_type = ParsingType.EASYOCR


class CraftTesseractParsingEngine(BaseDepsOCREngine):
    parsing_type = ParsingType.CRAFT_TESSERACT


class PaddleocrParsingEngine(BaseDepsOCREngine):
    parsing_type = ParsingType.PADDLEOCR
