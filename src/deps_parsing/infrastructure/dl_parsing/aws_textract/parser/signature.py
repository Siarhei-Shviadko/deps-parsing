from typing import cast

from deps_document_layout.model import PageBuilder, ParagraphBuilder

from .base_page_element import PageElementParser
from .types import AWSSignature

__all__ = ["SignatureDataParser"]


class SignatureDataParser(PageElementParser):
    def add_element(self, builder: ParagraphBuilder, signature: AWSSignature) -> PageBuilder:
        signature_polygon = self._response.polygon_of(signature)

        builder = (
            builder.with_line()
            .with_content(signature.text)
            .with_polygon(signature_polygon)
            .with_confidence(signature.confidence)
        )

        builder = (
            builder.with_signature()
            .with_value(signature.text)
            .with_confidence(signature.confidence)
            .with_polygon(signature_polygon)
        )

        return cast(PageBuilder, builder)
