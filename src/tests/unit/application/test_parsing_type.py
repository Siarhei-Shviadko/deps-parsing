from typing import Union

import pytest
from deps_document_layout.model import ParsingType as DLParsingType
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.application import ParsingType
from deps_parsing.domain.exceptions import UnsupportedParsingType


@pytest.mark.parametrize(
    "raw_type,target",
    [
        (TLParsingType.CSV.value, TLParsingType.CSV),
        (TLParsingType.EXCEL.value, TLParsingType.EXCEL),
        (DLParsingType.TESSERACT.value, DLParsingType.TESSERACT),
        (DLParsingType.AZURE_FORM_RECOGNIZER.value, DLParsingType.AZURE_FORM_RECOGNIZER),
        (DLParsingType.AWS_TEXTRACT.value, DLParsingType.AWS_TEXTRACT),
    ],
)
def test_parsing_type__dl_or_tl_type__ok(raw_type: str, target: Union[TLParsingType, DLParsingType]):
    assert ParsingType.supports(raw_type)

    parsing_type = ParsingType(raw_type)

    assert parsing_type.value == target
    assert parsing_type.layout_type == target.__class__


@pytest.mark.parametrize(
    "extra_extension,expected_type",
    [
        ("xlsx", TLParsingType.EXCEL),
        ("xls", TLParsingType.EXCEL),
    ],
)
def test_parsing_type__extra_type__ok(extra_extension: str, expected_type: TLParsingType):
    assert ParsingType.supports(extra_extension)
    assert ParsingType(extra_extension).value == expected_type


def test_parsing_type__unknown_type__error():
    with pytest.raises(UnsupportedParsingType):
        ParsingType("HelloWorld")
