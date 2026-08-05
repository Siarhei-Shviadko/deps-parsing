from typing import Type, Union

from deps_document_layout.model import ParsingType as DLParsingType
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.domain.exceptions import UnsupportedParsingType

from .semantic_parsing_type import SemanticParsingType

__all__ = ["ParsingType", "LayoutTypeReference"]

LayoutTypeReference = Union[Type[TLParsingType], Type[DLParsingType], Type[SemanticParsingType]]


class ParsingType:
    extra_types_mapping: dict[str, Union[TLParsingType, DLParsingType]] = {
        "XLS": TLParsingType.EXCEL,
        "XLSX": TLParsingType.EXCEL,
    }

    def __init__(self, value: str) -> None:
        self.value = self._resolve(value.upper())

    @classmethod
    def supports(cls, value: str) -> bool:
        value = value.upper()

        return (
            value in DLParsingType.__members__
            or value in TLParsingType.__members__
            or value in cls.extra_types_mapping
            or value in SemanticParsingType.__members__
        )

    @property
    def layout_type(self) -> LayoutTypeReference:
        return self.value.__class__

    @classmethod
    def _resolve(cls, value: str) -> Union[TLParsingType, DLParsingType, SemanticParsingType]:
        if value in DLParsingType.__members__:
            return DLParsingType(value)
        if value in TLParsingType.__members__:
            return TLParsingType(value)
        if value in cls.extra_types_mapping:
            return cls.extra_types_mapping[value]
        if value in SemanticParsingType.__members__:
            return SemanticParsingType[value]
        raise UnsupportedParsingType(f"Unsupported parsing type: {value}")
