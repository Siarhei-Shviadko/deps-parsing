from deps_document_layout.model import EntityId, Group, RawGroup

__all__ = ["GroupMapper"]


class GroupMapper:
    @classmethod
    def to_dict(cls, group: Group) -> RawGroup:
        return RawGroup(id=group.id(), name=group.name, members=[m() for m in group.members])

    @classmethod
    def from_dict(cls, group: RawGroup) -> Group:
        members = frozenset(EntityId(m) for m in group["members"])
        return Group(
            id_=EntityId(group["id"]),
            name=group["name"],
            members=members,
        )
