import pytest
from azure.ai.formrecognizer import DocumentLine, DocumentSpan, DocumentWord

from deps_parsing.infrastructure.dl_parsing.azure.spans import SpansOf


@pytest.mark.azure_parsing
def test_init__incompatible_element__error():
    with pytest.raises(RuntimeError):
        SpansOf("string")


@pytest.mark.azure_parsing
def test_include__false():
    line = DocumentLine(spans=[DocumentSpan(offset=0, length=10)])
    word = DocumentWord(span=DocumentSpan(offset=11, length=4))

    assert not SpansOf(line).include(SpansOf(word))


@pytest.mark.azure_parsing
def test_include__true():
    line = DocumentLine(spans=[DocumentSpan(offset=0, length=10)])
    word = DocumentWord(span=DocumentSpan(offset=0, length=4))

    assert SpansOf(line).include(SpansOf(word))
