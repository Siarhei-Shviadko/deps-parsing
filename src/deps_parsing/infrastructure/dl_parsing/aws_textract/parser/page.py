from deps_document_layout.model import DocumentLayout, PageBuilder, ParsingType

from .structured_response import StructuredResponse

__all__ = ["PageDataParser"]


class PageDataParser:
    def __init__(self, response: StructuredResponse):
        self._response = response

    def add_page_data(self, document_layout: DocumentLayout) -> PageBuilder:
        builder = (
            document_layout.add_page()
            .with_id(self._response.page_id)
            .with_page_number(self._response.page_number)
            .with_parsing_type(ParsingType.AWS_TEXTRACT)
            .with_dimension(width=self._response.page_width, height=self._response.page_height, unit="px")
            .with_file_path(self._response.file_path)
            .with_transformations()
            .with_angle(0.0)  # noqa:WPS358
        )

        return (
            builder.with_language(language_code=self._response.language, confidence=1.0)
            if self._response.language
            else builder
        )
