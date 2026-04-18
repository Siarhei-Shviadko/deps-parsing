from unittest.mock import Mock, patch

import pytest

from deps_parsing.infrastructure.exceptions import FileProxyRequestError
from deps_parsing.infrastructure.proxies import FileProxy


@pytest.fixture
def file_proxy():
    return FileProxy(
        base_url="http://file-service:8000",
        timeout=60,
        ssl_verify=False,
    )


class TestFileProxy:
    def test_get_file_content_success(self, file_proxy):
        with patch.object(file_proxy, "_session") as mock_session:
            mock_response = Mock()
            mock_response.ok = True
            mock_response.content = b"file content"
            mock_session.get.return_value = mock_response

            result = file_proxy.get_file_content("file-123")

            assert result == b"file content"
            mock_session.get.assert_called_once_with(
                url="http://file-service:8000/api/file/v1/files/file-123/content",
                timeout=60,
                verify=False,
            )

    def test_get_file_content_failure(self, file_proxy):
        with patch.object(file_proxy, "_session") as mock_session:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.url = "http://file-service:8000/api/file/v1/files/file-123/content"
            mock_response.content = b"404 Not Found"
            mock_session.get.return_value = mock_response

            with pytest.raises(FileProxyRequestError):
                file_proxy.get_file_content("file-123")

    def test_get_file_content_with_custom_timeout(self):
        proxy = FileProxy(
            base_url="http://file-service:8000",
            timeout=120,
            ssl_verify=True,
        )

        with patch.object(proxy, "_session") as mock_session:
            mock_response = Mock()
            mock_response.ok = True
            mock_response.content = b"content"
            mock_session.get.return_value = mock_response

            proxy.get_file_content("file-123")

            call_args = mock_session.get.call_args
            assert call_args.kwargs["timeout"] == 120
            assert call_args.kwargs["verify"] is True
