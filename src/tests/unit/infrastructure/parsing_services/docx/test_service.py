from deps_document_layout.model import ParsingFeature, ParsingType


def test_parse__ok(mocked_service, document_layout):
    features = set(ParsingFeature)
    document_layout, raw_parsing_response = mocked_service.parse(document_layout, features)

    assert len(document_layout.pages) == 1
    assert raw_parsing_response is None
    assert document_layout.parsing_features == {ParsingType.DOCX: features}
