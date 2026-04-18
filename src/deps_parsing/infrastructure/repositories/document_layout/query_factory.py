from deps_document_layout.model import (
    DocumentLayout,
    DocumentLayoutFeaturesFilter,
    LayoutWishList,
    PageBatch,
    ParsingFeature,
    ParsingType,
)
from sqlalchemy import Column, and_, delete, func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.sql import Delete, FromClause, Insert, Join, Select
from sqlalchemy.sql.selectable import CTE

from ..tables import (
    document_layout_table,
    image_table,
    key_value_pair_table,
    page_table,
    paragraph_table,
    table_table,
)

__all__ = ["DocumentLayoutQueryFactory"]


class DocumentLayoutQueryFactory:
    def __init__(self) -> None:
        self._page_schema = page_table
        self._image_schema = image_table
        self._key_value_pair_schema = key_value_pair_table
        self._paragraph_schema = paragraph_table
        self._table_schema = table_table
        self._document_layout_schema = document_layout_table

        self._feature_table_map = {
            ParsingFeature.TEXT: self._paragraph_schema,
            ParsingFeature.IMAGES: self._image_schema,
            ParsingFeature.TABLES: self._table_schema,
            ParsingFeature.KEY_VALUE_PAIRS: self._key_value_pair_schema,
        }

    @property
    def document_layout_columns(self) -> list[Column]:
        return [
            self._document_layout_schema.c.id,
            self._document_layout_schema.c.tenant_id,
            self._document_layout_schema.c.parsing_features,
            func.coalesce(self._document_layout_schema.c.merged_tables, text("'{}'::jsonb")).label(  # noqa: P103
                "merged_tables",
            ),
        ]

    @property
    def page_columns(self) -> list[Column]:
        return [
            self._page_schema.c.id,
            self._page_schema.c.page_number,
            self._page_schema.c.parsing_type,
            self._page_schema.c.dimension,
            self._page_schema.c.languages,
            self._page_schema.c.file_path,
            self._page_schema.c.transformations,
            self._page_schema.c.groups,
        ]

    def select_document_layout_info(self, layout_id: str, tenant_id: str) -> Select:
        return select(self.document_layout_columns).where(
            and_(
                self._document_layout_schema.c.id == layout_id,
                self._document_layout_schema.c.tenant_id == tenant_id,
            ),
        )

    def insert_images(self) -> Insert:
        query = pg_insert(self._image_schema)
        return query.on_conflict_do_update(
            constraint="image_pk",
            set_=dict(query.excluded),
        )

    def insert_key_value_pairs(self) -> Insert:
        query = pg_insert(self._key_value_pair_schema)
        return query.on_conflict_do_update(
            constraint="key_value_pair_pk",
            set_=dict(query.excluded),
        )

    def insert_paragraphs(self) -> Insert:
        query = pg_insert(self._paragraph_schema)
        return query.on_conflict_do_update(
            constraint="paragraph_pk",
            set_=dict(query.excluded),
        )

    def insert_tables(self) -> Insert:
        query = pg_insert(self._table_schema)
        return query.on_conflict_do_update(
            constraint="table_pk",
            set_=dict(query.excluded),
        )

    def insert_pages(self) -> Insert:
        query = pg_insert(self._page_schema)
        return query.on_conflict_do_update(
            constraint="unique__document_layout_id__page_number__parsing_type",
            set_=dict(query.excluded),
        )

    def insert_document_layout(self) -> Insert:
        query = pg_insert(self._document_layout_schema)
        return query.on_conflict_do_update(
            constraint="document_layout_id__tenant_id__pk",
            set_={
                "parsing_features": query.excluded.parsing_features,
                "merged_tables": query.excluded.merged_tables,
            },
        ).on_conflict_do_update(
            constraint="document_layout_id_key",
            set_={
                "parsing_features": query.excluded.parsing_features,
                "merged_tables": query.excluded.merged_tables,
            },
        )

    def select_document_layout_id(self, layout_id: str, tenant_id: str) -> Select:
        query = select([self._document_layout_schema.c.id])
        return query.where(
            and_(self._document_layout_schema.c.id == layout_id, self._document_layout_schema.c.tenant_id == tenant_id),
        )

    def delete_document_layout(self, layout_id: str, tenant_id: str) -> Delete:
        return delete(self._document_layout_schema).where(
            and_(
                self._document_layout_schema.c.id == layout_id,
                self._document_layout_schema.c.tenant_id == tenant_id,
            ),
        )

    def delete_pages_by_parsing_type(self, layout: DocumentLayout, parsing_type: ParsingType) -> Delete:
        return delete(self._page_schema).where(
            and_(
                self._page_schema.c.document_layout_id == layout.id(),
                self._page_schema.c.parsing_type == parsing_type,
            ),
        )

    def select_page_count_by_filtering(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> Select:
        return (
            select([func.count(self._page_schema.c.id).label("page_amount")])
            .select_from(self._base_join(filtering.parsing_type))
            .where(
                and_(
                    self._document_layout_schema.c.id == layout_id,
                    self._document_layout_schema.c.tenant_id == tenant_id,
                ),
            )
        )

    def select_page_count_foreach_parsing_type(
        self,
        layout_id: str,
        tenant_id: str,
    ) -> Select:
        layout_with_page = self._page_schema.join(
            self._document_layout_schema,
            self._page_schema.c.document_layout_id == self._document_layout_schema.c.id,
        )

        return (
            select(
                [
                    self._page_schema.c.parsing_type,
                    func.count(self._page_schema.c.id).label("page_amount"),
                ],
            )
            .select_from(layout_with_page)
            .where(
                and_(
                    self._document_layout_schema.c.id == layout_id,
                    self._document_layout_schema.c.tenant_id == tenant_id,
                ),
            )
            .group_by(self._page_schema.c.parsing_type)
        )

    def select_partial_document_layout_by(
        self,
        layout_id: str,
        tenant_id: str,
        wish_list: LayoutWishList,
    ) -> Select:
        pages_base = self._build_pages_query_for_partial_dl(layout_id=layout_id, wish_list=wish_list)
        pages_with_content = self._build_pages_with_content_query(
            pages_base=pages_base,
            images_by_page=self._build_images_by_wish_list_query(pages_base=pages_base, wish_list=wish_list),
            tables_by_page=self._build_tables_by_wish_list_query(pages_base=pages_base, wish_list=wish_list),
            key_value_pairs_by_page=self._build_key_value_pairs_by_wish_list_query(
                pages_base=pages_base,
                wish_list=wish_list,
            ),
            paragraph_by_page=self._build_paragraphs_by_wish_list_query(pages_base=pages_base, wish_list=wish_list),
            features=wish_list.features,
        )

        return self._build_final_document_layout_query(
            layout_id=layout_id,
            tenant_id=tenant_id,
            pages_with_content=pages_with_content,
            parsing_type=wish_list.parsing_type,
        )

    def select_document_layout_by(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> Select:
        pages_base = self._build_pages_base_query(
            layout_id=layout_id,
            parsing_type=filtering.parsing_type,
            page_batch=filtering.page_batch,
        )
        pages_with_content = self._build_pages_with_content_query(
            pages_base=pages_base,
            images_by_page=self._build_images_by_page_query(pages_base),
            tables_by_page=self._build_tables_by_page_query(pages_base),
            paragraph_by_page=self._build_paragraphs_by_page_query(pages_base),
            key_value_pairs_by_page=self._build_key_value_pairs_by_page_query(pages_base),
            features=filtering.features,
        )

        return self._build_final_document_layout_query(
            layout_id=layout_id,
            tenant_id=tenant_id,
            pages_with_content=pages_with_content,
            parsing_type=filtering.parsing_type,
        )

    def _base_join(self, parsing_type: ParsingType) -> Join:
        return self._document_layout_schema.outerjoin(
            page_table,
            and_(
                page_table.c.document_layout_id == document_layout_table.c.id,
                page_table.c.parsing_type == parsing_type,
            ),
        )

    def _build_pages_base_query(self, layout_id: str, parsing_type: ParsingType, page_batch: PageBatch | None) -> CTE:
        query = (
            select([self._page_schema])
            .where(
                and_(
                    self._page_schema.c.document_layout_id == layout_id,
                    self._page_schema.c.parsing_type == parsing_type,
                ),
            )
            .order_by(self._page_schema.c.page_number)
        )

        if page_batch is not None:
            query = query.offset(page_batch.index * page_batch.size)
            query = query.limit(page_batch.size)

        return query.cte("pages_base")

    def _build_pages_query_for_partial_dl(self, layout_id: str, wish_list: LayoutWishList) -> CTE:
        query = (
            select([self._page_schema])
            .where(
                and_(
                    self._page_schema.c.document_layout_id == layout_id,
                    self._page_schema.c.parsing_type == wish_list.parsing_type,
                ),
            )
            .order_by(self._page_schema.c.page_number)
        )

        if page_ids := wish_list.page_ids:
            query = query.where(self._page_schema.c.id.in_(page_ids))

        return query.cte("pages_base")

    def _images_by_page_query(self, pages_base: CTE) -> Select:
        return (
            select(
                [
                    self._image_schema.c.page_id,
                    self._image_schema.c.parsing_type,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            self._image_schema.c.id,
                            "order_num",
                            self._image_schema.c.order_num,
                            "title",
                            self._image_schema.c.title,
                            "file_path",
                            self._image_schema.c.file_path,
                            "polygon",
                            self._image_schema.c.polygon,
                            "description",
                            self._image_schema.c.description,
                        ),
                    ).label("images"),
                ],
            )
            .where(self._image_schema.c.page_id.in_(select([pages_base.c.id])))
            .group_by(self._image_schema.c.page_id, self._image_schema.c.parsing_type)
        )

    def _build_images_by_page_query(self, pages_base: CTE) -> CTE:
        return self._images_by_page_query(pages_base).cte("images_by_page")

    def _build_images_by_wish_list_query(self, pages_base: CTE, wish_list: LayoutWishList) -> CTE:
        query = self._images_by_page_query(pages_base)

        if image_ids := wish_list.image_ids:
            query = query.where(self._image_schema.c.id.in_(image_ids))

        return query.cte("images_by_page")

    def _tables_by_page_query(self, pages_base: CTE) -> Select:
        return (
            select(
                [
                    self._table_schema.c.page_id,
                    self._table_schema.c.parsing_type,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            self._table_schema.c.id,
                            "order_num",
                            self._table_schema.c.order_num,
                            "column_count",
                            self._table_schema.c.column_count,
                            "row_count",
                            self._table_schema.c.row_count,
                            "polygon",
                            self._table_schema.c.polygon,
                            "confidence",
                            self._table_schema.c.confidence,
                            "cells",
                            self._table_schema.c.cells,
                        ),
                    ).label("tables"),
                ],
            )
            .where(self._table_schema.c.page_id.in_(select([pages_base.c.id])))
            .group_by(self._table_schema.c.page_id, self._table_schema.c.parsing_type)
        )

    def _build_tables_by_page_query(self, pages_base: CTE) -> CTE:
        query = self._tables_by_page_query(pages_base)

        return query.cte("tables_by_page")

    def _build_tables_by_wish_list_query(self, pages_base: CTE, wish_list: LayoutWishList) -> CTE:
        query = self._tables_by_page_query(pages_base)

        if table_ids := wish_list.table_ids:
            query = query.where(self._table_schema.c.id.in_(table_ids))

        return query.cte("tables_by_page")

    def _paragraphs_by_page_query(self, pages_base: CTE) -> Select:
        return (
            select(
                [
                    self._paragraph_schema.c.page_id,
                    self._paragraph_schema.c.parsing_type,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            self._paragraph_schema.c.id,
                            "order_num",
                            self._paragraph_schema.c.order_num,
                            "content",
                            self._paragraph_schema.c.content,
                            "confidence",
                            self._paragraph_schema.c.confidence,
                            "role",
                            self._paragraph_schema.c.role,
                            "polygon",
                            self._paragraph_schema.c.polygon,
                            "lines",
                            self._paragraph_schema.c.lines,
                        ),
                    ).label("paragraphs"),
                ],
            )
            .where(self._paragraph_schema.c.page_id.in_(select([pages_base.c.id])))
            .group_by(self._paragraph_schema.c.page_id, self._paragraph_schema.c.parsing_type)
        )

    def _build_paragraphs_by_page_query(self, pages_base: CTE) -> CTE:
        return self._paragraphs_by_page_query(pages_base).cte("paragraphs_by_page")

    def _build_paragraphs_by_wish_list_query(self, pages_base: CTE, wish_list: LayoutWishList) -> CTE:
        query = self._paragraphs_by_page_query(pages_base)

        if (paragraph_ids := wish_list.paragraph_ids) and not wish_list.has_features_requiring_paragraphs():
            query = query.where(self._paragraph_schema.c.id.in_(paragraph_ids))

        return query.cte("paragraphs_by_page")

    def _key_value_pairs_by_page_query(self, pages_base: CTE) -> Select:
        return (
            select(
                [
                    self._key_value_pair_schema.c.page_id,
                    self._key_value_pair_schema.c.parsing_type,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            self._key_value_pair_schema.c.id,
                            "order_num",
                            self._key_value_pair_schema.c.order_num,
                            "key",
                            self._key_value_pair_schema.c.key,
                            "value",
                            self._key_value_pair_schema.c.value,
                            "confidence",
                            self._key_value_pair_schema.c.confidence,
                        ),
                    ).label("key_value_pairs"),
                ],
            )
            .where(self._key_value_pair_schema.c.page_id.in_(select([pages_base.c.id])))
            .group_by(self._key_value_pair_schema.c.page_id, self._key_value_pair_schema.c.parsing_type)
        )

    def _build_key_value_pairs_by_page_query(self, pages_base: CTE) -> CTE:
        return self._key_value_pairs_by_page_query(pages_base).cte("key_value_pairs_by_page")

    def _build_key_value_pairs_by_wish_list_query(self, pages_base: CTE, wish_list: LayoutWishList) -> CTE:
        query = self._key_value_pairs_by_page_query(pages_base)

        if key_value_pairs_ids := wish_list.key_value_pairs_ids:
            query = query.where(self._key_value_pair_schema.c.id.in_(key_value_pairs_ids))

        return query.cte("key_value_pairs_by_page")

    def _build_pages_with_content_query(
        self,
        pages_base: CTE,
        images_by_page: CTE,
        tables_by_page: CTE,
        paragraph_by_page: CTE,
        key_value_pairs_by_page: CTE,
        features: set[ParsingFeature],
    ) -> CTE:
        return (
            select(
                [
                    pages_base.c.document_layout_id,
                    pages_base.c.parsing_type,
                    func.jsonb_agg(
                        func.jsonb_build_object(
                            "id",
                            pages_base.c.id,
                            "page_number",
                            pages_base.c.page_number,
                            "parsing_type",
                            pages_base.c.parsing_type,
                            "dimension",
                            pages_base.c.dimension,
                            "languages",
                            pages_base.c.languages,
                            "file_path",
                            pages_base.c.file_path,
                            "transformations",
                            pages_base.c.transformations,
                            "groups",
                            pages_base.c.groups,
                            "images",
                            (
                                func.coalesce(images_by_page.c.images, "[]")
                                if ParsingFeature.IMAGES in features
                                else func.jsonb_build_array()
                            ),
                            "tables",
                            (
                                func.coalesce(tables_by_page.c.tables, "[]")
                                if ParsingFeature.TABLES in features
                                else func.jsonb_build_array()
                            ),
                            "paragraphs",
                            (
                                func.coalesce(paragraph_by_page.c.paragraphs, "[]")
                                if ParsingFeature.TEXT in features
                                else func.jsonb_build_array()
                            ),
                            "key_value_pairs",
                            (
                                func.coalesce(key_value_pairs_by_page.c.key_value_pairs, "[]")
                                if ParsingFeature.KEY_VALUE_PAIRS in features
                                else func.jsonb_build_array()
                            ),
                        ),
                    ).label("pages"),
                ],
            )
            .select_from(
                self._join_content_tables(
                    pages_base=pages_base,
                    images_by_page=images_by_page,
                    tables_by_page=tables_by_page,
                    paragraph_by_page=paragraph_by_page,
                    key_value_pairs_by_page=key_value_pairs_by_page,
                    features=features,
                ),
            )
            .group_by(pages_base.c.document_layout_id, pages_base.c.parsing_type)
            .cte("pages_with_content")
        )

    @staticmethod
    def _join_content_tables(
        pages_base: CTE,
        images_by_page: CTE,
        tables_by_page: CTE,
        paragraph_by_page: CTE,
        key_value_pairs_by_page: CTE,
        features: set[ParsingFeature],
    ) -> FromClause:
        joined_tables = pages_base
        feature_table_mapping = {
            ParsingFeature.IMAGES: images_by_page,
            ParsingFeature.TABLES: tables_by_page,
            ParsingFeature.TEXT: paragraph_by_page,
            ParsingFeature.KEY_VALUE_PAIRS: key_value_pairs_by_page,
        }

        for feature in features:
            table_to_join = feature_table_mapping[feature]

            joined_tables = joined_tables.outerjoin(
                table_to_join,
                and_(
                    pages_base.c.id == table_to_join.c.page_id,
                    pages_base.c.parsing_type == table_to_join.c.parsing_type,
                ),
            )

        return joined_tables

    def _build_final_document_layout_query(
        self,
        layout_id: str,
        tenant_id: str,
        pages_with_content: CTE,
        parsing_type: ParsingType,
    ) -> Select:
        return (
            select([*self.document_layout_columns, func.coalesce(pages_with_content.c.pages, "[]").label("pages")])
            .select_from(
                self._document_layout_schema.outerjoin(
                    pages_with_content,
                    and_(
                        pages_with_content.c.document_layout_id == self._document_layout_schema.c.id,
                        pages_with_content.c.parsing_type == parsing_type,
                    ),
                ),
            )
            .where(
                and_(
                    self._document_layout_schema.c.id == layout_id,
                    self._document_layout_schema.c.tenant_id == tenant_id,
                ),
            )
        )
