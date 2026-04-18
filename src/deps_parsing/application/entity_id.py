from typing import Union

from deps_document_layout.model import EntityId as DLEntityId
from deps_tabular_layout.models import EntityId as TLEntityId

__all__ = ["EntityId"]

EntityId = Union[DLEntityId, TLEntityId]
