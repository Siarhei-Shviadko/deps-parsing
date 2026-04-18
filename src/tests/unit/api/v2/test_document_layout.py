from http import HTTPStatus

import pytest
from deps_document_layout.model import (
    DocumentLayoutFeaturesFilter,
    ParsingFeature,
    ParsingType,
)

from deps_parsing.constants import V2_API_PREFIX
from deps_parsing.domain.exceptions import DocumentLayoutNotFound
from tests.data.document_layout import document_layout, document_layout_dict


def test_get_document_layout_v2__gotten(client, document_layout_service_mock, tenant_id):
    document_layout_service_mock.find_document_layout.return_value = document_layout

    response = client.get(
        f"{V2_API_PREFIX}/document-layout/2",
        params={"parsingType": "AWS_TEXTRACT", "features": ["tables", "kvps", "text"]},
    )

    assert response.status_code == HTTPStatus.OK

    document_layout_service_mock.find_document_layout.assert_called_with(
        document_layout_id="2",
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features={ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TEXT},
            page_batch=None,
        ),
    )


def test_get_document_layout_v2__invalid_pagination__error(client):
    response = client.get(
        f"{V2_API_PREFIX}/document-layout/2",
        params={"parsingType": "AWS_TEXTRACT", "features": ["tables", "kvps", "text"], "batchSize": 1},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_document_layout_v2__no_layout__404_error(client, document_layout_service_mock, tenant_id):
    document_layout_service_mock.find_document_layout.side_effect = DocumentLayoutNotFound("2")

    response = client.get(
        f"{V2_API_PREFIX}/document-layout/2",
        params={"parsingType": "AWS_TEXTRACT", "features": ["tables", "kvps", "text"]},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND

    document_layout_service_mock.find_document_layout.assert_called_with(
        document_layout_id="2",
        tenant_id=tenant_id,
        filtering=DocumentLayoutFeaturesFilter(
            parsing_type=ParsingType.AWS_TEXTRACT,
            features={ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TEXT},
            page_batch=None,
        ),
    )


@pytest.mark.partial
def test_update_paragraph__no_document_layout__404(
    client,
    update_paragraph_payload,
    document_layout_id,
    page_id,
    paragraph_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id}/paragraphs/{paragraph_id}",
        json=update_paragraph_payload,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_paragraph__200(
    client,
    update_paragraph_payload,
    document_layout_id,
    page_id,
    paragraph_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/paragraphs/{paragraph_id()}",
        json=update_paragraph_payload,
    )

    assert response.status_code == HTTPStatus.OK


def test_create_user_defined_document_layout__ok(client, document_layout_service_mock):
    document_layout_id = document_layout_dict["documentLayoutId"]

    response = client.put(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/user-parsing-type",
        json={"parsingType": "AWS_TEXTRACT"},
    )

    assert response.status_code == HTTPStatus.CREATED
    document_layout_service_mock.clone_pages.assert_called_once()


@pytest.mark.partial
def test_update_image__no_document_layout__404(
    client,
    update_image_payload,
    document_layout_id,
    page_id,
    image_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/images/{image_id()}",
        json=update_image_payload,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.partial
def test_update_table__no_document_layout__404(
    client,
    update_table_payload,
    document_layout_id,
    page_id,
    table_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/tables/{table_id()}",
        json=update_table_payload,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_image__200(
    client,
    update_image_payload,
    document_layout_id,
    page_id,
    image_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/images/{image_id()}",
        json=update_image_payload,
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_table__200(
    client,
    update_table_payload,
    document_layout_id,
    page_id,
    table_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/tables/{table_id()}",
        json=update_table_payload,
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_key_value_pair__200(
    client,
    update_key_value_pair_payload,
    document_layout_id,
    page_id,
    key_value_pair_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/key-value-pairs/{key_value_pair_id()}",
        json=update_key_value_pair_payload,
    )

    assert response.status_code == HTTPStatus.OK


@pytest.mark.partial
@pytest.mark.usefixtures("save_layout")
def test_update_key_value_pair__partial_update__200(
    client,
    document_layout_id,
    page_id,
    key_value_pair_id,
    faker,
):
    payload = {
        "key": {
            "content": faker.text(max_nb_chars=15),
        }
        # No value, confidence, or order provided
    }
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/key-value-pairs/{key_value_pair_id()}",
        json=payload,
    )
    assert response.status_code == HTTPStatus.OK


@pytest.mark.partial
def test_update_key_value_pair__no_document_layout__404(
    client,
    update_key_value_pair_payload,
    document_layout_id,
    page_id,
    key_value_pair_id,
):
    response = client.patch(
        f"{V2_API_PREFIX}/document-layout/{document_layout_id}/pages/{page_id()}/key-value-pairs/{key_value_pair_id()}",
        json=update_key_value_pair_payload,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
