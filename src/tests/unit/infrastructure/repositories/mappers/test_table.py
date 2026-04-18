from uuid import uuid4

from deps_parsing.application import ParsingType
from deps_parsing.infrastructure.repositories.document_layout.mappers import TableMapper


def test_table_mapper__ok(table_factory):
    orig = table_factory()
    restored = TableMapper.from_dict(
        TableMapper.to_dict(orig, page_id=uuid4().hex, parsing_type=ParsingType("TESSERACT")),
    )

    assert orig == restored
