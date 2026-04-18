from deps_parsing.infrastructure.repositories.document_layout.mappers import GroupMapper


def test__group_mapper__ok(group_factory):
    orig = group_factory()
    restored = GroupMapper.from_dict(GroupMapper.to_dict(orig))
    assert orig == restored
