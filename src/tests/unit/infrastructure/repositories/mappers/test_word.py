from deps_parsing.infrastructure.repositories.document_layout.mappers import WordMapper


def test__word_mapper__ok(word_factory):
    orig = word_factory()
    restored = WordMapper.from_dict(WordMapper.to_dict(orig))

    assert orig == restored
