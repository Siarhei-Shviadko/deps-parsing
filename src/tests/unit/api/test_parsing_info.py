from http import HTTPStatus

import pytest

from deps_parsing.constants import V2_API_PREFIX


@pytest.mark.parsing_info
def test_get_parsing_info__no_layouts__ok(client, document_layout_id, tabular_layout_service__with_mocked_excel_parser):
    response = client.get(f"{V2_API_PREFIX}/documents/{document_layout_id}/parsing-info")
    json_response = response.json()

    assert response.status_code == HTTPStatus.OK
    assert json_response["documentLayoutInfo"] is None
    assert json_response["tabularLayoutInfo"] is None


@pytest.mark.parsing_info
def test_get_parsing_info__only_tl__ok(
    client, tabular_layout_service__with_mocked_excel_parser, test_saved_full_tabular_layout
):
    response = client.get(f"{V2_API_PREFIX}/documents/{test_saved_full_tabular_layout.id()}/parsing-info")
    json_response = response.json()
    tabular_layout_info = json_response["tabularLayoutInfo"]

    assert response.status_code == HTTPStatus.OK
    assert json_response["documentLayoutInfo"] is None
    assert tabular_layout_info["id"] == test_saved_full_tabular_layout.id()
    assert tabular_layout_info["parsingType"] == test_saved_full_tabular_layout.parsing_type.value
    assert len(tabular_layout_info["sheets"]) == len(test_saved_full_tabular_layout.sheets)

    for ind in range(len(test_saved_full_tabular_layout.sheets)):
        assert tabular_layout_info["sheets"][ind]["id"] == test_saved_full_tabular_layout.sheets[ind].id()
        assert tabular_layout_info["sheets"][ind]["isHidden"] == test_saved_full_tabular_layout.sheets[ind].is_hidden
        assert len(tabular_layout_info["sheets"][ind]["tables"]) == len(
            test_saved_full_tabular_layout.sheets[ind].tables
        )
        assert len(tabular_layout_info["sheets"][ind]["images"]) == len(
            test_saved_full_tabular_layout.sheets[ind].images
        )

        for table_ind in range(len(test_saved_full_tabular_layout.sheets[ind].tables)):
            assert (
                tabular_layout_info["sheets"][ind]["tables"][table_ind]["id"]
                == test_saved_full_tabular_layout.sheets[ind].tables[table_ind].id()
            )
            assert (
                tabular_layout_info["sheets"][ind]["tables"][table_ind]["columnCount"]
                == test_saved_full_tabular_layout.sheets[ind].tables[table_ind].column_count
            )
            assert (
                tabular_layout_info["sheets"][ind]["tables"][table_ind]["rowCount"]
                == test_saved_full_tabular_layout.sheets[ind].tables[table_ind].row_count
            )

        for image_ind in range(len(test_saved_full_tabular_layout.sheets[ind].images)):
            assert (
                tabular_layout_info["sheets"][ind]["images"][image_ind]
                == test_saved_full_tabular_layout.sheets[ind].images[image_ind].id()
            )


@pytest.mark.parsing_info
def test_get_parsing_info__only_dl__ok(
    client, tabular_layout_service__with_mocked_excel_parser, test_saved_full_document_layout
):
    response = client.get(f"{V2_API_PREFIX}/documents/{test_saved_full_document_layout.id()}/parsing-info")
    json_response = response.json()
    document_layout_info = json_response["documentLayoutInfo"]

    assert response.status_code == HTTPStatus.OK
    assert json_response["tabularLayoutInfo"] is None
    assert document_layout_info["documentLayoutId"] == test_saved_full_document_layout.id()
    assert [key for key in document_layout_info["parsingFeatures"].keys()] == [
        key.value for key in test_saved_full_document_layout.parsing_features.keys()
    ]
    assert [el for value in document_layout_info["parsingFeatures"].values() for el in value] == [
        el.value for value in test_saved_full_document_layout.parsing_features.values() for el in value
    ]
    assert {test_saved_full_document_layout.pages[0].parsing_type: len(test_saved_full_document_layout.pages)} == {
        parsing_type: pages_info["pagesCount"] for parsing_type, pages_info in document_layout_info["pagesInfo"].items()
    }
