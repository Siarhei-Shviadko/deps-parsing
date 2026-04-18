import logging
from typing import Any

from requests import Response

from ..exceptions import DocumentProxyRequestError
from .generic import GenericProxy

__all__ = ["DocumentProxy"]


class DocumentProxy(GenericProxy):
    v1_url_suffix = "api/document/v1"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_document_files(self, document_id: str) -> bytes:
        response = self._session.get(
            url=f"{self._base_url}/{self.v1_url_suffix}/documents/{document_id}/files",
            timeout=self._timeout,
            verify=self._verify,
        )

        self._check_response(response)

        return response.content

    def get_brief_document_info(self, document_id: str) -> dict[str, Any]:
        response = self._session.get(
            url=f"{self._base_url}/{self.v1_url_suffix}/brief-documents-info",
            params={"documentIds": document_id},
            timeout=self._timeout,
            verify=self._verify,
        )

        self._check_response(response)

        return response.json()["documents"][0]

    def _check_response(self, response: Response) -> None:
        if not response.ok:
            self._logger.error(
                "Response to %s failed with error %s",
                response.url,
                response.content,
            )
            raise DocumentProxyRequestError(response.content)
