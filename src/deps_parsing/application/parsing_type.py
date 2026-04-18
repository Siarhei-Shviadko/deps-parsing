from typing import Type, Union

from deps_document_layout.model import ParsingType as DLParsingType
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.domain.exceptions import UnsupportedParsingType

__all__ = ["ParsingType", "LayoutTypeReference"]

LayoutTypeReference = Union[Type[TLParsingType], Type[DLParsingType]]


class ParsingType:
    extra_types_mapping: dict[str, Union[TLParsingType, DLParsingType]] = {
        "XLS": TLParsingType.EXCEL,
        "XLSX": TLParsingType.EXCEL,
    }

    def __init__(self, value: str) -> None:
        value = value.upper()

        if value in DLParsingType.__members__:
            self.value = DLParsingType(value)
        elif value in TLParsingType.__members__:
            self.value = TLParsingType(value)
        elif value in self.extra_types_mapping:
            self.value = self.extra_types_mapping[value]
        else:
            raise UnsupportedParsingType(f"Unsupported parsing type: {value}")

    @classmethod
    def supports(cls, value: str) -> bool:
        value = value.upper()

        return (
            value in DLParsingType.__members__ or value in TLParsingType.__members__ or value in cls.extra_types_mapping
        )

    @property
    def layout_type(self) -> LayoutTypeReference:
        return self.value.__class__
