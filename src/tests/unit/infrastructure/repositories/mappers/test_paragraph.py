from uuid import uuid4

from deps_parsing.application import ParsingType
from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    ParagraphMapper,
)


def test_paragraph_mapper(paragraph_factory):
    orig = paragraph_factory()
    restored = ParagraphMapper.from_dict(
        ParagraphMapper.to_dict(orig, page_id=uuid4().hex, parsing_type=ParsingType("TESSERACT")),
    )

    assert orig == restored
