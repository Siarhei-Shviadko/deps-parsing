from typing import Sequence

from azure.ai.formrecognizer import (
    BoundingRegion,
    DocumentBarcode,
    DocumentFormula,
    DocumentKeyValuePair,
    DocumentLanguage,
    DocumentLine,
    DocumentPage,
    DocumentParagraph,
    DocumentSelectionMark,
    DocumentTable,
    DocumentWord,
)
from azure.ai.formrecognizer import Point as DocumentPoint
from deps_document_layout.model import Point, Polygon

from ..spans import SpansOf

__all__ = ["StructuredPage"]


class StructuredPage:  # noqa: WPS214
    def __init__(self, source_id: str, page_number: int, file_path: str, languages: list[DocumentLanguage]) -> None:
        self.source_id = source_id
        self.page_number = page_number
        self.file_path = file_path
        self.languages = languages

        self._paragraphs: list[DocumentParagraph] = []
        self._tables: list[DocumentTable] = []
        self._key_value_pairs: list[DocumentKeyValuePair] = []

        self._parsed_page: DocumentPage

    @property
    def paragraphs(self) -> list[DocumentParagraph]:
        return self._paragraphs

    @property
    def tables(self) -> list[DocumentTable]:
        return self._tables

    @property
    def key_value_pairs(self) -> list[DocumentKeyValuePair]:
        return self._key_value_pairs

    @property
    def parsed_page(self) -> DocumentPage:
        return self._parsed_page

    @property
    def width(self) -> float:
        return self._parsed_page.width

    @property
    def height(self) -> float:
        return self._parsed_page.height

    @property
    def angle(self) -> float:
        return self._parsed_page.angle

    @property
    def unit(self) -> str:
        return self._parsed_page.unit

    def add_paragraph(self, paragraph: DocumentParagraph) -> None:
        self._paragraphs.append(paragraph)

    def add_table(self, table: DocumentTable) -> None:
        self._tables.append(table)

    def add_key_value_pair(self, key_value_pair: DocumentKeyValuePair) -> None:
        self._key_value_pairs.append(key_value_pair)

    def add_parsed_page(self, page: DocumentPage) -> None:
        self._parsed_page = page

    def lines_of(self, paragraph: DocumentParagraph) -> list[DocumentLine]:
        return [line for line in self.parsed_page.lines if SpansOf(paragraph).include(SpansOf(line))]

    def words_of(self, line: DocumentLine) -> list[DocumentWord]:
        return [word for word in self.parsed_page.words if SpansOf(line).include(SpansOf(word))]

    def selection_marks_of(self, line: DocumentLine) -> list[DocumentSelectionMark]:
        return [mark for mark in self.parsed_page.selection_marks if SpansOf(line).include(SpansOf(mark))]

    def barcodes_of(self, line: DocumentLine) -> list[DocumentBarcode]:
        return [barcode for barcode in self.parsed_page.barcodes if SpansOf(line).include(SpansOf(barcode))]

    def formulas_of(self, line: DocumentLine) -> list[DocumentFormula]:
        return [formula for formula in self.parsed_page.formulas if SpansOf(line).include(SpansOf(formula))]

    def convert_abs_coordinates_to_relative(self, document_polygon: Sequence[DocumentPoint]) -> Polygon:
        return tuple(
            (
                (
                    Point(x=max(point.x, 0.0) / self.width, y=max(point.y, 0.0) / self.height)
                    for point in document_polygon
                )
            ),
        )

    def convert_bounding_region_to_polygon(self, bounding_regions: BoundingRegion) -> Polygon:
        return self.convert_abs_coordinates_to_relative(bounding_regions.polygon)
