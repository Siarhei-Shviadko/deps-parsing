import logging
from http import HTTPStatus
from typing import Any, Optional

from requests import Response

from deps_parsing.domain.exceptions import UnifiedDataNotFound

from ...exceptions import UnifierProxyRequestError
from ..generic import GenericProxy
from .element_type import UnifiedDataElement
from .unified_data_image import UnifiedDataImage

__all__ = ["UnifierProxy"]


class UnifierProxy(GenericProxy):
    v1_url_suffix = "api/unifier/v1"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def find_unified_data_by_document_id(
        self,
        document_id: str,
        unified_data_types: Optional[list[UnifiedDataElement]] = None,
    ) -> dict[str, Any]:
        params = {"unified_data_types": unified_data_types} if unified_data_types else {}
        response = self._session.get(
            url=f"{self._base_url}/{self.v1_url_suffix}/unified_data/{document_id}",
            params=params,
            timeout=self._timeout,
            verify=self._verify,
        )
        self._check_response(response)

        return response.json()

    def get_preprocessed_images(self, document_id: str) -> list[UnifiedDataImage]:
        udata = self.find_unified_data_by_document_id(document_id, [UnifiedDataElement.IMAGE])

        return [
            UnifiedDataImage.from_dict(image) for image in udata["elements"] if image["originalImageId"] is not None
        ]

    def get_original_images(self, document_id: str) -> list[UnifiedDataImage]:
        udata = self.find_unified_data_by_document_id(document_id, [UnifiedDataElement.IMAGE])

        return [UnifiedDataImage.from_dict(image) for image in udata["elements"] if image["originalImageId"] is None]

    def _check_response(self, response: Response) -> None:
        if response.status_code == HTTPStatus.NOT_FOUND:
            raise UnifiedDataNotFound(response.content)

        if not response.ok:
            self._logger.error(
                "Response to %s with payload %s failed with error %s",
                response.url,
                response.request.__dict__,
                response.content,
            )
            raise UnifierProxyRequestError(response.content)
