from random import randint
from uuid import uuid4

import pytest
from deps_document_layout.model import EntityId, PageBatch
from deps_document_layout.model.document_layout import (
    DocumentLayoutFeaturesFilter,
    ParsingFeature,
    ParsingType,
)

from deps_parsing.infrastructure.repositories import DocumentLayoutRepository
from tests.data.document_layout import document_layout
from tests.data.document_layout import document_layout_2 as document_layout_azure
from tests.data.document_layout import (
    document_layout_short_pages,
    document_layout_user_defined,
    document_layout_user_defined_2,
)
from tests.factories import PageFactory
from tests.helpers import (
    compare_2_document_layout_info,
    full_compare_2_document_layouts,
)

FIRST_ELEMENT = 0
SECOND_ELEMENT = 1


def test_save_document_layout__valid_layout__ok(
    document_layout_repository: DocumentLayoutRepository, test_features_filter
):
    document_layout_repository.save(document_layout)
    saved_document_layout = document_layout_repository.layout_of_id(
        document_layout.id(), document_layout.tenant_id(), test_features_filter
    )

    assert saved_document_layout
    assert len(saved_document_layout.pages) == len(document_layout.pages)
    full_compare_2_document_layouts(saved_document_layout, document_layout)


def test_save__document_layout_exists_with_not_all_features__new_version_with_all_features__saved(
    document_layout_repository,
    test_features_filter,
):
    document_layout_repository.save(document_layout_short_pages)
    short_saved_doc_layout = document_layout_repository.layout_of_id(
        document_layout.id(), document_layout.tenant_id(), test_features_filter
    )
    try:
        assert len(short_saved_doc_layout.pages) == len(document_layout.pages)
        full_compare_2_document_layouts(short_saved_doc_layout, document_layout)
    except AssertionError:
        document_layout_repository.save(document_layout)
        full_saved_document_layout = document_layout_repository.layout_of_id(
            document_layout.id(),
            document_layout.tenant_id(),
            test_features_filter,
        )
        assert full_saved_document_layout
        assert len(full_saved_document_layout.pages) == len(document_layout.pages)
        full_compare_2_document_layouts(full_saved_document_layout, document_layout)
    else:
        assert False


def test_is_layout_exists__ok(document_layout_repository, test_features_filter):
    document_layout_repository.save(document_layout_azure)
    document_layout_repository.save(document_layout_short_pages)
    assert document_layout_repository.is_layout_exists(document_layout_azure.id(), document_layout.tenant_id())
    assert document_layout_repository.is_layout_exists(document_layout_short_pages.id(), document_layout.tenant_id())


def test_get_layout__other_tenant_id__none_returns(document_layout_repository, test_features_filter):
    document_layout_repository.save(document_layout_short_pages)

    layout = document_layout_repository.layout_of_id(
        document_layout_short_pages.id(), "fake_tenant_id", test_features_filter
    )

    assert layout is None


def test_get_layout__no_such_parsing_type__return_layout_without_pages(
    document_layout_repository, test_features_filter
):
    document_layout_repository.save(document_layout_azure)

    layout = document_layout_repository.layout_of_id(
        document_layout_azure.id(), document_layout.tenant_id(), test_features_filter
    )

    assert layout.pages == []


@pytest.mark.parametrize(
    "params",
    [
        {"features": {ParsingFeature.TABLES}},
        {"features": {ParsingFeature.IMAGES}},
        {"features": {ParsingFeature.TEXT}},
        {"features": {ParsingFeature.KEY_VALUE_PAIRS}},
        {
            "features": {
                ParsingFeature.TABLES,
                ParsingFeature.IMAGES,
                ParsingFeature.TEXT,
                ParsingFeature.KEY_VALUE_PAIRS,
                ParsingFeature.TABLES,
            }
        },
    ],
)
def test_get_layout_by_feature__ok(params, document_layout_repository):
    features_map = {
        ParsingFeature.TABLES: "tables",
        ParsingFeature.IMAGES: "images",
        ParsingFeature.TEXT: "paragraphs",
        ParsingFeature.KEY_VALUE_PAIRS: "key_value_pairs",
    }
    required_features = params["features"]
    filter_ = DocumentLayoutFeaturesFilter(**params, parsing_type=ParsingType.AWS_TEXTRACT)

    document_layout_repository.save(document_layout)
    layout = document_layout_repository.layout_of_id(document_layout.id(), document_layout.tenant_id(), filter_)

    for k, v in features_map.items():
        if k in required_features:
            assert getattr(layout.pages[0], v) == getattr(document_layout.pages[0], v)
            assert getattr(layout.pages[1], v) == getattr(document_layout.pages[1], v)
        else:
            assert getattr(layout.pages[0], v) == tuple()
            assert getattr(layout.pages[1], v) == tuple()


def test_update_parsing_features__ok(
    document_layout_repository: DocumentLayoutRepository,
    test_features_filter,
):
    assert document_layout.parsing_features == {
        ParsingType.AZURE_FORM_RECOGNIZER: {ParsingFeature.TABLES, ParsingFeature.IMAGES},
    }
    document_layout_repository.save(document_layout)
    document_layout.update_parsing_features(ParsingType.AZURE_FORM_RECOGNIZER, {ParsingFeature.KEY_VALUE_PAIRS})
    document_layout_repository.save(document_layout)

    saved_document_layout = document_layout_repository.layout_of_id(
        document_layout.id(),
        document_layout.tenant_id(),
        test_features_filter,
    )

    assert saved_document_layout.parsing_features == {
        ParsingType.AZURE_FORM_RECOGNIZER: {
            ParsingFeature.TABLES,
            ParsingFeature.IMAGES,
            ParsingFeature.KEY_VALUE_PAIRS,
        },
    }


def test_update_parsing_features__empty_features__ok(
    document_layout_repository: DocumentLayoutRepository,
    test_features_filter,
):
    document_layout.parsing_features.clear()
    document_layout_repository.save(document_layout)

    saved_document_layout = document_layout_repository.layout_of_id(
        document_layout.id(),
        document_layout.tenant_id(),
        test_features_filter,
    )

    assert saved_document_layout.parsing_features == {}


def test_save_pages__same_page_id_different_parsing_type__saved(document_layout_repository, document_layout, tenant_id):
    page_id = EntityId(uuid4().hex)
    page_number = randint(1, 10)
    parsing_type = ParsingType.AWS_TEXTRACT
    page = PageFactory(id_=page_id, page_number=page_number, parsing_type=parsing_type)
    document_layout.pages.append(PageFactory(id_=page_id, page_number=page_number, parsing_type=ParsingType.TESSERACT))
    document_layout_repository.save(document_layout)

    document_layout.pages.append(page)
    document_layout_repository.save(document_layout)

    filtering = DocumentLayoutFeaturesFilter(parsing_type=parsing_type)
    dl = document_layout_repository.layout_of_id(document_layout.id(), tenant_id, filtering=filtering)
    assert page in dl.pages


def test_get_layout_info__layout_exist__valid_info(document_layout_repository):
    document_layout_repository.save(document_layout)

    layout_info = document_layout_repository.layout_of_id_info(document_layout.id(), document_layout.tenant_id())

    compare_2_document_layout_info(document_layout, layout_info)


def test_get_layout_info__layout_does_not_exist__valid_info(document_layout_repository):
    layout_info = document_layout_repository.layout_of_id_info(document_layout.id(), document_layout.tenant_id())

    assert not layout_info


def test_delete__deleted(document_layout_repository):
    document_layout_repository.save(document_layout)
    assert document_layout_repository.layout_of_id_info(document_layout.id(), document_layout.tenant_id())

    document_layout_repository.delete(document_layout)

    assert not document_layout_repository.layout_of_id_info(document_layout.id(), document_layout.tenant_id())


@pytest.mark.page
def test_get_document_layout_pages__no_layout__empty_list(
    document_layout_repository: DocumentLayoutRepository,
    document_layout_id,
    default_page_batch,
    tenant_id,
):
    res = document_layout_repository.find_document_layout_pages_with_amount(
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
    document_layout_repository: DocumentLayoutRepository,
    default_page_batch,
    document_layout_id,
    tenant_id,
):
    page_amount = 0
    document_layout_repository.save(document_layout)

    res = document_layout_repository.find_document_layout_pages_with_amount(
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

    assert res == ([], page_amount)


@pytest.mark.page
def test_get_document_layout_pages__default_batch__first_page(
    document_layout_repository: DocumentLayoutRepository,
    default_page_batch,
):
    expected_pages = [document_layout_short_pages.pages[FIRST_ELEMENT]]
    document_layout_repository.save(document_layout_short_pages)
    page_amount = len(document_layout_short_pages.pages)

    res = document_layout_repository.find_document_layout_pages_with_amount(
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
    document_layout_repository: DocumentLayoutRepository,
    default_page_batch,
):
    expected_pages = document_layout_short_pages.pages
    document_layout_repository.save(document_layout_short_pages)
    page_amount = len(document_layout_short_pages.pages)

    res = document_layout_repository.find_document_layout_pages_with_amount(
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

    assert res == (expected_pages, page_amount)


@pytest.mark.page
def test_get_document_layout_pages__batch_index_1__second_page(
    document_layout_repository: DocumentLayoutRepository,
    default_page_batch,
):
    expected_pages = [document_layout_short_pages.pages[SECOND_ELEMENT]]
    document_layout_repository.save(document_layout_short_pages)
    page_amount = len(document_layout_short_pages.pages)

    res = document_layout_repository.find_document_layout_pages_with_amount(
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
    document_layout_repository: DocumentLayoutRepository,
    default_page_batch,
):
    document_layout_repository.save(document_layout_short_pages)
    page_amount = len(document_layout_short_pages.pages)

    res = document_layout_repository.find_document_layout_pages_with_amount(
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
    document_layout_repository: DocumentLayoutRepository,
    default_page_batch,
):
    page = document_layout.pages[FIRST_ELEMENT]
    assert page.tables
    assert page.images
    assert page.paragraphs
    assert page.key_value_pairs
    document_layout_repository.save(document_layout)

    res = document_layout_repository.find_document_layout_pages_with_amount(
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


@pytest.mark.info
def test_save__layout_without_pages__saved(
    document_layout_repository: DocumentLayoutRepository,
    document_layout_id,
    document_layout,
    tenant_id,
):
    document_layout_repository.save(document_layout)

    assert document_layout_repository.is_layout_exists(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
    )


def test_layout_of_id_without_pages__ok(document_layout_repository: DocumentLayoutRepository):
    document_layout_repository.save(document_layout)

    layout = document_layout_repository.layout_of_id_without_pages(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
    )

    assert layout.id == document_layout.id
    assert layout.tenant_id == document_layout.tenant_id
    assert layout.parsing_features == document_layout.parsing_features
    assert layout.merged_tables == document_layout.merged_tables
    assert not layout.pages


def test_layout_of_id_without_pages__no_layout__none(document_layout_repository: DocumentLayoutRepository):
    layout = document_layout_repository.layout_of_id_without_pages(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
    )

    assert not layout


def test_save_cloned_user_defined_document_layout__ok(document_layout_repository: DocumentLayoutRepository):
    document_layout_repository.save(document_layout_user_defined)
    document_layout_repository.save_cloned_user_defined_document_layout(document_layout_user_defined_2)

    saved_document_layout = document_layout_repository.layout_of_id(
        layout_id=document_layout_user_defined.id(),
        tenant_id=document_layout_user_defined.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=set(),
        ),
    )

    assert saved_document_layout.id == document_layout_user_defined.id
    assert saved_document_layout.tenant_id == document_layout_user_defined.tenant_id
    assert saved_document_layout.pages[FIRST_ELEMENT] != document_layout_user_defined.pages[FIRST_ELEMENT]
    assert saved_document_layout.pages[FIRST_ELEMENT] == document_layout_user_defined_2.pages[FIRST_ELEMENT]


def test_save_cloned_user_defined_document_layout__no_layout__no_error(
    document_layout_repository: DocumentLayoutRepository,
):
    document_layout_repository.save_cloned_user_defined_document_layout(document_layout_user_defined_2)

    saved_document_layout = document_layout_repository.layout_of_id(
        layout_id=document_layout_user_defined_2.id(),
        tenant_id=document_layout_user_defined_2.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=set(),
        ),
    )

    assert saved_document_layout.id == document_layout_user_defined_2.id
    assert saved_document_layout.tenant_id == document_layout_user_defined_2.tenant_id
    assert saved_document_layout.pages == document_layout_user_defined_2.pages
