import pytest
from deps_document_layout.model import IDocumentLayoutRepository, LayoutWishList

from deps_parsing.application import DocumentLayoutService


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_paragraph__updated(
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_service: DocumentLayoutService,
    paragraph_update_data,
    document_layout_id,
    paragraph_id,
    tenant_id,
    page_id,
):
    document_layout_service.update_paragraph(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        page_id=page_id(),
        paragraph_id=paragraph_id(),
        update_data=paragraph_update_data,
    )

    updated_layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        wish_list=LayoutWishList(),
    )
    updated_page = updated_layout.page_of_id(page_id)
    updated_paragraph = updated_page.paragraph_of_id(paragraph_id)
    assert updated_paragraph.content == " ".join(d.content for d in paragraph_update_data)
    assert updated_paragraph.confidence == 1.0
