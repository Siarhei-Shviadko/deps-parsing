from deps_document_layout.model import Page

from ..markers import SimilarityMarkers
from .abstract_marker import AbstractMarker

__all__ = ["TextBetweenMarker"]


class TextBetweenMarker(AbstractMarker):
    """
    This marker checks if there is any text located between tables.
    In algorithm, we check if the last word of the first page goes after its last table
        and if the first word at next page goes before its first table.
    """

    type = SimilarityMarkers.TEXT_BETWEEN_TABLES

    def is_present(self, first_page: Page, second_page: Page) -> bool:
        first_page_table = self.last_table_of_page(first_page)
        second_page_table = self.first_table_of_page(second_page)

        last_table_y_max: float = max([i.y for i in first_page_table.polygon])
        first_table_y_min: float = min([i.y for i in second_page_table.polygon])

        if not first_page.paragraphs or not second_page.paragraphs:
            return False
        if not first_page.paragraphs[-1].lines or not second_page.paragraphs[0].lines:
            return False
        if not first_page.paragraphs[-1].lines[-1].words or not second_page.paragraphs[0].lines[0].words:
            return False

        last_word_coords: list[float] = [i.y for i in first_page.paragraphs[-1].lines[-1].words[-1].polygon]
        first_word_coords: list[float] = [i.y for i in second_page.paragraphs[0].lines[0].words[0].polygon]

        return any(
            word_y_max > last_table_y_max or word_y_min < first_table_y_min
            for word_y_max, word_y_min in zip(last_word_coords, first_word_coords)
        )
