from typing import cast

from deps_document_layout.model import (
    KeyValuePairBuilder,
    KeyValuePairElementBuilder,
    PageBuilder,
)

from deps_parsing.domain.model import CheckmarkValue

from .base_page_element import PageElementParser
from .types import AWSKeyValuePair, AWSValue

__all__ = ["KeyValuePairDataParser"]


class KeyValuePairDataParser(PageElementParser):
    def add_key_value_pair(self, builder: PageBuilder, kvp: AWSKeyValuePair) -> PageBuilder:
        builder = builder.with_key_value_pair().with_confidence(kvp.confidence)
        builder = self._add_key(builder, kvp)
        builder = self._add_value(builder, kvp.value)
        return cast(PageBuilder, builder)

    def _add_key(
        self,
        builder: KeyValuePairBuilder,
        kvp: AWSKeyValuePair,
    ) -> KeyValuePairElementBuilder:
        builder = self._add_paragraph_and_line(
            builder=builder.with_key().with_paragraph_content(),
            polygon=self._response.polygon_of(kvp),
            content=self._build_key_content(kvp),
            confidence=kvp.confidence,
        )

        for word in kvp.key:
            builder = self._add_word_to_line(builder, word)

        return cast(KeyValuePairElementBuilder, builder)

    def _add_value(self, builder: KeyValuePairElementBuilder, value: AWSValue) -> KeyValuePairElementBuilder:
        builder = self._add_paragraph_and_line(
            builder=builder.with_value().with_paragraph_content(),
            polygon=self._response.polygon_of(value),
            content=self._content_of(value),
            confidence=value.confidence,
        )

        for word_or_checkbox in value.children:
            builder = self._add_word_or_checkbox(builder, word_or_checkbox)

        return cast(KeyValuePairElementBuilder, builder)

    @staticmethod
    def _content_of(value: AWSValue) -> str:
        if value.contains_checkbox:
            return CheckmarkValue.CHECKED if value.children[0].is_selected() else CheckmarkValue.UNCHECKED
        return value.get_text()

    @staticmethod
    def _build_key_content(kvp: AWSKeyValuePair) -> str:
        return " ".join((k.text for k in kvp.key))
