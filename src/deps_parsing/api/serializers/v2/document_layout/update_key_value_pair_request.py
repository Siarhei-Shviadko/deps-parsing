from typing import List, Optional

from deps_document_layout.model import (
    KeyValuePairElementUpdateData,
    KeyValuePairUpdateData,
)
from deps_document_layout.serializers.document_layout import SerializedPoint

from ...base import ConfiguredBaseModel

__all__ = ["SerializedKeyValuePairElementUpdateData", "UpdateKeyValuePairRequest"]


class SerializedKeyValuePairElementUpdateData(ConfiguredBaseModel):
    content: Optional[str] = None
    polygon: Optional[List[SerializedPoint]] = None

    def update_data(self) -> KeyValuePairElementUpdateData:
        return KeyValuePairElementUpdateData(
            content=self.content,
            polygon=tuple(point.to_model() for point in self.polygon) if self.polygon is not None else None,
        )


class UpdateKeyValuePairRequest(ConfiguredBaseModel):
    key: Optional[SerializedKeyValuePairElementUpdateData] = None
    value: Optional[SerializedKeyValuePairElementUpdateData] = None

    @property
    def update_data(self) -> KeyValuePairUpdateData:
        return KeyValuePairUpdateData(
            key=self.key.update_data() if self.key else None,
            value=self.value.update_data() if self.value else None,
        )
