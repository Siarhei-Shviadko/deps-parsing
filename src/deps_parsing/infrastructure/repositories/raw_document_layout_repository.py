import json
import logging
from typing import Any

from deps_document_layout.model import ParsingType
from deps_object_storage import ObjectStorage

from deps_parsing.constants import DOCUMENT_LAYOUT_FOLDER
from deps_parsing.domain.interfaces import IRawDocumentLayoutRepository

__all__ = ["RawDocumentLayoutRepository"]


class RawDocumentLayoutRepository(IRawDocumentLayoutRepository):
    def __init__(self, object_storage: ObjectStorage, file_extension: str) -> None:
        self._object_storage = object_storage
        self.file_extension = file_extension
        self._logger = logging.getLogger(self.__class__.__name__)

    def save(self, layout_id: str, layout: dict[int, Any], parsing_type: ParsingType) -> str:
        filename = self._build_filename(layout_id, parsing_type)
        content = json.dumps(layout).encode("utf-8")
        return self._object_storage.upload(filename, content, replace_if_exists=True)

    def layout_of_id(self, layout_id: str, parsing_type: ParsingType) -> dict[int, Any]:
        layout = self._object_storage.download(self._build_filename(layout_id, parsing_type))
        return json.loads(layout)

    def delete(self, layout_id: str, parsing_type: ParsingType) -> None:
        self._object_storage.delete(self._build_filename(layout_id, parsing_type))

    def _build_filename(self, layout_id: str, parsing_type: ParsingType) -> str:
        return f"{DOCUMENT_LAYOUT_FOLDER}/{layout_id}/{parsing_type.value}.{self.file_extension}"
