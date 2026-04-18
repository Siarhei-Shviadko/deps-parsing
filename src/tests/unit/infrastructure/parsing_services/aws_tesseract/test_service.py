from deps_document_layout.model import ParsingFeature, ParsingType


def test_parse__ok(totally_mocked_aws_parsing_service, document_layout):
    features = set(ParsingFeature)
    document_layout, raw_parsing_response = totally_mocked_aws_parsing_service.parse(document_layout, features)

    assert len(document_layout.pages) == 1
    assert len(raw_parsing_response) == 1
    assert document_layout.parsing_features == {ParsingType.AWS_TEXTRACT: features}


def test_parse_by_document__ok(totally_mocked_aws_document_parsing_service, document_layout):
    features = set(ParsingFeature)
    document_layout, raw_parsing_response = totally_mocked_aws_document_parsing_service.parse(document_layout, features)

    assert len(document_layout.pages) == 2
    assert document_layout.parsing_features == {ParsingType.AWS_TEXTRACT: features}
