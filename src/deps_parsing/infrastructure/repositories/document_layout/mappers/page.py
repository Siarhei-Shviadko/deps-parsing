from deps_document_layout.model import (
    Dimension,
    EntityId,
    Image,
    Language,
    Page,
    ParsingType,
    RawDimension,
    RawImage,
    RawInsertPagesData,
    RawKeyValuePair,
    RawLanguage,
    RawPageFromDB,
    RawPageToDB,
    RawParagraph,
    RawTable,
)

from .group import GroupMapper
from .key_value_pair import KeyValuePairMapper
from .paragraph import ParagraphMapper
from .polygon import PolygonMapper
from .table import TableMapper
from .transformation import TransformationsMapper

__all__ = ["PageMapper"]


class PageMapper:
    @classmethod
    def to_dict(cls, document_layout_id: str, pages: list[Page]) -> RawInsertPagesData:
        raw_pages: list[RawPageToDB] = []
        raw_images: list[RawImage] = []
        raw_paragraphs: list[RawParagraph] = []
        raw_key_value_pairs: list[RawKeyValuePair] = []
        raw_tables: list[RawTable] = []

        for page in pages:
            page_id = page.id()
            parsing_type = page.parsing_type
            raw_pages.append(
                RawPageToDB(
                    id=page_id,
                    page_number=page.page_number,
                    parsing_type=parsing_type,
                    dimension=cls._dimension_to_dict(page.dimension),
                    languages=[cls._language_to_dict(languages) for languages in page.languages],
                    file_path=page.file_path,
                    transformations=TransformationsMapper.to_dict(page.transformations),
                    document_layout_id=document_layout_id,
                    groups=[GroupMapper.to_dict(group) for group in page.groups],
                ),
            )
            raw_images.extend(cls._image_to_dict(image, page_id, parsing_type) for image in page.images)
            raw_paragraphs.extend(
                ParagraphMapper.to_dict(paragraph, page_id, parsing_type) for paragraph in page.paragraphs
            )
            raw_key_value_pairs.extend(
                KeyValuePairMapper.to_dict(key_value_pair, page_id, parsing_type)
                for key_value_pair in page.key_value_pairs
            )
            raw_tables.extend(TableMapper.to_dict(table, page_id, parsing_type) for table in page.tables)

        return RawInsertPagesData(
            pages=raw_pages,
            images=raw_images,
            paragraphs=raw_paragraphs,
            key_value_pairs=raw_key_value_pairs,
            tables=raw_tables,
        )

    @classmethod
    def from_dict(cls, raw_page: RawPageFromDB) -> Page:
        return Page(
            id_=EntityId(raw_page["id"]),
            page_number=raw_page["page_number"],
            parsing_type=ParsingType(raw_page["parsing_type"]),
            dimension=cls._dimension_from_dict(raw_page["dimension"]),
            languages=tuple(cls._language_from_dict(language) for language in raw_page["languages"])
            if "languages" in raw_page and raw_page["languages"] is not None
            else None,
            file_path=raw_page["file_path"],
            transformations=TransformationsMapper.from_dict(raw_page["transformations"]),
            images=tuple(cls._image_from_dict(image) for image in raw_page["images"]) if "images" in raw_page else None,
            key_value_pairs=tuple(KeyValuePairMapper.from_dict(kv_pair) for kv_pair in raw_page["key_value_pairs"]),
            tables=tuple(TableMapper.from_dict(table) for table in raw_page["tables"]),
            paragraphs=tuple(ParagraphMapper.from_dict(paragraph) for paragraph in raw_page["paragraphs"]),
            groups=tuple(GroupMapper.from_dict(group) for group in raw_page["groups"]),
        )

    @classmethod
    def _dimension_to_dict(cls, dimension: Dimension) -> RawDimension:
        return {
            "width": dimension.width,
            "height": dimension.height,
            "unit": dimension.unit,
        }

    @classmethod
    def _dimension_from_dict(cls, dimension: RawDimension) -> Dimension:
        return Dimension(
            width=dimension["width"],
            height=dimension["height"],
            unit=dimension["unit"],
        )

    @classmethod
    def _language_to_dict(cls, language: Language) -> RawLanguage:
        return {
            "language_code": language.language_code,
            "confidence": language.confidence,
        }

    @classmethod
    def _language_from_dict(cls, language: RawLanguage) -> Language:
        return Language(language_code=language["language_code"], confidence=language["confidence"])

    @classmethod
    def _image_to_dict(cls, image: Image, page_id: str, parsing_type: ParsingType) -> RawImage:
        return {
            "id": image.id(),
            "order_num": image.order,
            "title": image.title,
            "file_path": image.file_path,
            "polygon": PolygonMapper.to_dict(image.polygon),
            "description": image.description,
            "page_id": page_id,
            "parsing_type": parsing_type,
        }

    @classmethod
    def _image_from_dict(cls, image: RawImage) -> Image:
        return Image(
            id_=EntityId(image["id"]),
            order=image["order_num"],
            title=image["title"],
            file_path=image["file_path"],
            polygon=PolygonMapper.from_dict(image["polygon"]),
            description=image.get("description"),
        )
