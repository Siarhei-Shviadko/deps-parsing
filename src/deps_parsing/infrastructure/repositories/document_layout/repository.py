from typing import Any, Optional

from deps_document_layout.model import (
    DocumentLayout,
    DocumentLayoutFeaturesFilter,
    IDocumentLayoutRepository,
    LayoutWishList,
    Page,
    ParsingType,
    RawInsertPagesData,
)

from deps_parsing.domain.dtos import DocumentLayoutInfo
from deps_parsing.extras.datasource import Database

from .mappers import DocumentLayoutMapper
from .query_factory import DocumentLayoutQueryFactory

__all__ = ["DocumentLayoutRepository"]


class DocumentLayoutRepository(IDocumentLayoutRepository):
    def __init__(self, database: Database) -> None:
        self._db = database
        self._query_factory = DocumentLayoutQueryFactory()

    def save(self, layout: DocumentLayout) -> None:
        layout_dict = DocumentLayoutMapper.to_dict(layout)
        self.save_raw(layout_dict)

    def save_raw(self, raw_layout: dict[str, Any]) -> None:
        with self._db.connection() as conn:
            self._save_document_layout(conn, raw_layout["document_layout"])
            self._save_pages(conn, raw_layout["pages"])

    def save_raw_pages(self, raw_pages: RawInsertPagesData) -> None:
        with self._db.connection() as conn:
            self._save_pages(conn, raw_pages)

    def save_cloned_user_defined_document_layout(self, document_layout: DocumentLayout) -> None:
        layout_dict = DocumentLayoutMapper.to_dict(document_layout)
        with self._db.connection() as conn:
            self._delete_pages(conn, document_layout, ParsingType.USER_DEFINED)
            self._save_document_layout(conn, layout_dict["document_layout"])
            self._save_pages(conn, layout_dict["pages"])

    def layout_of_id_info(self, layout_id: str, tenant_id: str) -> Optional[DocumentLayoutInfo]:
        layout_query = self._query_factory.select_document_layout_info(layout_id, tenant_id)
        pages_query = self._query_factory.select_page_count_foreach_parsing_type(layout_id, tenant_id)

        with self._db.connection() as conn:
            if not (layout_info_result := conn.execute(layout_query).first()):
                return None

            pages_count_result = conn.execute(pages_query).fetchall()

        return DocumentLayoutMapper.layout_info_from_dict(
            raw_dl=layout_info_result,
            pages_count_result=pages_count_result,
        )

    def layout_of_id_without_pages(self, layout_id: str, tenant_id: str) -> Optional[DocumentLayout]:
        query = self._query_factory.select_document_layout_info(layout_id, tenant_id)

        with self._db.connection() as conn:
            result = conn.execute(query).fetchone()

        return DocumentLayoutMapper.from_dict(result) if result else None

    def layout_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> Optional[DocumentLayout]:
        query = self._query_factory.select_document_layout_by(layout_id, tenant_id, filtering)
        with self._db.connection() as conn:
            if row := conn.execute(query).fetchone():
                return DocumentLayoutMapper.from_dict(row)

    def is_layout_exists(self, layout_id: str, tenant_id: str) -> bool:
        with self._db.connection() as conn:
            return bool(conn.execute(self._query_factory.select_document_layout_id(layout_id, tenant_id)).fetchone())

    def delete(self, document_layout: DocumentLayout) -> None:
        with self._db.connection() as conn:
            conn.execute(
                self._query_factory.delete_document_layout(
                    layout_id=document_layout.id(),
                    tenant_id=document_layout.tenant_id(),
                ),
            )

    def find_document_layout_pages_with_amount(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> tuple[list[Page], int]:
        with self._db.connection() as conn:
            rows = conn.execute(
                self._query_factory.select_document_layout_by(
                    layout_id=document_layout_id,
                    tenant_id=tenant_id,
                    filtering=filtering,
                ),
            ).fetchone()

            row = conn.execute(
                self._query_factory.select_page_count_by_filtering(
                    layout_id=document_layout_id,
                    tenant_id=tenant_id,
                    filtering=filtering,
                ),
            ).fetchone()

        return (
            DocumentLayoutMapper.from_dict(rows).pages if rows else [],
            row.page_amount,
        )

    def partial_layout_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        wish_list: LayoutWishList,
    ) -> Optional[DocumentLayout]:
        with self._db.connection() as conn:
            row = conn.execute(
                self._query_factory.select_partial_document_layout_by(
                    layout_id=layout_id,
                    tenant_id=tenant_id,
                    wish_list=wish_list,
                ),
            ).fetchone()

        if row:
            return DocumentLayoutMapper.from_dict(row)

        return None

    def _save_document_layout(self, conn, raw_data: dict[str, str]) -> None:
        conn.execute(self._query_factory.insert_document_layout(), raw_data)

    def _save_pages(self, conn, raw_data: RawInsertPagesData) -> None:
        if not raw_data:
            return

        if pages := raw_data["pages"]:
            conn.execute(self._query_factory.insert_pages(), pages)
        if images := raw_data["images"]:
            conn.execute(self._query_factory.insert_images(), images)
        if tables := raw_data["tables"]:
            conn.execute(self._query_factory.insert_tables(), tables)
        if paragraphs := raw_data["paragraphs"]:
            conn.execute(self._query_factory.insert_paragraphs(), paragraphs)
        if key_value_pairs := raw_data["key_value_pairs"]:
            conn.execute(self._query_factory.insert_key_value_pairs(), key_value_pairs)

    def _delete_pages(self, conn, document_layout: DocumentLayout, parsing_type: ParsingType) -> None:
        conn.execute(
            self._query_factory.delete_pages_by_parsing_type(
                layout=document_layout,
                parsing_type=parsing_type,
            ),
        )
