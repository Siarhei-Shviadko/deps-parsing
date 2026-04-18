import logging
from typing import Optional

from deps_message_flow.events.publisher import DomainEventPublisher
from deps_tabular_layout.models import (
    CellProperties,
    EntityId,
    ParsingType,
    TabularLayout,
    TabularLayoutFactory,
)

from deps_parsing.domain.dtos import (
    TabularLayoutFilter,
    TabularLayoutInfo,
    TabularLayoutProjection,
)
from deps_parsing.domain.exceptions import TabularLayoutNotFound
from deps_parsing.domain.interfaces import (
    ICellCommandRepository,
    ITabularLayoutCommandRepository,
    ITabularLayoutQueryRepository,
)
from deps_parsing.infrastructure.tl_parsing import AbstractTabularLayoutParser

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
        document_id: str,
        tenant_id: str,
        parsing_type: ParsingType,
        features: Optional[set[str]] = None,
        language: Optional[str] = None,
    ) -> EntityId:
        layout = TabularLayoutFactory.make_empty_layout(
            document_id=document_id,
            tenant_id=tenant_id,
            parsing_type=parsing_type,
            extracted_props=list(CellProperties),
        )

        layout = self._parsing_service_for(parsing_type).parse(
            layout=layout,
        )

        self._logger.info(
            "Tabular Layout parsing for document_id: `%s` has been finished. "
            + "Document has `%s` sheets, extracted properties: `%s`",
            document_id,
            len(layout.sheets),
            layout.extracted_properties,
        )

        self._tl_command_repository.save(layout)

        return layout.id

    def layout_info_for(self, document_id: str, tenant_id: str) -> Optional[TabularLayoutInfo]:
        return self._tl_query_repository.layout_of_id_info(layout_id=document_id, tenant_id=tenant_id)

    def find_tabular_layout(
        self,
        layout_id: str,
        tenant_id: str,
        filtering: TabularLayoutFilter,
    ) -> TabularLayoutProjection:
        if tl := self._tl_query_repository.layout_projection_of_id(  # noqa: WPS337
            layout_id=layout_id,
            tenant_id=tenant_id,
            filtering=filtering,
        ):
            return tl
        raise TabularLayoutNotFound(layout_id)

    def delete_layout(self, layout_id: str, tenant_id: str) -> None:
        if layout := self._tl_query_repository.layout_of_id(layout_id=layout_id, tenant_id=tenant_id):
            self._tl_command_repository.delete(layout_id, tenant_id)
            layout.delete()
            self._publish_events(layout)
            return

        self._logger.debug("Cannot delete tabular layout `%s`. Reason: it doesn't exist.", layout_id)

    def delete_layout_cells(self, layout_id: str) -> None:
        self._cell_command_repository.delete(layout_id=layout_id)

    def _parsing_service_for(self, parsing_type: ParsingType) -> AbstractTabularLayoutParser:
        if parsing_type not in self._parsing_service_mapper:
            raise NotImplementedError(f"Parser for parsing type {parsing_type} is not implemented yet :(")

        return self._parsing_service_mapper[parsing_type]

    def _publish_events(self, tabular_layout: TabularLayout) -> None:
        self._domain_event_publisher.publish(
            aggregate_type=self.AGGREGATE_TYPE,
            aggregate_id=tabular_layout.id(),
            domain_events=tabular_layout.events,
        )
