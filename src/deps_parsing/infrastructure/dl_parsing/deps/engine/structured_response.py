from typing import Any, Optional

from .types import Bbox, Table, TextLine, WordBox

__all__ = ["DepsStructuredResponse"]

CommonData = list[dict[str, Any]]


class DepsStructuredResponse:
    def __init__(self, response: dict[str, Any], language: Optional[str] = None) -> None:
        self.language = language
        self.orig_response = response
        self.tables_data = (
            [Table.from_dict(**table_data) for table_data in response["tables_data"]]
            if response.get("tables_data")
            else []
        )
        self.paragraphs: CommonData = []
        self.text_lines: CommonData = []
        self.words: list[list[WordBox]] = []

        if ocr_data := self.orig_response.get("ocr_data"):
            self._build_paragraph_data([TextLine.from_dict(**data) for data in ocr_data])

    def _build_paragraph_data(self, text_lines: list[TextLine]) -> None:
        bbox = None
        content = []
        for line in text_lines:
            line_content, line_bbox = self._build_line_data(line)
            bbox = self._update_bbox(bbox, line_bbox)
            content.append(line_content)
        self.paragraphs.append({"content": "\n".join(content), "bbox": bbox})

    def _build_line_data(self, text_line: TextLine) -> tuple[str, Bbox]:
        bbox = None
        line = []
        line_words = []
        for word in text_line.word_boxes:
            bbox = self._update_bbox(bbox, word.bbox)
            line.append(word.content)
            line_words.append(word)
        self.words.append(line_words)
        line_content = " ".join(line)
        self.text_lines.append({"content": line_content, "bbox": bbox})
        return line_content, bbox

    def _update_bbox(self, orig_bbox: Optional[Bbox], new_bbox: Bbox) -> Bbox:
        if orig_bbox is None:
            return new_bbox
        if orig_bbox.x > new_bbox.x:
            orig_bbox.x = new_bbox.x
        if orig_bbox.y > new_bbox.y:
            orig_bbox.y = new_bbox.y
        if (orig_bbox.h + orig_bbox.y) < (new_height := new_bbox.y + new_bbox.h):
            orig_bbox.h = new_height - orig_bbox.y
        if (orig_bbox.x + orig_bbox.w) < (new_width := new_bbox.x + new_bbox.w):
            orig_bbox.w = new_width - orig_bbox.x
        return orig_bbox
