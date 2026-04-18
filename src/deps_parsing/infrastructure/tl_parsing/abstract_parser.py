import logging
from abc import ABC, abstractmethod

from deps_tabular_layout.models import TabularLayout

from deps_parsing.domain.interfaces import ICellCommandRepository
from deps_parsing.infrastructure.proxies import DocumentProxy

__all__ = ["AbstractTabularLayoutParser"]


class AbstractTabularLayoutParser(ABC):
    def __init__(
        self,
        documents_proxy: DocumentProxy,
        cell_command_repository: ICellCommandRepository,
    ) -> None:
        self._documents_proxy = documents_proxy
        self._cell_repository = cell_command_repository

        self._logger = logging.getLogger(self.__class__.__name__)

    def parse(
        self,
        layout: TabularLayout,
    ) -> TabularLayout:
        blob: bytes = self._documents_proxy.get_document_files(layout.id())

        return self._perform_parsing(blob, layout)

    @abstractmethod
    def _perform_parsing(self, blob: bytes, tabular_layout: TabularLayout) -> TabularLayout:
        ...
