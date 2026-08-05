__all__ = [
    "all_semantic_layout_info_payload",
    "semantic_layout_info_payload",
    "semantic_layout_info_payload_without_id",
]


semantic_layout_info_payload = {
    "id": "semantic-layout-1",
    "provider": "llamaindex",
    "createdAt": "2026-06-04T10:30:00Z",
    "metadata": {
        "sourceProvider": "azure",
        "processingTimeMs": 15240,
        "confidence": 0.95,
    },
}

all_semantic_layout_info_payload = {
    "layoutId": "document-123",
    "semanticLayoutInfo": {
        "llamaindex": semantic_layout_info_payload,
    },
}

semantic_layout_info_payload_without_id = {
    "provider": "llamaindex",
    "createdAt": "2026-06-04T10:30:00Z",
    "metadata": {
        "sourceProvider": "azure",
    },
}
