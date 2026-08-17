from typing import Any, Optional

__all__ = ["StubSemanticLayoutApplication"]


class StubSemanticLayoutApplication:
    def parse(
        self,
        entity_id: str,
        tenant_id: str,
        file_path: str,
        parsing_type,
        features: Optional[set] = None,
        language: Optional[str] = None,
        routing_info: Optional[dict[str, Any]] = None,
    ) -> None:
        pass
