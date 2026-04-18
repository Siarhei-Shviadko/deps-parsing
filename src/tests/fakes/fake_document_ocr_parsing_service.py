from deps_parsing.infrastructure.dl_parsing.document_based_service import (
    DocumentOCRBasedParsingService,
)

__all__ = ["FakeDocumentOCRParsingService"]


class FakeDocumentOCRParsingService(DocumentOCRBasedParsingService):
    def add_to_document_layout(self, document_layout, parsed_document, parsed_images):
        pass

    def recognize_blob(self, blob, features, language=None):
        return {}

    def _list_preparsed_images(self, layout_id, raw_document, parsed_document):
        return []
