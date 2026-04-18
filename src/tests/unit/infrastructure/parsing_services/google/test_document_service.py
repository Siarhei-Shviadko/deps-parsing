from deps_document_layout.model import DocumentLayout, ParsingFeature
from google.cloud.documentai import Document

from deps_parsing.infrastructure.dl_parsing import DocumentAIDocumentParsingService


def test_docai_document_parsing_service__ok(
    mocked_document_ai_document_parsing_service: DocumentAIDocumentParsingService,
    parsed_file__all_types: Document,
    document_layout: DocumentLayout,
):
    dl, raw_dl = mocked_document_ai_document_parsing_service.parse(
        document_layout=document_layout,
        features={ParsingFeature.TEXT, ParsingFeature.KEY_VALUE_PAIRS, ParsingFeature.TABLES},
        language="en",
    )

    assert len(dl.pages) == 1

    assert len(dl.pages[0].paragraphs) == len(parsed_file__all_types.pages[0].paragraphs) + 40  # 40 those are cells
    assert len(dl.pages[0].tables) == len(parsed_file__all_types.pages[0].tables)
    assert len(dl.pages[0].key_value_pairs) == len(parsed_file__all_types.pages[0].form_fields)

    assert len(raw_dl["pages"][0]["paragraphs"]) == len(parsed_file__all_types.pages[0].paragraphs)
    assert len(raw_dl["pages"][0]["tables"]) == len(parsed_file__all_types.pages[0].tables)
    assert len(raw_dl["pages"][0]["form_fields"]) == len(parsed_file__all_types.pages[0].form_fields)
