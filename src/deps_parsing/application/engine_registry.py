from dataclasses import dataclass
from types import MappingProxyType

from deps_document_layout.model import ParsingType as DLParsingType
from deps_tabular_layout.models import ParsingType as TLParsingType

from .layout_type import LayoutType
from .semantic_parsing_type import SemanticParsingType

__all__ = ["EngineInfo", "ENGINES"]

_NAMES = MappingProxyType(
    {
        "GCP_VISION": "GCP Document AI",
        "AWS_TEXTRACT": "AWS Textract",
        "AZURE_FORM_RECOGNIZER": "Azure Form Recognizer",
        "TESSERACT": "Tesseract",
        "DOCX": "DOCX",
        "EXCEL": "Excel",
        "CSV": "CSV",
        "llamaindex": "LlamaIndex",
    },
)


@dataclass(frozen=True)
class EngineInfo:
    code: str
    name: str
    layout_type: LayoutType


def _build_engines(
    parsing_type: type[DLParsingType] | type[TLParsingType] | type[SemanticParsingType],
    layout_type: LayoutType,
) -> list[EngineInfo]:
    return [
        EngineInfo(code=member.value, name=_NAMES[member.value], layout_type=layout_type)
        for member in parsing_type
        if member.value in _NAMES
    ]


ENGINES: list[EngineInfo] = (
    _build_engines(DLParsingType, LayoutType.DOCUMENT_LAYOUT)
    + _build_engines(TLParsingType, LayoutType.TABULAR_LAYOUT)
    + _build_engines(SemanticParsingType, LayoutType.SEMANTIC_LAYOUT)
)
