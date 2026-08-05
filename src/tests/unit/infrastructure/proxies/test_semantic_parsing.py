from unittest.mock import Mock, patch

import pytest

from deps_parsing.infrastructure.exceptions import SemanticParsingProxyRequestError
from tests.data.semantic_layout_info import all_semantic_layout_info_payload


class TestSemanticParsingProxy:
    def test_get_all_semantic_layout_info_success(self, semantic_parsing_proxy):
        with patch.object(semantic_parsing_proxy, "_session") as mock_session:
            mock_response = Mock()
            mock_response.ok = True
            mock_response.json.return_value = all_semantic_layout_info_payload
            mock_session.get.return_value = mock_response

            result = semantic_parsing_proxy.get_all_semantic_layout_info("document-123")

            assert result == all_semantic_layout_info_payload
            mock_session.get.assert_called_once_with(
                url=(
                    f"{semantic_parsing_proxy._base_url}/api/semantic-parsing/v1/" f"semantic-layout/document-123/info"
                ),
                timeout=semantic_parsing_proxy._timeout,
                verify=semantic_parsing_proxy._verify,
            )

    def test_get_all_semantic_layout_info_failure(self, semantic_parsing_proxy):
        with patch.object(semantic_parsing_proxy, "_session") as mock_session:
            mock_response = Mock()
            mock_response.ok = False
            mock_response.url = (
                f"{semantic_parsing_proxy._base_url}/api/semantic-parsing/v1/" f"semantic-layout/document-123/info"
            )
            mock_response.content = b"404 Not Found"
            mock_session.get.return_value = mock_response

            with pytest.raises(SemanticParsingProxyRequestError):
                semantic_parsing_proxy.get_all_semantic_layout_info("document-123")
