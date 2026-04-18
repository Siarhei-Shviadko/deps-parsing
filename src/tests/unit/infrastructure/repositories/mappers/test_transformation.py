from deps_parsing.infrastructure.repositories.document_layout.mappers import (
    TransformationsMapper,
)


def test_transformations_mapper__ok(transformations_factory):
    orig = transformations_factory()
    restored = TransformationsMapper.from_dict(TransformationsMapper.to_dict(orig))

    assert orig == restored


def test_transformations_mapper__thresholding_none__ok(transformations_factory):
    orig = transformations_factory(thresholding=None)
    restored = TransformationsMapper.from_dict(TransformationsMapper.to_dict(orig))

    assert orig == restored
