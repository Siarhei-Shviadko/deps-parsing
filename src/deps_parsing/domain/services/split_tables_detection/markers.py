from dataclasses import dataclass
from enum import Enum

from deps_parsing.domain.constants import ABSENCE, PRESENCE

__all__ = ["SimilarityMarkers", "SimilarityMarkersWeight"]


class SimilarityMarkers(str, Enum):
    HEADERS_REPETITION = "headers-repetition"
    COLUMNS_ALIGNMENT = "columns-alignment"
    TEXT_BETWEEN_TABLES = "text-between-tables"
    COLUMNS_COUNT = "columns-count"
    INDEXING_CONTINUATION = "indexing-continuation"


@dataclass
class SimilarityMarkersWeight:
    similarity_threshold: float
    weights: dict[SimilarityMarkers, dict[bool, float]]

    def marker_weight(self, marker: SimilarityMarkers, is_present: bool) -> float:
        return self.weights[marker][is_present]

    def marker_has_weight(self, marker: SimilarityMarkers) -> bool:
        if marker not in self.weights:
            return False

        return self.weights[marker][PRESENCE] != 0 or self.weights[marker][ABSENCE] != 0

    @classmethod
    def make_default_weights(cls) -> dict[SimilarityMarkers, dict[bool, float]]:
        return {
            SimilarityMarkers.HEADERS_REPETITION: {PRESENCE: 1, ABSENCE: 0},
            SimilarityMarkers.TEXT_BETWEEN_TABLES: {PRESENCE: 0, ABSENCE: 1},
            SimilarityMarkers.COLUMNS_COUNT: {PRESENCE: 1, ABSENCE: -1},
            SimilarityMarkers.INDEXING_CONTINUATION: {PRESENCE: 1, ABSENCE: 0},
            SimilarityMarkers.COLUMNS_ALIGNMENT: {PRESENCE: 0.8, ABSENCE: -0.7},
        }

    @classmethod
    def calculate_default_threshold(cls) -> float:
        default_weights = cls.make_default_weights()

        summation = sum(weight[PRESENCE] + weight[ABSENCE] for weight in default_weights.values())

        return round(summation / 2, 2)
