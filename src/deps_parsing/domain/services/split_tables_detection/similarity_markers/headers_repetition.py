import re

from deps_document_layout.model import Page

from ..markers import SimilarityMarkers
from .abstract_marker import AbstractMarker

__all__ = ["HeadersRepetitionMarker"]


class HeadersRepetitionMarker(AbstractMarker):
    """
    This function checks column headers:
    If the second page table repeats the header row from the first page table.
    """

    type = SimilarityMarkers.HEADERS_REPETITION

    def is_present(self, first_page: Page, second_page: Page) -> bool:
        first_page_table = self.last_table_of_page(first_page)
        second_page_table = self.first_table_of_page(second_page)

        last_tab_headers: list[str] = [cell.content for cell in first_page_table.cells if cell.row_index == 0]
        first_tab_headers: list[str] = [cell.content for cell in second_page_table.cells if cell.row_index == 0]

        for head1, head2 in zip(last_tab_headers, first_tab_headers):
            head1 = re.sub(r"[\n\t ]", "", head1)
            head2 = re.sub(r"[\n\t ]", "", head2)

            if head1.lower() != head2.lower():
                return False

        return True
