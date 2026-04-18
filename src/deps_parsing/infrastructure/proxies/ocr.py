import logging
from typing import Any

from deps_document_layout.model import ParsingType
from requests import Response

from ..exceptions import OCRProxyRequestError
from .generic import GenericProxy

__all__ = ["OCRProxy"]


class OCRProxy(GenericProxy):
    v2_url_suffix = "api/ocr/v2"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def extract_text_from_image(
        self,
        blob: bytes,
        engine: ParsingType,
        language: str,
    ) -> dict[str, Any]:
        response = self._session.post(
            url=f"{self._base_url}/{self.v2_url_suffix}/extract-text",
            files={"file": blob},
            data={"engine": engine.value, "language": language},
            timeout=self._timeout,
            verify=self._verify,
        )
        self._check_response(response)

        return response.json()

    def _check_response(self, response: Response) -> None:
        if not response.ok:
            self._logger.error(
                "Response to %s with payload %s failed with error %s",
                response.url,
                response.request.__dict__,
                response.content,
            )
            raise OCRProxyRequestError(response.content)
