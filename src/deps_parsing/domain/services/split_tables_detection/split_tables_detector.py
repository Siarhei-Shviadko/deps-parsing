import math
from typing import Generator

from deps_document_layout.model import DocumentLayout, Page, ParsingType

from .markers import SimilarityMarkers, SimilarityMarkersWeight
from .similarity_markers import (
    AbstractMarker,
    ColumnsAlignmentMarker,
    ColumnsCountMarker,
    HeadersRepetitionMarker,
    IndexingContinuationMarker,
    TextBetweenMarker,
)
from .tables_group import TablesGroup

__all__ = ["SplitTablesDetectionService"]

FIRST_VALUE_IDX, LAST_VALUE_IDX = 0, -1


class SplitTablesDetectionService:
    _MINIMAL_SIMILARITY = -math.inf

    def __init__(self, similarity_threshold: float, weights: dict[SimilarityMarkers, dict[bool, float]]) -> None:
        self.weights = SimilarityMarkersWeight(
            similarity_threshold=similarity_threshold,
            weights=weights,
        )

        self.markers: list[AbstractMarker] = [
            TextBetweenMarker(),
            HeadersRepetitionMarker(),
            ColumnsAlignmentMarker(),
            ColumnsCountMarker(),
            IndexingContinuationMarker(),
        ]

    def detect_split_tables(self, document_layout: DocumentLayout, for_parsing_type: ParsingType) -> list[TablesGroup]:
        detected_groups: list[TablesGroup] = []
        current_group = TablesGroup(parsing_type=for_parsing_type)

        for first_page, second_page in self._iter_paired_pages(document_layout, for_parsing_type):
            similarity: float = self._calculate_tables_similarity(first_page, second_page)

            if similarity > self.weights.similarity_threshold:
                current_group.add(for_page=first_page.page_number, table=first_page.tables[LAST_VALUE_IDX])
                current_group.add(for_page=second_page.page_number, table=second_page.tables[FIRST_VALUE_IDX])
            elif current_group.has_tables():
                detected_groups.append(current_group)
                current_group = TablesGroup(parsing_type=for_parsing_type)

        if current_group.has_tables():
            detected_groups.append(current_group)

        return detected_groups

    def _iter_paired_pages(
        self,
        document_layout: DocumentLayout,
        with_parsing_type: ParsingType,
    ) -> Generator[tuple[Page, Page], None, None]:
        pages_with_parsing_type = [page for page in document_layout.pages if page.parsing_type == with_parsing_type]

        for page_index, current_page in enumerate(pages_with_parsing_type):
            if page_index >= len(document_layout.pages) - 1:
                continue

            yield current_page, document_layout.pages[page_index + 1]

    def _calculate_tables_similarity(self, first_page: Page, second_page: Page) -> float:
        """
        Calculates the similarity between the Last Table on the first page and the First Table on the second page.
        Similarity is a numeric value between -inf and +inf that represents how likely those tables to be merged.
        If the similarity is greater than the threshold, the tables will be merged.
        """
        if not all((first_page.has_table(), second_page.has_table())):
            return self._MINIMAL_SIMILARITY

        similarity = 0.0
        for marker in self.markers:
            # To save compute time we skip the type if it has no effect on the similarity
            if not self.weights.marker_has_weight(marker.type):
                continue

            marker_is_present: bool = marker.is_present(first_page, second_page)

            similarity += self.weights.marker_weight(marker.type, is_present=marker_is_present)

        return similarity
