from deps_document_layout.model import (
    RawImage,
    RawInsertPagesData,
    RawKeyValuePair,
    RawPageToDB,
    RawParagraph,
    RawTable,
)
from deps_document_layout.serializers.document_layout import SerializedPage

from .base import ConfiguredBaseModel

__all__ = ["GetDocumentLayoutPagesResponse", "SaveDocumentLayoutPagesRequest"]


class GetDocumentLayoutPagesResponse(ConfiguredBaseModel):
    total: int
    pages: list[SerializedPage]


class SaveDocumentLayoutPagesRequest(ConfiguredBaseModel):
    pages: list[SerializedPage]

    def to_dict(self, document_layout_id: str) -> RawInsertPagesData:
        raw_pages: list[RawPageToDB] = []
        raw_images: list[RawImage] = []
        raw_paragraphs: list[RawParagraph] = []
        raw_key_value_pairs: list[RawKeyValuePair] = []
        raw_tables: list[RawTable] = []

        for page in self.pages:
            page_id = page.id
            parsing_type = page.parsing_type
            raw_pages.append(
                RawPageToDB(
                    id=page_id,
                    page_number=page.page_number,
                    parsing_type=parsing_type,
                    dimension=page.dimension.to_dict(),
                    languages=[languages.to_dict() for languages in page.languages],
                    file_path=page.file_path,
                    transformations=page.transformations.to_dict(),
                    document_layout_id=document_layout_id,
                    groups=[group.to_dict() for group in page.groups],
                ),
            )
            raw_images.extend(image.to_dict(page_id=page_id, parsing_type=parsing_type) for image in page.images)
            raw_paragraphs.extend(
                paragraph.to_dict(page_id=page_id, parsing_type=parsing_type) for paragraph in page.paragraphs
            )
            raw_key_value_pairs.extend(
                kvp.to_dict(page_id=page_id, parsing_type=parsing_type) for kvp in page.key_value_pairs
            )
            raw_tables.extend(table.to_dict(page_id=page_id, parsing_type=parsing_type) for table in page.tables)

        return RawInsertPagesData(
            pages=raw_pages,
            images=raw_images,
            paragraphs=raw_paragraphs,
            key_value_pairs=raw_key_value_pairs,
            tables=raw_tables,
        )
