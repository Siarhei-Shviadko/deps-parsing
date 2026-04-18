from typing import Protocol

from deps_tabular_layout.models import TabularLayout

__all__ = ["ITabularLayoutCommandRepository"]


class ITabularLayoutCommandRepository(Protocol):
    def save(self, layout: TabularLayout) -> None:
        ...

    def delete(self, layout_id: str, tenant_id: str) -> None:
        ...
