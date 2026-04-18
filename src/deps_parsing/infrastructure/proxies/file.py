import logging

from requests import Response

from ..exceptions import FileProxyRequestError
from .generic import GenericProxy

__all__ = ["FileProxy"]


class FileProxy(GenericProxy):
    v1_url_suffix = "api/file/v1"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_file_content(self, file_id: str) -> bytes:
        response = self._session.get(
            url=f"{self._base_url}/{self.v1_url_suffix}/files/{file_id}/content",
            timeout=self._timeout,
            verify=self._verify,
        )

        self._check_response(response)

        return response.content

    def _check_response(self, response: Response) -> None:
        if not response.ok:
            self._logger.error(
                "Response to %s failed with error %s",
                response.url,
                response.content,
            )
            raise FileProxyRequestError(response.content)
