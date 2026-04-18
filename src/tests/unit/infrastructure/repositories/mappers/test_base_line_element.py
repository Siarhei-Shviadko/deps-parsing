from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    BaseLineElementMapper,
)


def test_base_element_mapper__ok(base_line_element_factory):
    orig = base_line_element_factory()
    restored = BaseLineElementMapper.from_dict(BaseLineElementMapper.to_dict(orig))
    assert orig.order == restored["order"]
    assert orig.confidence == restored["confidence"]
    assert orig.polygon == restored["polygon"]
