import logging
from abc import ABC, abstractmethod

from deps_object_storage import ObjectStorage
from deps_tabular_layout.models import TabularLayout

from deps_parsing.domain.interfaces import ICellCommandRepository

__all__ = ["AbstractTabularLayoutParser"]


class AbstractTabularLayoutParser(ABC):
    def __init__(self, storage: ObjectStorage, cell_command_repository: ICellCommandRepository) -> None:
        self._storage = storage
        self._cell_repository = cell_command_repository

        self._logger = logging.getLogger(self.__class__.__name__)

    def parse(self, file_path: str, layout: TabularLayout) -> TabularLayout:
        blob: bytes = self._storage.download(file_path)

        return self._perform_parsing(blob, layout)

    @abstractmethod
    def _perform_parsing(self, blob: bytes, tabular_layout: TabularLayout) -> TabularLayout:
        ...
