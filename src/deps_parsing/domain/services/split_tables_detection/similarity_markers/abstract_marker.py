from abc import ABC, abstractmethod

from deps_document_layout.model import Page, Table

from ..markers import SimilarityMarkers

__all__ = ["AbstractMarker"]

FIRST_VALUE_IDX, LAST_VALUE_IDX = 0, -1


class AbstractMarker(ABC):
    type: SimilarityMarkers

    @abstractmethod
    def is_present(self, first_page: Page, second_page: Page) -> bool:
        pass

    def first_table_of_page(self, page: Page) -> Table:
        return page.tables[FIRST_VALUE_IDX]

    def last_table_of_page(self, page: Page) -> Table:
        return page.tables[LAST_VALUE_IDX]
