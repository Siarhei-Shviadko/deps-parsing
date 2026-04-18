from typing import Any

from deps_parsing.domain.exceptions import UnifiedDataNotFound
from deps_parsing.infrastructure.proxies import UnifiedDataElement, UnifiedDataImage

__all__ = ["FakeUnifierProxy"]


class FakeUnifierProxy:
    def __init__(self) -> None:
        self._storage: dict[str, dict[str, Any]] = {}

    def find_unified_data_by_document_id(
        self,
        document_id: str,
        unified_data_types: list[UnifiedDataElement] | None = None,
    ) -> dict[str, Any]:
        if udata := self._storage.get(document_id):
            return udata

        raise UnifiedDataNotFound

    def get_preprocessed_images(self, document_id: str) -> list[UnifiedDataImage]:
        udata = self.find_unified_data_by_document_id(document_id, [UnifiedDataElement.IMAGE])

        return [
            UnifiedDataImage.from_dict(image) for image in udata["elements"] if image["originalImageId"] is not None
        ]

    def get_original_images(self, document_id: str) -> list[UnifiedDataImage]:
        udata = self.find_unified_data_by_document_id(document_id, [UnifiedDataElement.IMAGE])

        return [UnifiedDataImage.from_dict(image) for image in udata["elements"] if image["originalImageId"] is None]

    def save(self, entity_id: str, udata: dict[str, Any]) -> None:
        self._storage[entity_id] = udata
