from deps_parsing.infrastructure.exceptions import SemanticParsingProxyRequestError
from tests.data.semantic_layout_info import all_semantic_layout_info_payload


def test_layout_info_for__ok(
    semantic_layout_service,
    semantic_parsing_proxy_mock,
    semantic_layout_info,
    document_id,
    tenant_id,
):
    semantic_parsing_proxy_mock.get_all_semantic_layout_info.return_value = all_semantic_layout_info_payload

    info = semantic_layout_service.layout_info_for(document_id=document_id, tenant_id=tenant_id)

    assert info == {"llamaindex": semantic_layout_info}
    semantic_parsing_proxy_mock.get_all_semantic_layout_info.assert_called_once_with(document_id)


def test_layout_info_for__not_found__returns_none(
    semantic_layout_service,
    semantic_parsing_proxy_mock,
    document_id,
    tenant_id,
):
    semantic_parsing_proxy_mock.get_all_semantic_layout_info.side_effect = SemanticParsingProxyRequestError(b"404")

    assert semantic_layout_service.layout_info_for(document_id=document_id, tenant_id=tenant_id) is None
