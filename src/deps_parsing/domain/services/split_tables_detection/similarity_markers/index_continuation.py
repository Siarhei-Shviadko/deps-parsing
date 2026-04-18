import re

from deps_document_layout.model import Cell, Page

from ..markers import SimilarityMarkers
from .abstract_marker import AbstractMarker

__all__ = ["IndexingContinuationMarker"]

NUM_PATTERN = re.compile(r"\d+[\).\s]*$")
CHAR_PATTER = re.compile(r"[a-zA-Z][\).\s]*$")


# fmt: off
class IndexingContinuationMarker(AbstractMarker):
    type = SimilarityMarkers.INDEXING_CONTINUATION

    def is_present(self, first_page: Page, second_page: Page) -> bool:
        first_page_table = self.last_table_of_page(first_page)
        second_page_table = self.first_table_of_page(second_page)

        table1_length = first_page_table.row_count
        table2_length = second_page_table.row_count

        first_table__last_cell: Cell = [
            cell
            for cell in first_page_table.cells
            if cell.column_index == 0 and cell.row_index + cell.row_span == table1_length
        ][0]
        second_table__first_cell: Cell = second_page_table.cells[0]

        result = self._check_if_continuous_indexing(first_table__last_cell.content, second_table__first_cell.content)

        # The `result` could be negative, because first row could be occupied by headers,
        #   so we also checked first cell in the second row.
        # But first we check if the second table has more than one row at all.
        if not result and second_table__first_cell.row_index + second_table__first_cell.row_span != table2_length:
            second_table__second_row_id: int = (
                second_page_table.cells[0].row_index + second_page_table.cells[0].row_span
            )
            second_table__second_cell: Cell = [
                cell
                for cell in second_page_table.cells
                if cell.column_index == 0 and cell.row_index == second_table__second_row_id
            ][0]

            result = self._check_if_continuous_indexing(
                previous_label=first_table__last_cell.content,
                next_label=second_table__second_cell.content,
            )

        return result

    def _check_if_continuous_indexing(self, previous_label: str, next_label: str) -> bool:
        if not self._is_valid_label_format(previous_label, next_label):
            return False

        return (
            self._is_alphabetical_continuation(previous_label, next_label)
            or self._is_numeric_continuation(previous_label, next_label)
        )

    def _is_valid_label_format(self, previous_label: str, next_label: str) -> bool:
        # Match the whole string with the pattern and check if it's exactly equal to the label
        match1 = re.fullmatch(NUM_PATTERN, previous_label.strip())
        match2 = re.fullmatch(NUM_PATTERN, next_label.strip())
        if match1 is not None and match2 is not None:
            return True

        match3 = re.fullmatch(CHAR_PATTER, previous_label.strip())
        match4 = re.fullmatch(CHAR_PATTER, next_label.strip())

        return match3 is not None and match4 is not None

    def _extract_label_number(self, label) -> int:
        # Strict pattern to match numbers possibly followed by '.' or ')'
        return int(re.search(r"\d+", label).group()) if re.search(NUM_PATTERN, label) else 0

    def _extract_label_char(self, label) -> str:
        # Strict pattern to match single characters possibly followed by '.' or ')'
        return re.search(r"[a-zA-Z]", label).group().lower() if re.search(CHAR_PATTER, label) else ""

    def _is_numeric_continuation(self, previous_label: str, next_label: str) -> bool:
        previous_numeric_index = self._extract_label_number(previous_label)
        next_numeric_index = self._extract_label_number(next_label)

        if next_numeric_index is not None and previous_numeric_index is not None:
            return next_numeric_index == previous_numeric_index + 1

        return False

    def _is_alphabetical_continuation(self, previous_label: str, next_label: str) -> bool:
        previous_char = self._extract_label_char(previous_label)
        next_char = self._extract_label_char(next_label)

        if previous_char and next_char:
            return ord(next_char) == ord(previous_char) + 1

        return False
