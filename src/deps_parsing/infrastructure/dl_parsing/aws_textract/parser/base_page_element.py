from typing import Union, cast

from deps_document_layout.model import LineBuilder, ParagraphBuilder, Polygon

from .structured_response import StructuredResponse
from .types import AWSCheckbox, AWSKeyValuePair, AWSWord

__all__ = ["PageElementParser"]


class PageElementParser:
    def __init__(self, response: StructuredResponse) -> None:
        self._response = response

    def _add_word_or_checkbox(self, builder: LineBuilder, element: Union[AWSWord, AWSCheckbox]) -> LineBuilder:
        type_mapping = {
            AWSWord: self._add_word_to_line,
            AWSCheckbox: self._add_checkbox_to_line,
            AWSKeyValuePair: self._add_key_value_to_line,
        }
        return type_mapping[type(element)](builder, element)

    def _add_word_to_line(self, builder: LineBuilder, word: AWSWord) -> LineBuilder:
        return (
            builder.with_word()
            .with_content(word.text)
            .with_confidence(word.confidence)
            .with_polygon(self._response.polygon_of(word))
            .with_style()
        )

    def _add_checkbox_to_line(self, builder: LineBuilder, checkbox: AWSCheckbox) -> LineBuilder:
        builder = (
            builder.with_selection_mark()
            .with_state(str(checkbox.is_selected()))
            .with_polygon(self._response.polygon_of(checkbox))
            .with_confidence(checkbox.confidence)
        )
        return cast(LineBuilder, builder)

    def _add_key_value_to_line(self, builder: LineBuilder, key_value: AWSKeyValuePair) -> LineBuilder:
        """Happens when several checkboxes are in the same table cell"""
        for element in key_value.key:
            builder = self._add_word_or_checkbox(builder, element)
        for element in key_value.value.children:
            builder = self._add_word_or_checkbox(builder, element)
        return builder

    @staticmethod
    def _add_paragraph_and_line(
        builder: ParagraphBuilder,
        polygon: Polygon,
        content: str,
        confidence: float,
    ) -> LineBuilder:
        return (
            builder.with_confidence(confidence)
            .with_polygon(polygon)
            .with_content(content)
            .with_line()
            .with_confidence(confidence)
            .with_polygon(polygon)
            .with_content(content)
        )
