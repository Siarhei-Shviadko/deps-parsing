from deps_parsing.infrastructure.repositories.document_layout.mappers import LineMapper


def test__line_mapper__ok(line_factory):
    orig = line_factory()
    restored = LineMapper.from_dict(LineMapper.to_dict(orig))

    assert orig == restored
