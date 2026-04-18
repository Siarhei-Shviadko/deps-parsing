from itertools import combinations

import pytest
from deps_document_layout.model import ParsingFeature
from textractor.entities.document import Document

from tests.fakes import FakeAWSTextractProxy


@pytest.mark.parametrize("features", [set(combination) for combination in combinations(ParsingFeature, 2)])
def test_recognize_blob__blob_is_recognized(
    fake_aws_proxy_page1_response: FakeAWSTextractProxy, aws_textract_engine, fake_blob, page1_dict, features
):
    response = aws_textract_engine.recognize_blob(fake_blob, features)
    assert isinstance(response, Document)
    assert set(fake_aws_proxy_page1_response.last_called_features) == features
    assert fake_aws_proxy_page1_response.last_called_content == fake_blob


@pytest.mark.parametrize(
    "features, expected",
    [
        ({ParsingFeature.TEXT}, {ParsingFeature.TEXT}),
        (
            {ParsingFeature.KEY_VALUE_PAIRS},
            {ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TEXT, ParsingFeature.IMAGES},
        ),
        ({ParsingFeature.TABLES}, {ParsingFeature.TABLES, ParsingFeature.TEXT, ParsingFeature.IMAGES}),
        (
            {ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS},
            {ParsingFeature.TABLES, ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TEXT, ParsingFeature.IMAGES},
        ),
        ({ParsingFeature.IMAGES}, {ParsingFeature.TEXT, ParsingFeature.IMAGES}),
    ],
)
def test_fetch_received_features__valid_features(aws_textract_engine, features, expected):
    assert aws_textract_engine.fetch_received_features(features) == expected
