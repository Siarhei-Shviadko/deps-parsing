import pytest
from deps_document_layout.model import IDocumentLayoutRepository, LayoutWishList

from deps_parsing.application import DocumentLayoutService


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_paragraph__no_layout__error(
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_service: DocumentLayoutService,
    user_defined_parsing_type,
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
        wish_list=LayoutWishList(parsing_type=user_defined_parsing_type),
    )
    updated_page = updated_layout.page_of_id(page_id)
    updated_paragraph = updated_page.paragraph_of_id(paragraph_id)
    assert updated_paragraph.content == " ".join(d.content for d in paragraph_update_data)
    assert updated_paragraph.confidence == 1.0


@pytest.mark.usefixtures("save_layout")
def test_update_image__success(
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_service: DocumentLayoutService,
    document_layout_id,
    image_update_data,
    image_id,
    tenant_id,
    page_id,
):
    document_layout_service.update_image(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        page_id=page_id(),
        image_id=image_id(),
        title=image_update_data["title"],
        description=image_update_data["description"],
        filepath=image_update_data["filepath"],
        polygon=image_update_data["polygon"],
    )

    updated_layout = document_layout_repository.partial_layout_of_id(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        wish_list=LayoutWishList(),
    )

    updated_page = updated_layout.page_of_id(page_id)
    updated_image = updated_page.image_of_id(image_id())

    assert updated_image.title == image_update_data["title"]
    assert updated_image.description == image_update_data["description"]
    assert updated_image.file_path == image_update_data["filepath"]

    for point in updated_image.polygon:
        assert {"y": point.y, "x": point.x} in image_update_data["polygon"]
