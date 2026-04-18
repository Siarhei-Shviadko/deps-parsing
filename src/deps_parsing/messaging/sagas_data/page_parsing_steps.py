import logging

from ...infrastructure import OCRProxy, TablesProxy
from .page_parsing_data import PageParsingSagaData

__all__ = ["PageParsingSteps"]


class PageParsingSteps:
    def __init__(self, ocr_proxy: OCRProxy, tables_proxy: TablesProxy) -> None:
        self._ocr_proxy = ocr_proxy
        self._tables_proxy = tables_proxy

        self._logger = logging.getLogger(self.__class__.__name__)

    def parse_text(self, data: PageParsingSagaData) -> None:
        data.parsing_result["ocr_data"] = self._ocr_proxy.extract_text_from_image(
            data.blob,
            data.parsing_type,
            data.language,
        )
        self._logger.debug(
            "Step text recognition has been finished. Parsing type: %s, language: %s, result: %s",
            data.parsing_type,
            data.language,
            data.parsing_result["ocr_data"],
        )

    def parse_tables(self, data: PageParsingSagaData) -> None:
        if data.tables_extraction_is_needed:
            data.parsing_result["tables_data"] = self._tables_proxy.extract_tables_from_image_and_textlines(
                data.blob,
                data.parsing_result["ocr_data"],
            )
            self._logger.debug(
                "Step tables extraction has been finished. Result: %s",
                data.parsing_result["tables_data"],
            )
