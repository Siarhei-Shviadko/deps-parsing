from deps_document_layout.model import Page

from ..markers import SimilarityMarkers
from .abstract_marker import AbstractMarker

__all__ = ["ColumnsCountMarker"]


class ColumnsCountMarker(AbstractMarker):
    """
    This Marker checks that number of columns stay consistent between tables.
    """

    type = SimilarityMarkers.COLUMNS_COUNT

    def is_present(self, first_page: Page, second_page: Page) -> bool:
        first_page_table = self.last_table_of_page(first_page)
        second_page_table = self.first_table_of_page(second_page)

        return first_page_table.column_count == second_page_table.column_count
