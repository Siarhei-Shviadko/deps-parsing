from deps_document_layout.model import (
    EntityId,
    Image,
    KeyValuePair,
    LayoutWishList,
    Page,
    Paragraph,
    ParsingFeature,
    ParsingType,
    Table,
)

__all__ = ["PagesByWishListGatherer"]


class PagesByWishListGatherer:
    def __init__(self, pages: list[Page], wish_list: LayoutWishList) -> None:
        self._pages: dict[tuple[str, ParsingType], Page] = {}
        self._images: dict[tuple[str, ParsingType], Image] = {}
        self._paragraphs: dict[tuple[str, ParsingType], Paragraph] = {}
        self._tables: dict[tuple[str, ParsingType], Table] = {}
        self._kvps: dict[tuple[str, ParsingType], KeyValuePair] = {}
        self._wish_list = wish_list

        for page in pages:
            page_parsing_type = page.parsing_type
            self._pages[(page.id(), page_parsing_type)] = page
            self._images.update({(i.id(), page_parsing_type): i for i in page.images})
            self._paragraphs.update({(p.id(), page_parsing_type): p for p in page.paragraphs})
            self._tables.update({(t.id(), page_parsing_type): t for t in page.tables})
            self._kvps.update({(kvp.id(), page_parsing_type): kvp for kvp in page.key_value_pairs})

    @property
    def _parsing_type(self) -> ParsingType:
        return self._wish_list.parsing_type

    def gather(self) -> list[Page]:
        pages: list[Page] = []

        for page_wish_list in self._wish_list.pages or []:
            page_id = page_wish_list.page_id
            if page := self._pages.get((page_id, self._parsing_type)):
                pages.append(
                    Page(
                        id_=EntityId(page_id),
                        page_number=page.page_number,
                        parsing_type=page.parsing_type,
                        dimension=page.dimension,
                        languages=page.languages,
                        file_path=page.file_path,
                        transformations=page.transformations,
                        groups=page.groups,
                        images=(
                            page.images if (images := self._gather_images(page_wish_list.image_ids)) is None else images
                        ),
                        paragraphs=(
                            page.paragraphs
                            if (paragraphs := self._gather_paragraphs(page_wish_list.paragraph_ids)) is None
                            else paragraphs
                        ),
                        tables=(
                            page.tables if (tables := self._gather_tables(page_wish_list.table_ids)) is None else tables
                        ),
                        key_value_pairs=(
                            page.key_value_pairs
                            if (kvps := self._gather_kvps(page_wish_list.key_value_pair_ids)) is None
                            else kvps
                        ),
                    ),
                )

        return pages

    def _gather_images(self, image_ids: list[str] | None) -> tuple[Image, ...] | None:
        if ParsingFeature.IMAGES in self._wish_list.features:
            if image_ids:
                return tuple(self._images[(id_, self._parsing_type)] for id_ in image_ids)

            return None

        return tuple()

    def _gather_tables(self, table_ids: list[str] | None) -> tuple[Table, ...] | None:
        if ParsingFeature.TABLES in self._wish_list.features:
            if table_ids:
                return tuple(self._tables[(id_, self._parsing_type)] for id_ in table_ids)

            return None

        return tuple()

    def _gather_kvps(self, kvp_ids: list[str] | None) -> tuple[KeyValuePair, ...] | None:
        if ParsingFeature.KEY_VALUE_PAIRS in self._wish_list.features:
            if kvp_ids:
                return tuple(self._kvps[(id_, self._parsing_type)] for id_ in kvp_ids)

            return None

        return tuple()

    def _gather_paragraphs(self, paragraph_ids: list[str] | None) -> tuple[Paragraph, ...] | None:
        if ParsingFeature.TEXT in self._wish_list.features:
            if paragraph_ids and not self._wish_list.has_features_requiring_paragraphs():
                return tuple(self._paragraphs[(id_, self._parsing_type)] for id_ in paragraph_ids or [])

            return None

        return tuple()
