import logging
from typing import Any, cast

from deps_document_layout.model import PageBuilder, ParagraphBuilder

from .base_page_element import PageElementParser

__all__ = ["GenericTextDataParser"]

_logger = logging.getLogger(__name__)


class GenericTextDataParser(PageElementParser):
    def add_element(self, builder: ParagraphBuilder, page_element: Any) -> PageBuilder:
        try:
            builder = (
                builder.with_line()
                .with_confidence(page_element.confidence)
                .with_content(page_element.text)
                .with_polygon(self._response.polygon_of(page_element))
            )
        except Exception as ex:
            _logger.warning(f"Failed to add generic text element: `{ex}`. Element: `{page_element}`")
            return cast(PageBuilder, builder)

        return cast(PageBuilder, builder)
