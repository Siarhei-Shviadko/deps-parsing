from .base import NotFoundError

__all__ = ["DocumentLayoutNotFound"]


class DocumentLayoutNotFound(NotFoundError):
    def __init__(self, id_: str) -> None:
        super().__init__(f"Document layout `{id_}` not found")
