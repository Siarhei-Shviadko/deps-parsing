import logging
from typing import Optional

from requests import RequestException

from deps_parsing.domain.dtos import SemanticLayoutInfo
from deps_parsing.infrastructure.exceptions import SemanticParsingProxyRequestError
from deps_parsing.infrastructure.proxies import SemanticParsingProxy
from deps_parsing.infrastructure.proxies.semantic_layout_info_mapper import (
    SemanticLayoutInfoMapper,
)

__all__ = ["SemanticLayoutService"]


class SemanticLayoutService:
    def __init__(self, semantic_parsing_proxy: SemanticParsingProxy) -> None:
        self._semantic_parsing_proxy = semantic_parsing_proxy
        self._logger = logging.getLogger(self.__class__.__name__)

    def layout_info_for(self, document_id: str, tenant_id: str) -> Optional[dict[str, SemanticLayoutInfo]]:
        try:
            payload = self._semantic_parsing_proxy.get_all_semantic_layout_info(document_id)
            return SemanticLayoutInfoMapper.from_all_providers_dict(payload, document_id)
        except (SemanticParsingProxyRequestError, RequestException):
            self._logger.debug(
                "Semantic layout info not found for document `%s` in tenant `%s`.",
                document_id,
                tenant_id,
            )
            return None
