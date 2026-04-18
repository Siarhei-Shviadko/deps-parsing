import json
import logging
from typing import Any, Optional

from requests import Response

from ..exceptions import TablesProxyRequestError
from .generic import GenericProxy

__all__ = ["TablesProxy"]


class TablesProxy(GenericProxy):
    v1_url_suffix = "api/tables/v1"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def extract_tables_from_image_and_textlines(
        self,
        blob: bytes,
        ocr_textlines: list[dict[str, Any]],
        source_id: Optional[str] = None,
    ) -> dict[str, Any]:
        data = {"ocrTextlines": json.dumps(ocr_textlines)}
        if source_id is not None:
            data["sourceId"] = source_id

        response = self._session.post(
            url=f"{self._base_url}/{self.v1_url_suffix}/file/extract-from-textlines",
            data=data,
            files={"file": blob},
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
            raise TablesProxyRequestError(response.content)
