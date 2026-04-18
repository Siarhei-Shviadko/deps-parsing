import pytest
from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    IDocumentLayoutRepository,
    PageBatch,
    ParsingFeature,
    ParsingType,
)

from deps_parsing.domain.exceptions import DocumentLayoutNotFound
from deps_parsing.infrastructure.repositories.document_layout.mappers import PageMapper
from tests.data.document_layout import document_layout, document_layout_short_pages
from tests.factories import PageFactory

FIRST_ELEMENT = 0
SECOND_ELEMENT = 1


@pytest.mark.page
def test_get_document_layout_pages__no_layout__empty_list(
    document_layout_service,
    document_layout_id,
    tenant_id,
    default_page_batch,
):
    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features=set(),
            page_batch=PageBatch(
                index=default_page_batch.index,
                size=default_page_batch.size,
            ),
        ),
    )

    assert res == ([], 0)


@pytest.mark.page
def test_get_document_layout_pages__no_parsing_type__empty_list(
    document_layout_repository: IDocumentLayoutRepository,
    default_page_batch,
    document_layout_id,
    document_layout_service,
    tenant_id,
):
    document_layout_repository.save(document_layout)

    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AZURE_FORM_RECOGNIZER,
            features=set(),
            page_batch=PageBatch(
                index=default_page_batch.index,
                size=default_page_batch.size,
            ),
        ),
    )

    assert res == ([], 0)


@pytest.mark.page
def test_get_document_layout_pages__default_batch__first_page(
    document_layout_repository: IDocumentLayoutRepository,
    default_page_batch,
    document_layout_service,
):
    expected_pages = [document_layout_short_pages.pages[FIRST_ELEMENT]]
    page_amount = len(document_layout_short_pages.pages)
    document_layout_repository.save(document_layout_short_pages)

    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_short_pages.id(),
        tenant_id=document_layout_short_pages.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features=set(),
            page_batch=PageBatch(
                index=default_page_batch.index,
                size=default_page_batch.size,
            ),
        ),
    )

    assert res == (expected_pages, page_amount)


@pytest.mark.page
def test_get_document_layout_pages__batch_size_2__two_pages(
    document_layout_repository: IDocumentLayoutRepository,
    default_page_batch,
    document_layout_service,
):
    expected_pages = document_layout_short_pages.pages
    document_layout_repository.save(document_layout_short_pages)

    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_short_pages.id(),
        tenant_id=document_layout_short_pages.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features=set(),
            page_batch=PageBatch(
                index=default_page_batch.index,
                size=2,
            ),
        ),
    )

    assert res == (expected_pages, len(expected_pages))


@pytest.mark.page
def test_get_document_layout_pages__batch_index_1__second_page(
    document_layout_repository: IDocumentLayoutRepository,
    default_page_batch,
    document_layout_service,
):
    expected_pages = [document_layout_short_pages.pages[SECOND_ELEMENT]]
    page_amount = len(document_layout_short_pages.pages)
    document_layout_repository.save(document_layout_short_pages)

    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_short_pages.id(),
        tenant_id=document_layout_short_pages.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features=set(),
            page_batch=PageBatch(
                index=1,
                size=default_page_batch.size,
            ),
        ),
    )

    assert res == (expected_pages, page_amount)


@pytest.mark.page
def test_get_document_layout_pages__batch_extra_index__empty_list(
    document_layout_repository: IDocumentLayoutRepository,
    default_page_batch,
    document_layout_service,
):
    document_layout_repository.save(document_layout_short_pages)
    page_amount = len(document_layout_short_pages.pages)

    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout_short_pages.id(),
        tenant_id=document_layout_short_pages.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features=set(),
            page_batch=PageBatch(
                index=20,
                size=default_page_batch.size,
            ),
        ),
    )

    assert res == ([], page_amount)


@pytest.mark.page
def test_get_document_layout_pages__only_tables__ok(
    document_layout_repository: IDocumentLayoutRepository,
    default_page_batch,
    document_layout_service,
):
    page = document_layout.pages[FIRST_ELEMENT]
    assert page.tables
    assert page.images
    assert page.paragraphs
    assert page.key_value_pairs
    document_layout_repository.save(document_layout)

    res = document_layout_service.get_document_layout_pages_with_page_amount(
        document_layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features={ParsingFeature.TABLES},
            page_batch=PageBatch(
                index=default_page_batch.index,
                size=default_page_batch.size,
            ),
        ),
    )

    gotten_page = res[FIRST_ELEMENT][FIRST_ELEMENT]
    assert gotten_page.tables
    assert not gotten_page.images
    assert not gotten_page.paragraphs
    assert not gotten_page.key_value_pairs


@pytest.mark.page
def test_save_document_layout_pages__layout_doesnt_exist__not_found_error(
    document_layout_service,
    document_layout_id,
    tenant_id,
):
    pages = PageMapper.to_dict(document_layout_id=document_layout_id, pages=PageFactory.build_batch(size=2))

    with pytest.raises(DocumentLayoutNotFound):
        document_layout_service.save_document_layout_pages(document_layout_id, tenant_id, pages)


@pytest.mark.page
def test_save_document_layout_pages__layout_exists__ok(
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_id,
    document_layout,
    document_layout_service,
    tenant_id,
):
    page_number = 2
    parsing_type = ParsingType.TESSERACT
    pages = PageMapper.to_dict(
        document_layout_id=document_layout_id,
        pages=PageFactory.build_batch(size=page_number, parsing_type=parsing_type),
    )
    document_layout_repository.save(document_layout)
    assert not document_layout_repository.layout_of_id(
        document_layout_id,
        tenant_id,
        DocumentLayoutFeaturesFilter(parsing_type=parsing_type),
    ).pages

    document_layout_service.save_document_layout_pages(document_layout_id, tenant_id, pages)

    assert (
        len(
            document_layout_repository.layout_of_id(
                document_layout_id,
                tenant_id,
                DocumentLayoutFeaturesFilter(parsing_type=parsing_type),
            ).pages
        )
        == page_number
    )
