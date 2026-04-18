from deps_document_layout.model import PageBuilder

from deps_parsing.domain.model import CheckmarkValue

from .structured_response import StructuredResponse
from .types import DocAIKeyValuePair

__all__ = ["KeyValuePairsParser"]


def _avg(*values: float) -> float:
    return sum(values) / len(values) if values else 0.0


_document_ai_checkmark_to_internal: dict[str, CheckmarkValue] = {
    "filled_checkbox": CheckmarkValue.CHECKED,
    "unfilled_checkbox": CheckmarkValue.UNCHECKED,
}


class KeyValuePairsParser:
    def __init__(self, response: StructuredResponse) -> None:
        self._response = response

    def add_key_value_pairs_to(self, builder: PageBuilder) -> PageBuilder:
        for key_value_pair in self._response.key_value_pairs:
            field_confidence = _avg(key_value_pair.field_name.confidence, key_value_pair.field_value.confidence)

            builder = (
                builder.with_key_value_pair()
                .with_confidence(field_confidence)
                .with_key()
                .with_content(self._response.get_text_of(key_value_pair.field_name))
                .with_polygon(self._response.get_polygon_of(key_value_pair.field_name))
                .with_value()
                .with_content(self._handle_form_value(key_value_pair))
                .with_polygon(self._response.get_polygon_of(key_value_pair.field_value))
            )

        return builder

    def _handle_form_value(self, key_value_pair: DocAIKeyValuePair) -> str:
        if key_value_pair.value_type in _document_ai_checkmark_to_internal:
            return _document_ai_checkmark_to_internal[key_value_pair.value_type]

        return self._response.get_text_of(key_value_pair.field_value)
