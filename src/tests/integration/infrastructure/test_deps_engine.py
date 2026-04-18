import pytest
from deps_document_layout.model import ParsingFeature


@pytest.mark.deps_parsing
def test_recognize_blob__all_steps__ok(tesseract_engine, requests_mock):
    ocr_data = "ocr_data"
    tables_data = "tables_data"
    requests_mock.post("http://ocr:8000/api/ocr/v2/extract-text", json=ocr_data)
    requests_mock.post("http://tables:8000/api/tables/v1/file/extract-from-textlines", json=tables_data)

    res = tesseract_engine.recognize_blob(b"blob", {ParsingFeature.TABLES}, "eng")

    assert res == {"ocr_data": ocr_data, "tables_data": tables_data}


@pytest.mark.deps_parsing
def test_recognize_blob__only_text__ok(tesseract_engine, requests_mock):
    ocr_data = "ocr_data"
    requests_mock.post("http://ocr:8000/api/ocr/v2/extract-text", json=ocr_data)

    res = tesseract_engine.recognize_blob(b"blob", {ParsingFeature.TEXT}, "eng")

    assert res == {"ocr_data": ocr_data}
