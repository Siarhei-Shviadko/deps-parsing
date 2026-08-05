from deps_parsing.api.serializers.v2.parsing_info import SerializedParsingInfo
from deps_parsing.api.serializers.v2.semantic_layout_info import (
    SerializedSemanticLayoutInfo,
)
from deps_parsing.domain.dtos import ParsingInfo


def test_serialized_semantic_layout_info__from_model__ok(semantic_layout_info):
    serialized = SerializedSemanticLayoutInfo.from_model(semantic_layout_info)

    payload = serialized.model_dump(by_alias=True)

    assert payload["id"] == semantic_layout_info.id
    assert payload["provider"] == "llamaindex"
    assert payload["createdAt"] == semantic_layout_info.created_at
    assert payload["metadata"]["sourceProvider"] == "azure"
    assert payload["metadata"]["processingTimeMs"] == 15240


def test_serialized_parsing_info__without_semantic_layout__none():
    parsing_info = ParsingInfo(layout_id="doc-1", document_layout_info=None, tabular_layout_info=None)

    payload = SerializedParsingInfo.from_model(parsing_info).model_dump(by_alias=True)

    assert payload["semanticLayoutInfo"] is None


def test_serialized_parsing_info__with_semantic_layout__ok(semantic_layout_info):
    parsing_info = ParsingInfo(
        layout_id="doc-1",
        document_layout_info=None,
        tabular_layout_info=None,
        semantic_layout_info={"llamaindex": semantic_layout_info},
    )

    payload = SerializedParsingInfo.from_model(parsing_info).model_dump(by_alias=True)

    assert len(payload["semanticLayoutInfo"]) == 1
    assert payload["semanticLayoutInfo"]["llamaindex"]["id"] == semantic_layout_info.id
    assert payload["semanticLayoutInfo"]["llamaindex"]["metadata"]["sourceProvider"] == "azure"
