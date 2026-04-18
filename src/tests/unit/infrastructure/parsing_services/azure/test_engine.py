import pytest
from deps_document_layout.model import ParsingFeature


@pytest.mark.azure_parsing
def test_recognize_blob__with_kvp__ok(azure_proxy_mock, azure_engine, lite_azure_proxy_response):
    file_blob = b"some blob"
    azure_proxy_mock.analyze_prebuilt_document.return_value = lite_azure_proxy_response
    azure_engine.recognize_blob(file_blob, {ParsingFeature.KEY_VALUE_PAIRS})

    azure_proxy_mock.analyze_prebuilt_document.assert_called_once_with(file_blob)


@pytest.mark.azure_parsing
def test_recognize_blob__without_kvp__ok(azure_proxy_mock, azure_engine, lite_azure_proxy_response):
    file_blob = b"some blob"
    azure_proxy_mock.analyze_prebuilt_layout.return_value = lite_azure_proxy_response
    azure_engine.recognize_blob(file_blob, {ParsingFeature.TABLES})

    azure_proxy_mock.analyze_prebuilt_layout.assert_called_once_with(file_blob)


@pytest.mark.azure_parsing
def test_get_received_features__without_kvp__ok(azure_engine):
    features = azure_engine.fetch_received_features({ParsingFeature.TABLES})

    assert features == {ParsingFeature.TEXT, ParsingFeature.TABLES}


@pytest.mark.azure_parsing
def test_get_received_features__with_kvp__ok(azure_engine):
    features = azure_engine.fetch_received_features({ParsingFeature.KEY_VALUE_PAIRS})

    assert features == {ParsingFeature.TEXT, ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS}
