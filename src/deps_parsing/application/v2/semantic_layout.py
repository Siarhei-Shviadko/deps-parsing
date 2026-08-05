import logging
from typing import Any, Optional

from deps_document_layout.model import ParsingFeature
from deps_message_flow.commands.producer import CommandProducer

from deps_parsing.constants import COMMANDS_REPLIES_CHANNEL
from deps_parsing.messaging.commands import ParseSemanticLayout

from ..semantic_parsing_type import SemanticParsingType
from .i_can_parse_document import ICanParseDocument

__all__ = ["SemanticLayoutApplication"]


class SemanticLayoutApplication(ICanParseDocument[ParsingFeature, SemanticParsingType, None]):
    def __init__(self, command_producer: CommandProducer) -> None:
        self._command_producer = command_producer
        self._logger = logging.getLogger(self.__class__.__name__)

    def parse(
        self,
        entity_id: str,
        tenant_id: str,
        file_path: str,
        parsing_type: SemanticParsingType,
        features: Optional[set[ParsingFeature]] = None,
        language: Optional[str] = None,
        routing_info: Optional[dict[str, Any]] = None,
    ) -> None:
        self._logger.info(
            "Dispatching ParseSemanticLayout for entity_id=%s, tenant_id=%s, provider=%s",
            entity_id,
            tenant_id,
            parsing_type.value,
        )
        self._command_producer.send(
            "SemanticParsingCommands",
            ParseSemanticLayout(
                entity_id=entity_id,
                tenant_id=tenant_id,
                file_path=file_path,
                provider=parsing_type.value,
                features=list(features) if features is not None else None,
                language=language,
            ),
            COMMANDS_REPLIES_CHANNEL,
            headers=routing_info if routing_info is not None else {},
        )
