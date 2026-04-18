import pytest
from deps_document_layout.model import IDocumentLayoutRepository, LayoutWishList

from deps_parsing.application import DocumentLayoutService

FIRST_ELEMENT: int = 0


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_table__updated(
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_service: DocumentLayoutService,
    table_update_data,
    document_layout_id,
    paragraph_id,
    table_id,
    tenant_id,
    page_id,
):
    document_layout_service.update_table(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        page_id=page_id(),
        table_id=table_id(),
        update_data=table_update_data,
    )

    updated_layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        wish_list=LayoutWishList(),
    )
    updated_page = updated_layout.page_of_id(page_id)
    updated_table = updated_page.table_of_id(table_id)
    assert updated_table.confidence == 1.0
    updated_paragraph = updated_page.paragraph_of_id(paragraph_id)
    assert updated_paragraph.content == table_update_data[FIRST_ELEMENT].content
    assert updated_paragraph.confidence == 1.0
