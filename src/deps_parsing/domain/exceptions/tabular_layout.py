from .base import NotFoundError

__all__ = ["TabularLayoutNotFound"]


class TabularLayoutNotFound(NotFoundError):
    def __init__(self, id_: str) -> None:
        super().__init__(f"Tabular layout `{id_}` not found")
