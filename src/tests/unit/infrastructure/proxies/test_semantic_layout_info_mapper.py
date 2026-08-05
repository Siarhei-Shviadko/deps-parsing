from deps_parsing.infrastructure.proxies.semantic_layout_info_mapper import (
    SemanticLayoutInfoMapper,
)
from tests.data.semantic_layout_info import (
    all_semantic_layout_info_payload,
    semantic_layout_info_payload,
    semantic_layout_info_payload_without_id,
)


def test_from_dict__ok(semantic_layout_info):
    result = SemanticLayoutInfoMapper.from_dict(semantic_layout_info_payload, layout_id="document-123")

    assert result == semantic_layout_info


def test_from_dict__missing_id__uses_layout_id():
    result = SemanticLayoutInfoMapper.from_dict(
        semantic_layout_info_payload_without_id,
        layout_id="document-123",
    )

    assert result.id == "document-123"


def test_from_all_providers_dict__ok(semantic_layout_info):
    result = SemanticLayoutInfoMapper.from_all_providers_dict(
        all_semantic_layout_info_payload,
        layout_id="document-123",
    )

    assert result == {"llamaindex": semantic_layout_info}


def test_from_all_providers_dict__missing_semantic_layout_info__returns_empty_dict():
    result = SemanticLayoutInfoMapper.from_all_providers_dict({}, layout_id="document-123")

    assert result == {}
