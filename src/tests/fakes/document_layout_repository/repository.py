from copy import deepcopy
from typing import Optional

from deps_document_layout.model import (
    DocumentLayout,
    DocumentLayoutFeaturesFilter,
    IDocumentLayoutRepository,
    LayoutWishList,
    Page,
    PageBatch,
    ParsingType,
    RawInsertPagesData,
)

from deps_parsing.domain.dtos import DocumentLayoutInfo, PageInfo

from .pages_by_wish_list_gatherer import PagesByWishListGatherer
from .raw_insert_pages_data_mapper import RawInsertPagesDataMapper

__all__ = ["FakeDocumentLayoutRepository"]


FIRST_ELEMENT = 0


class FakeDocumentLayoutRepository(IDocumentLayoutRepository):
    def __init__(self) -> None:
        self._db: dict[tuple[str, str], DocumentLayout] = {}

    def save(self, layout: DocumentLayout) -> None:
        layout = deepcopy(layout)
        layout.events.clear()
        self._db[layout.id(), layout.tenant_id()] = layout

    def save_raw_pages(self, raw_pages: RawInsertPagesData) -> None:
        layout = None
        document_layout_id = raw_pages["pages"][FIRST_ELEMENT]["document_layout_id"]
        for key, dl in self._db.items():
            if document_layout_id in key:
                layout = dl
                break

        if layout:
            for page in RawInsertPagesDataMapper(raw_pages).to_models():
                self._add_page_to_layout(page, layout=layout)
        else:
            raise RuntimeError(f"Document layout `{document_layout_id}` existence violation.")

    def save_cloned_user_defined_document_layout(self, document_layout: DocumentLayout) -> None:
        layout_key = (document_layout.id(), document_layout.tenant_id())
        existing_layout = self._db.get(layout_key)

        if existing_layout:
            remaining_pages = [page for page in existing_layout.pages if page.parsing_type != ParsingType.USER_DEFINED]

            user_defined_pages = [
                page for page in document_layout.pages if page.parsing_type == ParsingType.USER_DEFINED
            ]

            existing_layout.pages.clear()
            existing_layout.pages.extend(remaining_pages + user_defined_pages)

            existing_layout.parsing_features.clear()
            existing_layout.parsing_features.update(document_layout.parsing_features)

            self.save(existing_layout)
        else:
            self.save(document_layout)

    def layout_of_id_info(self, layout_id: str, tenant_id: str) -> Optional[DocumentLayoutInfo]:
        if layout := deepcopy(self._db.get((layout_id, tenant_id))):
            unique_parsing_types = set(page.parsing_type for page in layout.pages)
            pages_info = {
                parsing_type: PageInfo(pages_count=sum(1 for page in layout.pages if page.parsing_type == parsing_type))
                for parsing_type in unique_parsing_types
            }

            return DocumentLayoutInfo(
                id=layout.id(),
                parsing_features=layout.parsing_features,
                merged_tables=layout.merged_tables,
                pages_info=pages_info,
            )

        return None

    def layout_of_id_without_pages(self, layout_id: str, tenant_id: str) -> Optional[DocumentLayout]:
        if layout := deepcopy(self._db.get((layout_id, tenant_id))):
            layout.clear()

        return layout

    def layout_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> Optional[DocumentLayout]:
        if layout := deepcopy(self._db.get((layout_id, tenant_id))):
            return self._apply_filtering(layout, filtering)

        return layout

    def delete(self, layout: DocumentLayout) -> None:
        del self._db[layout.id(), layout.tenant_id()]

    def is_layout_exists(self, layout_id: str, tenant_id: str) -> bool:
        return bool(self._db.get((layout_id, tenant_id)))

    def find_document_layout_pages_with_amount(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> tuple[list[Page], int]:
        default_amount = 0
        layout = self.layout_of_id(layout_id=document_layout_id, tenant_id=tenant_id, filtering=filtering)
        pages = self._batch_pages(layout.pages, filtering.page_batch) if layout else []
        page_amount = len(layout.pages) if layout else default_amount

        return pages, page_amount

    def partial_layout_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        wish_list: LayoutWishList,
    ) -> Optional[DocumentLayout]:
        if layout := deepcopy(self._db.get((layout_id, tenant_id))):
            if wish_list.page_ids:
                pages = layout.pages[:]
                layout.clear()
                layout.pages.extend(PagesByWishListGatherer(pages=pages, wish_list=wish_list).gather())

            return layout

        return None

    @staticmethod
    def _apply_filtering(layout: DocumentLayout, filtering: DocumentLayoutFeaturesFilter) -> DocumentLayout:
        pages = [page for page in layout.pages if page.parsing_type == filtering.parsing_type]
        for page in pages:
            page.leave_only(filtering.features)

        layout.clear()
        layout.pages.extend(pages)

        return layout

    @staticmethod
    def _batch_pages(pages: list[Page], page_batch: PageBatch) -> list[Page]:
        first_page_index = page_batch.index * page_batch.size

        return pages[first_page_index : first_page_index + page_batch.size] if first_page_index < len(pages) else []

    @staticmethod
    def _add_page_to_layout(page: Page, layout: DocumentLayout) -> None:
        pages = layout.pages

        for index, old_page in enumerate(pages):
            if old_page == page:
                pages.pop(index)
                pages.insert(index, page)
                break
        else:
            pages.append(page)
