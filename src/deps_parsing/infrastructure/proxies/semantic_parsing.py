import logging
from typing import Any

from requests import Response

from ..exceptions import SemanticParsingProxyRequestError
from .generic import GenericProxy

__all__ = ["SemanticParsingProxy"]


class SemanticParsingProxy(GenericProxy):
    v1_url_suffix = "api/semantic-parsing/v1"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_all_semantic_layout_info(self, layout_id: str) -> dict[str, Any]:
        response = self._session.get(
            url=f"{self._base_url}/{self.v1_url_suffix}/semantic-layout/{layout_id}/info",
            timeout=self._timeout,
            verify=self._verify,
        )

        self._check_response(response)

        return response.json()

    def _check_response(self, response: Response) -> None:
        if not response.ok:
            self._logger.error(
                "Response to %s failed with error %s",
                response.url,
                response.content,
            )
            raise SemanticParsingProxyRequestError(response.content)
