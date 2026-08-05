from deps_document_layout.model import ParsingType as DLParsingType
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.application import ENGINES, LayoutType, SemanticParsingType
from deps_parsing.application.engine_registry import _NAMES


def _codes_for_layout(layout_type: LayoutType) -> set[str]:
    return {engine.code for engine in ENGINES if engine.layout_type == layout_type}


def test_engine_registry__covers_all_enum_members():
    assert _codes_for_layout(LayoutType.DOCUMENT_LAYOUT) == {
        member.value for member in DLParsingType if member.value in _NAMES
    }
    assert _codes_for_layout(LayoutType.TABULAR_LAYOUT) == {
        member.value for member in TLParsingType if member.value in _NAMES
    }
    assert _codes_for_layout(LayoutType.SEMANTIC_LAYOUT) == {
        member.value for member in SemanticParsingType if member.value in _NAMES
    }
