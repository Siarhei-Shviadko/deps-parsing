import json
from http import HTTPStatus
from typing import Any

__all__ = ["FakeResponse"]


class FakeResponse:
    def __init__(self, status_code: HTTPStatus, content: Any):
        self._status_code = status_code
        self._content = content

    @property
    def status_code(self) -> HTTPStatus:
        return self._status_code

    @property
    def ok(self) -> bool:
        return self._status_code <= HTTPStatus.BAD_REQUEST

    def json(self) -> Any:
        return json.loads(self._content)

    @property
    def url(self) -> str:
        return "fake_url_for_test"

    @property
    def request(self):
        return object

    @property
    def content(self) -> Any:
        return self._content
