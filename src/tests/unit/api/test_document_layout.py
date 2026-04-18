from http import HTTPStatus

import pytest
from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    PageBatch,
    ParsingFeature,
    ParsingType,
)
from deps_document_layout.serializers.document_layout import (
    SerializedDocumentLayout,
    SerializedPage,
)

from deps_parsing.constants import V1_API_PREFIX
from deps_parsing.domain.exceptions import DocumentLayoutNotFound, ParsingException
from tests.data.document_layout import document_layout, document_layout_dict
from tests.factories import PageFactory


def test_get_document_layout__gotten(client, document_layout_service_mock, tenant_id):
    document_layout_service_mock.get_or_create_document_layout.return_value = document_layout

    response = client.get(
        f"{V1_API_PREFIX}/document-layout/2",
        params={"parsingType": "AWS_TEXTRACT", "features": ["tables", "kvps", "text"]},
    )

    received_document_layout = response.json()

    assert response.status_code == HTTPStatus.OK
    assert received_document_layout["documentLayoutId"] == document_layout_dict["documentLayoutId"]
    assert received_document_layout["pages"] == document_layout_dict["pages"]
    assert received_document_layout["parsingFeatures"].keys() == document_layout_dict["parsingFeatures"].keys()

    for value1, value2 in zip(
        received_document_layout["parsingFeatures"].values(),
        document_layout_dict["parsingFeatures"].values(),
    ):
        for feature in value1:
            assert feature in value2

    document_layout_service_mock.get_or_create_document_layout.assert_called_with(
        document_layout_id="2",
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            features={ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TEXT},
            parsing_type=ParsingType.AWS_TEXTRACT,
        ),
    )


def test_create_document_layout__created(client, document_layout_service_mock, tenant_id):
    document_layout_service_mock.save_raw_document_layout.return_value = None

    response = client.post(f"{V1_API_PREFIX}/document-layout", json=document_layout_dict)

    assert response.status_code == HTTPStatus.CREATED
    document_layout_service_mock.save_raw_document_layout.assert_called_with(
        SerializedDocumentLayout(**document_layout_dict).to_dict(tenant_id)
    )


@pytest.mark.page
def test_get_document_layout_pages__empty_list__ok(
    document_layout_service_mock,
    document_layout_id,
    tenant_id,
    client,
):
    expected_pages = []
    expected_page_amount = len(expected_pages)
    parsing_type = ParsingType.AWS_TEXTRACT
    document_layout_service_mock.get_document_layout_pages_with_page_amount.return_value = (expected_pages, 0)
    params = {"parsingType": parsing_type}

    response = client.get(f"{V1_API_PREFIX}/document-layout/{document_layout_id}/pages", params=params)

    response_json = response.json()
    assert response_json["total"] == expected_page_amount
    assert response_json["pages"] == expected_pages
    document_layout_service_mock.get_document_layout_pages_with_page_amount.assert_called_once_with(
        document_layout_id=document_layout_id,
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            page_batch=PageBatch(index=PageBatch.index, size=PageBatch.size),
            features=set(),
            parsing_type=parsing_type,
        ),
    )


@pytest.mark.page
def test_get_document_layout_pages__one_page__ok(
    document_layout_service_mock,
    document_layout_id,
    tenant_id,
    client,
):
    page = PageFactory()
    expected_pages = [SerializedPage.from_model(page).dict(by_alias=True)]
    expected_page_amount = len(expected_pages)
    document_layout_service_mock.get_document_layout_pages_with_page_amount.return_value = [page], 1
    params = {"parsingType": ParsingType.AWS_TEXTRACT}

    response = client.get(f"{V1_API_PREFIX}/document-layout/{document_layout_id}/pages", params=params)

    response_json = response.json()
    assert response_json["total"] == expected_page_amount
    assert response_json["pages"] == expected_pages


@pytest.mark.info
def test_save_document_layout_info__ok(
    document_layout_service_mock,
    document_layout_id,
    tenant_id,
    client,
):
    document_layout_service_mock.save_document_layout_info.return_value = None
    document_layout_info = {
        "documentLayoutId": document_layout_id,
        "parsingFeatures": {ParsingType.TESSERACT.value: [ParsingFeature.KEY_VALUE_PAIRS.value]},
    }

    response = client.put(f"{V1_API_PREFIX}/document-layout/info", json=document_layout_info)

    assert response.status_code == HTTPStatus.OK
    document_layout_service_mock.save_document_layout_info.assert_called_once()


@pytest.mark.page
def test_save_pages__layout_doesnt_exist__not_found(document_layout_service_mock, client):
    document_layout_id = document_layout_dict["documentLayoutId"]
    pages = {"pages": document_layout_dict["pages"]}
    document_layout_service_mock.save_document_layout_pages.side_effect = DocumentLayoutNotFound(document_layout_id)

    response = client.put(f"{V1_API_PREFIX}/document-layout/{document_layout_id}/pages", json=pages)

    assert response.status_code == HTTPStatus.NOT_FOUND
    document_layout_service_mock.save_document_layout_pages.assert_called_once()


@pytest.mark.page
def test_save_pages__layout_exists__ok(client, document_layout_service_mock):
    document_layout_id = document_layout_dict["documentLayoutId"]
    pages = {"pages": document_layout_dict["pages"]}
    document_layout_service_mock.save_document_layout_pages.return_value = None

    response = client.put(f"{V1_API_PREFIX}/document-layout/{document_layout_id}/pages", json=pages)

    assert response.status_code == HTTPStatus.OK
    document_layout_service_mock.save_document_layout_pages.assert_called_once()


def test_get_user_defined_document_layout__ok(client, document_layout_service_mock):
    document_layout_id = document_layout_dict["documentLayoutId"]
    document_layout_service_mock.get_or_create_document_layout.return_value = document_layout

    response = client.get(
        f"{V1_API_PREFIX}/document-layout/{document_layout_id}",
        params={"parsingType": "USER_DEFINED", "features": ["tables", "kvps", "text"]},
    )

    assert response.status_code == HTTPStatus.OK
    document_layout_service_mock.get_or_create_document_layout.assert_called_once()


def test_get_user_defined_document_layout__doesnt_exist__400(client, document_layout_service_mock):
    document_layout_id = document_layout_dict["documentLayoutId"]
    document_layout_service_mock.get_or_create_document_layout.side_effect = ParsingException

    response = client.get(
        f"{V1_API_PREFIX}/document-layout/{document_layout_id}",
        params={"parsingType": "USER_DEFINED", "features": ["tables", "kvps", "text"]},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    document_layout_service_mock.get_or_create_document_layout.assert_called_once()
