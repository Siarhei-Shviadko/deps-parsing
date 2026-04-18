from deps_document_layout.model import Guard, ImmutableCheck

__all__ = [
    "CommandChannel",
]


class CommandChannel:
    name = Guard[str](str, ImmutableCheck())

    def __init__(self, name: str) -> None:
        self.name = name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, CommandChannel) and other.name == self.name
