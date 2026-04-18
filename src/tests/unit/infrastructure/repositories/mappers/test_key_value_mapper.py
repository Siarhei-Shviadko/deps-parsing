from uuid import uuid4

from deps_parsing.application import ParsingType
from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    KeyValuePairMapper,
)


def test_key_value_mapper__ok(key_value_pair_factory):
    orig = key_value_pair_factory()
    restored = KeyValuePairMapper.from_dict(
        KeyValuePairMapper.to_dict(orig, page_id=uuid4().hex, parsing_type=ParsingType("TESSERACT")),
    )

    assert orig == restored
