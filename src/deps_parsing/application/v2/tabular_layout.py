import logging
from typing import Any, Optional

from deps_message_flow.events.publisher import DomainEventPublisher
from deps_tabular_layout.models import (
    CellProperties,
    EntityId,
    ParsingType,
    TabularLayoutFactory,
)

from deps_parsing.domain.interfaces import (
    ICellCommandRepository,
    ITabularLayoutCommandRepository,
    ITabularLayoutQueryRepository,
)
from deps_parsing.infrastructure.tl_parsing.v2 import AbstractTabularLayoutParser

from .i_can_parse_document import ICanParseDocument

__all__ = ["TabularLayoutService"]


class TabularLayoutService(ICanParseDocument[str, ParsingType, EntityId]):
    AGGREGATE_TYPE = "TabularLayout"

    def __init__(
        self,
        parsing_service_mapper: dict[ParsingType, AbstractTabularLayoutParser],
        tl_command_repository: ITabularLayoutCommandRepository,
        cell_command_repository: ICellCommandRepository,
        tl_query_repository: ITabularLayoutQueryRepository,
        domain_event_publisher: DomainEventPublisher,
    ) -> None:
        self._tl_command_repository = tl_command_repository
        self._cell_command_repository = cell_command_repository
        self._tl_query_repository = tl_query_repository
        self._parsing_service_mapper = parsing_service_mapper
        self._domain_event_publisher = domain_event_publisher

        self._logger = logging.getLogger(self.__class__.__name__)

    def parse(
        self,
        entity_id: str,
        tenant_id: str,
        file_path: str,
        parsing_type: ParsingType,
        features: Optional[set[str]] = None,
        language: Optional[str] = None,
        routing_info: Optional[dict[str, Any]] = None,
    ) -> EntityId:
        layout = TabularLayoutFactory.make_empty_layout(
            document_id=entity_id,
            tenant_id=tenant_id,
            parsing_type=parsing_type,
            extracted_props=list(CellProperties),
        )

        layout = self._parsing_service_for(parsing_type).parse(file_path=file_path, layout=layout)

        self._logger.info(
            "Tabular Layout parsing for entity_id: `%s` has been finished. "
            + "Document has `%s` sheets, extracted properties: `%s`",
            entity_id,
            len(layout.sheets),
            layout.extracted_properties,
        )

        self._tl_command_repository.save(layout)

        return layout.id

    def _parsing_service_for(self, parsing_type: ParsingType) -> AbstractTabularLayoutParser:
        if parsing_type not in self._parsing_service_mapper:
            raise NotImplementedError(f"Parser for parsing type {parsing_type} is not implemented yet :(")

        return self._parsing_service_mapper[parsing_type]
