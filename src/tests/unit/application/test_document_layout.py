from copy import deepcopy
from typing import cast

import pytest
from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    IDocumentLayoutRepository,
    PageBatch,
    ParsingFeature,
    ParsingType,
)

from deps_parsing.domain.exceptions import DocumentLayoutNotFound, ParsingException
from deps_parsing.domain.interfaces import IRawDocumentLayoutRepository
from tests.data.document_layout import document_layout as full_document_layout

DOCUMENT_ID = DOCUMENT_LAYOUT_ID = full_document_layout.id()
TENANT_ID = full_document_layout.tenant_id()
RAW_DOCUMENT_LAYOUT = {1: "raw_document_layout"}
FEATURES = {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}


@pytest.mark.document_layout_service
def test_parse_dl__unexpected_parsing_type__error(document_layout_repository_mock, document_layout_service):  # restore
    document_layout_repository_mock.layout_of_id.return_value = None
    with pytest.raises(NotImplementedError):
        document_layout_service.parse(
            document_id=DOCUMENT_ID,
            tenant_id=TENANT_ID,
            parsing_type=cast(ParsingType, "some parsing type"),
            features=FEATURES,
        )


@pytest.mark.document_layout_service
def test_get_dl__dl_exist__with_pages__successful(
    document_layout_repository_mock,
    raw_document_layout_repository_mock,
    azure_page_parsing_service_mock,
    document_layout_service,
):
    document_layout_repository_mock.layout_of_id.return_value = full_document_layout

    dl = document_layout_service.get_or_create_document_layout(
        document_layout_id=DOCUMENT_LAYOUT_ID,
        tenant_id=TENANT_ID,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AZURE_FORM_RECOGNIZER,
            features=FEATURES,
        ),
    )

    assert dl.tenant_id() == TENANT_ID
    assert dl.id() == DOCUMENT_LAYOUT_ID
    document_layout_repository_mock.layout_of_id.assert_called_once_with(
        layout_id=DOCUMENT_LAYOUT_ID,
        tenant_id=TENANT_ID,
        filtering=DocumentLayoutFeaturesFilter(ParsingType.AZURE_FORM_RECOGNIZER, FEATURES),
    )
    document_layout_repository_mock.save.assert_not_called()
    raw_document_layout_repository_mock.save.assert_not_called()
    azure_page_parsing_service_mock.parse.assert_not_called()


@pytest.mark.document_layout_service
def test_get_dl__dl_doesnt_exist__successful(
    document_layout_repository_mock,
    raw_document_layout_repository_mock,
    azure_page_parsing_service_mock,
    document_layout_service,
    document_layout,
):
    document_layout_id = document_layout.id()
    tenant_id = document_layout.tenant_id()
    language = "eng"
    document_layout_repository_mock.layout_of_id.return_value = None
    document_layout_repository_mock.save.return_value = None
    raw_document_layout_repository_mock.save.return_value = "file_path"
    azure_page_parsing_service_mock.choose_processable_features.return_value = FEATURES
    azure_page_parsing_service_mock.parse.return_value = document_layout, RAW_DOCUMENT_LAYOUT

    dl = document_layout_service.get_or_create_document_layout(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AZURE_FORM_RECOGNIZER,
            features=FEATURES,
        ),
        language=language,
    )

    assert dl.tenant_id() == tenant_id
    assert dl.id() == document_layout_id
    document_layout_repository_mock.layout_of_id.assert_called_once_with(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(ParsingType.AZURE_FORM_RECOGNIZER, FEATURES),
    )
    document_layout_repository_mock.save.assert_called_once_with(dl)
    raw_document_layout_repository_mock.save.assert_called_once_with(
        document_layout_id,
        RAW_DOCUMENT_LAYOUT,
        ParsingType.AZURE_FORM_RECOGNIZER.value,
    )
    azure_page_parsing_service_mock.choose_processable_features.assert_called_once_with(FEATURES)
    azure_page_parsing_service_mock.parse.assert_called_once_with(
        document_layout=dl, features=FEATURES, language=language
    )


@pytest.mark.document_layout_service
def test_save_document_layout_dict__successful(
    document_layout_repository_mock,
    document_layout_service,
    document_layout_dict,
):
    document_layout_repository_mock.save_raw.return_value = None

    document_layout_service.save_raw_document_layout(document_layout_dict)

    document_layout_repository_mock.save_raw.assert_called_with(document_layout_dict)


@pytest.mark.document_layout
def test_delete_document_layout__not_exists__no_error(
    document_layout_service,
    document_layout_id,
    tenant_id,
):
    document_layout_service.delete_document_layout(document_layout_id=document_layout_id, tenant_id=tenant_id)


@pytest.mark.document_layout
def test_delete_document_layout__layout_exists_raw_data_not_exists__deleted(
    raw_document_layout_repository: IRawDocumentLayoutRepository,
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_service,
    document_layout_id,
    document_layout,
    tenant_id,
):
    document_layout_repository.save(document_layout)
    assert document_layout_repository.is_layout_exists(layout_id=document_layout_id, tenant_id=tenant_id)

    document_layout_service.delete_document_layout(document_layout_id=DOCUMENT_LAYOUT_ID, tenant_id=TENANT_ID)

    assert not document_layout_repository.is_layout_exists(layout_id=DOCUMENT_LAYOUT_ID, tenant_id=TENANT_ID)


@pytest.mark.document_layout
def test_delete_document_layout__layout_and_raw_data_exist__deleted(
    raw_document_layout_repository: IRawDocumentLayoutRepository,
    document_layout_repository: IDocumentLayoutRepository,
    document_layout_service,
):
    parsing_type = ParsingType.AZURE_FORM_RECOGNIZER
    document_layout_repository.save(full_document_layout)
    assert document_layout_repository.is_layout_exists(layout_id=DOCUMENT_LAYOUT_ID, tenant_id=TENANT_ID)
    raw_document_layout_repository.save(
        layout_id=DOCUMENT_LAYOUT_ID,
        layout={"pages": ["some_page_data"]},
        parsing_type=parsing_type,
    )
    assert raw_document_layout_repository.layout_of_id(layout_id=DOCUMENT_LAYOUT_ID, parsing_type=parsing_type)

    document_layout_service.delete_document_layout(document_layout_id=DOCUMENT_LAYOUT_ID, tenant_id=TENANT_ID)

    assert not document_layout_repository.is_layout_exists(layout_id=DOCUMENT_LAYOUT_ID, tenant_id=TENANT_ID)
    with pytest.raises(Exception):
        raw_document_layout_repository.layout_of_id(layout_id=DOCUMENT_LAYOUT_ID, parsing_type=parsing_type)


@pytest.mark.info
def test_save_document_layout_info__layout_doesnt_exist__created(
    document_layout_repository: IDocumentLayoutRepository, document_layout_service, document_layout
):
    parsing_type = ParsingType.TESSERACT
    features = {ParsingFeature.KEY_VALUE_PAIRS}
    document_layout.update_parsing_features(parsing_type=parsing_type, features=features)
    assert not document_layout_repository.is_layout_exists(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
    )

    document_layout_service.save_document_layout_info(document_layout)

    assert document_layout == document_layout_repository.layout_of_id(
        layout_id=document_layout.id(),
        tenant_id=document_layout.tenant_id(),
        filtering=DocumentLayoutFeaturesFilter(parsing_type=parsing_type, features=features),
    )


@pytest.mark.info
def test_save_document_layout_info__layout_exists__updated(
    document_layout_repository: IDocumentLayoutRepository, document_layout_service, document_layout
):
    document_layout.update_parsing_features(parsing_type=ParsingType.AWS_TEXTRACT, features={ParsingFeature.TABLES})
    document_layout_repository.save(document_layout)
    document_layout.update_parsing_features(parsing_type=ParsingType.TESSERACT, features={ParsingFeature.TEXT})
    assert (
        ParsingType.TESSERACT
        not in document_layout_repository.layout_of_id(
            layout_id=document_layout.id(),
            tenant_id=document_layout.tenant_id(),
            filtering=DocumentLayoutFeaturesFilter(parsing_type=ParsingType.TESSERACT),
        ).parsing_features
    )

    document_layout_service.save_document_layout_info(document_layout)

    assert (
        ParsingType.TESSERACT
        in document_layout_repository.layout_of_id(
            layout_id=document_layout.id(),
            tenant_id=document_layout.tenant_id(),
            filtering=DocumentLayoutFeaturesFilter(parsing_type=ParsingType.TESSERACT),
        ).parsing_features
    )


@pytest.mark.document_layout_service
def test_get_dl__azure_document_service__dl_doesnt_exist__successful(
    document_layout_repository_mock,
    raw_document_layout_repository_mock,
    azure_document_parsing_service_mock,
    document_layout_service,
    document_layout,
):
    document_layout_id = document_layout.id()
    tenant_id = document_layout.tenant_id()
    language = "eng"
    document_layout_repository_mock.layout_of_id.return_value = None
    document_layout_repository_mock.save.return_value = None
    raw_document_layout_repository_mock.save.return_value = "file_path"
    azure_document_parsing_service_mock.choose_processable_features.return_value = FEATURES
    azure_document_parsing_service_mock.parse.return_value = document_layout, RAW_DOCUMENT_LAYOUT

    dl = document_layout_service.get_or_create_document_layout(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AZURE_FORM_RECOGNIZER,
            features=FEATURES,
        ),
        language=language,
    )

    assert dl.tenant_id() == tenant_id
    assert dl.id() == document_layout_id
    document_layout_repository_mock.layout_of_id.assert_called_once_with(
        layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(ParsingType.AZURE_FORM_RECOGNIZER, FEATURES),
    )
    document_layout_repository_mock.save.assert_called_once_with(dl)
    raw_document_layout_repository_mock.save.assert_called_once_with(
        document_layout_id,
        RAW_DOCUMENT_LAYOUT,
        ParsingType.AZURE_FORM_RECOGNIZER.value,
    )
    azure_document_parsing_service_mock.choose_processable_features.assert_called_once_with(FEATURES)
    azure_document_parsing_service_mock.parse.assert_called_once_with(
        document_layout=dl, features=FEATURES, language=language
    )


def test_find_dl__dl_doesnt_exist__error(
    document_layout_repository_mock,
    document_layout_service,
):
    document_layout_repository_mock.layout_of_id.return_value = None
    with pytest.raises(DocumentLayoutNotFound):
        document_layout_service.find_document_layout(
            document_layout_id="abc",
            tenant_id="tenant_id",
            filtering=DocumentLayoutFeaturesFilter(parsing_type=ParsingType.TESSERACT, features=set()),
        )


def test_find_dl__dl_exists__ok(
    document_layout_repository_mock,
    document_layout_service,
    document_layout,
):
    document_layout_repository_mock.layout_of_id.return_value = document_layout

    dl = document_layout_service.find_document_layout(
        document_layout_id="abc",
        tenant_id="tenant_id",
        filtering=DocumentLayoutFeaturesFilter(parsing_type=ParsingType.TESSERACT, features=set()),
    )

    assert dl


def test_find_dl__dl_exists__page_filter_provided__ok(
    document_layout_repository_mock,
    document_layout_service,
    document_layout,
):
    document_layout_repository_mock.layout_of_id.return_value = document_layout

    dl = document_layout_service.find_document_layout(
        "abc", "tenant_id", DocumentLayoutFeaturesFilter(parsing_type=ParsingType.TESSERACT, page_batch=PageBatch(1, 2))
    )

    assert dl


def test_parse__successful(
    azure_document_parsing_service_mock,
    document_layout_service,
    document_layout,
    mocker,
):
    document_id = document_layout.id()
    tenant_id = document_layout.tenant_id()
    language = "eng"
    parsing_type = ParsingType.AZURE_FORM_RECOGNIZER
    features = FEATURES

    azure_document_parsing_service_mock.parse.return_value = (document_layout, None)

    with mocker.patch.object(document_layout_service, "_find_document_layout", return_value=document_layout):
        dl_id = document_layout_service.parse(
            document_id=document_id,
            tenant_id=tenant_id,
            parsing_type=parsing_type,
            features=features,
            language=language,
        )

        azure_document_parsing_service_mock.parse.assert_called_once()
        assert dl_id == document_layout.id


def test_parse__without_parsing_features__empty_dl_saved(
    azure_document_parsing_service_mock,
    document_layout_repository_mock,
    document_layout_service,
    document_layout,
):
    document_id = document_layout.id()
    tenant_id = document_layout.tenant_id()
    language = "eng"
    parsing_type = ParsingType.AZURE_FORM_RECOGNIZER
    features = None
    document_layout_repository_mock.layout_of_id.return_value = document_layout

    dl_id = document_layout_service.parse(
        document_id=document_id,
        tenant_id=tenant_id,
        parsing_type=parsing_type,
        features=features,
        language=language,
    )

    document_layout_repository_mock.save.assert_called_once_with(document_layout)

    azure_document_parsing_service_mock.parse.assert_not_called()
    assert dl_id == document_layout.id


def test_clone_pages__cloned(
    test_saved_full_document_layout,
    document_layout_repository,
    document_layout_service,
):
    test_saved_full_document_layout.parsing_features.update({ParsingType.AWS_TEXTRACT: set(ParsingFeature)})
    document_layout_repository.save(test_saved_full_document_layout)
    tenant_id = test_saved_full_document_layout.tenant_id()
    document_layout_id = test_saved_full_document_layout.id()
    parsing_type = ParsingType.AWS_TEXTRACT

    document_layout_service.clone_pages(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        original_parsing_type=parsing_type,
    )

    saved_document_layout_with_new_parsing_type = document_layout_service.find_document_layout(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=set(ParsingFeature),
        ),
    )

    assert (
        saved_document_layout_with_new_parsing_type.parsing_features[ParsingType.USER_DEFINED]
        == test_saved_full_document_layout.parsing_features[parsing_type]
    )
    assert len(saved_document_layout_with_new_parsing_type.pages) == len(test_saved_full_document_layout.pages)

    assert len(saved_document_layout_with_new_parsing_type.merged_tables) == len(
        test_saved_full_document_layout.merged_tables,
    )


def test_clone_pages__no_document_layout__error(
    test_saved_full_document_layout,
    document_layout_repository,
    document_layout_service,
):
    tenant_id = test_saved_full_document_layout.tenant_id()
    parsing_type = ParsingType.AWS_TEXTRACT

    with pytest.raises(DocumentLayoutNotFound):
        document_layout_service.clone_pages(
            document_layout_id="fake_id",
            tenant_id=tenant_id,
            original_parsing_type=parsing_type,
        )


def test_clone_pages_with_user_defined__cloned(
    document_layout_service,
    saved_layout_with_user_defined_pages,
):
    tenant_id = saved_layout_with_user_defined_pages.tenant_id()
    document_layout_id = saved_layout_with_user_defined_pages.id()
    parsing_type = ParsingType.AWS_TEXTRACT

    document_layout_service.clone_pages(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        original_parsing_type=parsing_type,
    )

    saved_document_layout_with_new_parsing_type = document_layout_service.find_document_layout(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=set(ParsingFeature),
        ),
    )

    assert (
        saved_document_layout_with_new_parsing_type.parsing_features[ParsingType.USER_DEFINED]
        == saved_layout_with_user_defined_pages.parsing_features[parsing_type]
    )
    assert saved_document_layout_with_new_parsing_type.pages != saved_layout_with_user_defined_pages.pages
    assert len(saved_document_layout_with_new_parsing_type.pages) == len(saved_layout_with_user_defined_pages.pages)


def test_get_dl__user_defined__dl_with_user_defined_doesnt_exist__error(
    document_layout_repository_mock,
    document_layout_service,
):
    document_layout_repository_mock.layout_of_id.return_value = full_document_layout

    with pytest.raises(ParsingException):
        document_layout_service.get_or_create_document_layout(
            document_layout_id=DOCUMENT_LAYOUT_ID,
            tenant_id=TENANT_ID,
            filtering=DocumentLayoutFeaturesFilter(
                parsing_type=ParsingType.USER_DEFINED,
                features=FEATURES,
            ),
        )


def test_get_dl__user_defined__dl_exists_with_not_all_requested_features__error(
    document_layout_repository_mock,
    document_layout_service,
):
    document_layout_repository_mock.layout_of_id.return_value = full_document_layout
    expected_features = deepcopy(full_document_layout.parsing_features["AZURE_FORM_RECOGNIZER"])

    full_document_layout.parsing_features.update({ParsingType.USER_DEFINED: expected_features})

    with pytest.raises(ParsingException):
        document_layout_service.get_or_create_document_layout(
            document_layout_id=DOCUMENT_LAYOUT_ID,
            tenant_id=TENANT_ID,
            filtering=DocumentLayoutFeaturesFilter(
                parsing_type=ParsingType.USER_DEFINED,
                features=FEATURES,
            ),
        )


def test_get_dl_user_defined__dl_exists__ok(
    document_layout_repository_mock,
    document_layout_service,
):
    expected_features = deepcopy(full_document_layout.parsing_features["AZURE_FORM_RECOGNIZER"])

    full_document_layout.parsing_features.update({ParsingType.USER_DEFINED: expected_features})
    document_layout_repository_mock.layout_of_id.return_value = full_document_layout

    dl = document_layout_service.get_or_create_document_layout(
        document_layout_id=DOCUMENT_LAYOUT_ID,
        tenant_id=TENANT_ID,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.USER_DEFINED,
            features=expected_features,
        ),
    )

    assert dl
