from typing import Optional

from deps_document_layout.model import (
    DocumentLayout,
    LineBuilder,
    PageBuilder,
    ParagraphBuilder,
    ParsingType,
    Point,
    Polygon,
    TableBuilder,
)

from deps_parsing.infrastructure.proxies import UnifiedDataImage

from .engine import Bbox, DepsStructuredResponse, SourceBboxCoordinates, Table, WordBox

__all__ = ["DepsParser"]

FIRST_ELEMENT: int = 0
DEFAULT_CONFIDENCE: float = 1.0
DEPS_DIMENSION_UNIT: str = "px"


class DepsParser:
    def __init__(self, image: UnifiedDataImage, parsing_type: ParsingType, language: Optional[str] = None) -> None:
        self._image = image
        self._parsing_type = parsing_type
        self._language = language

    def add_response_to_page(self, response: DepsStructuredResponse, layout: DocumentLayout) -> DocumentLayout:
        page_builder = self._add_page(layout)
        if response.paragraphs:
            page_builder = self._add_paragraphs(page_builder, response)
        if response.tables_data:
            page_builder = self._add_tables(page_builder, response.tables_data)
        page_builder.build()

        return layout

    def _add_page(self, layout: DocumentLayout) -> PageBuilder:
        builder = (
            layout.add_page()
            .with_id(self._image.id)
            .with_page_number(self._image.page)
            .with_parsing_type(self._parsing_type)
            .with_dimension(width=self._image.width, height=self._image.height, unit=DEPS_DIMENSION_UNIT)
            .with_file_path(self._image.blob_name)
            .with_transformations()
        )

        if self._image.applied_transformation:
            transformations = self._image.applied_transformation.parameters.kwargs
            if (angle := transformations.get("angle")) is not None:
                builder = builder.with_angle(angle)
            if (orientation := transformations.get("orientation")) is not None:
                builder = builder.with_orientation(orientation)

        if self._language is not None:
            builder = builder.with_language(self._language, confidence=DEFAULT_CONFIDENCE)

        return builder

    def _add_tables(self, builder: PageBuilder, tables: list[Table]) -> TableBuilder:
        for table in tables:
            builder = (
                builder.with_table()
                .with_column_count(len(table.columns))
                .with_row_count(len(table.rows))
                .with_polygon(
                    self._source_bbox_coordinates_to_polygon([table.source_bbox_coordinates])
                    if table.source_bbox_coordinates
                    else self._build_polygon_from_bbox(table.coordinates),
                )
            )
            builder = self._add_cells(builder, table)

        return builder

    def _add_cells(self, builder: PageBuilder, table: Table) -> TableBuilder:
        for cell in table.cells:
            builder = (
                builder.with_cell()
                .with_content(cell.value)
                .with_column_index(cell.coordinates.column)
                .with_column_span(cell.coordinates.colspan)
                .with_row_index(cell.coordinates.row)
                .with_row_span(cell.coordinates.rowspan)
                .with_polygon(self._source_bbox_coordinates_to_polygon(cell.source_bbox_coordinates))
            )
        return builder

    def _add_paragraphs(self, builder: PageBuilder, response: DepsStructuredResponse) -> PageBuilder:
        builder = (
            builder.with_paragraph()
            .with_content(response.paragraphs[FIRST_ELEMENT]["content"])
            .with_polygon(
                self._build_polygon_from_bbox(response.paragraphs[0]["bbox"]),
            )
        )
        return self._add_lines(builder, response)

    def _add_lines(self, builder: ParagraphBuilder, response: DepsStructuredResponse) -> LineBuilder:
        for line, words in zip(response.text_lines, response.words):
            builder = (
                builder.with_line()
                .with_content(line["content"])
                .with_polygon(
                    self._build_polygon_from_bbox(line["bbox"]),
                )
            )
            builder = self._add_words(builder, words)
        return builder

    def _add_words(self, builder: LineBuilder, words: list[WordBox]) -> LineBuilder:
        for word in words:
            builder = (
                builder.with_word()
                .with_content(word.content)
                .with_polygon(
                    self._build_polygon_from_bbox(word.bbox),
                )
                .with_confidence(float(word.confidence))
                .with_style()
            )
        return builder

    def _source_bbox_coordinates_to_polygon(self, coords: list[SourceBboxCoordinates]) -> Polygon:
        return self._build_polygon_from_bbox(coords[FIRST_ELEMENT].bboxes[FIRST_ELEMENT])

    @staticmethod
    def _build_polygon_from_bbox(bbox: Bbox) -> Polygon:
        p1 = Point(bbox.x, bbox.y)
        p2 = Point(bbox.x + bbox.w, bbox.y)
        p3 = Point(bbox.x + bbox.w, bbox.y + bbox.h)
        p4 = Point(bbox.x, bbox.y + bbox.h)
        return p1, p2, p3, p4
