import logging
from typing import Any, Optional

from deps_document_layout.model import ParsingFeature
from deps_document_layout.model import ParsingType as DLParsingType
from deps_message_flow.commands.producer import CommandProducer
from deps_tabular_layout.models import ParsingType as TLParsingType

from deps_parsing.constants import COMMANDS_REPLIES_CHANNEL
from deps_parsing.domain.dtos import ParsingInfo
from deps_parsing.domain.exceptions import UnsupportedParsingType
from deps_parsing.domain.model import IDocumentTypeRepository
from deps_parsing.infrastructure.proxies import DocumentProxy
from deps_parsing.messaging.commands import ParseDocument

from .document_layout import DocumentLayoutService
from .entity_id import EntityId
from .i_can_parse_document import ICanParseDocument
from .parsing_type import LayoutTypeReference, ParsingType
from .tabular_layout import TabularLayoutService

__all__ = ["ParsingService"]


class ParsingService:
    def __init__(
        self,
        document_proxy: DocumentProxy,
        document_type_repository: IDocumentTypeRepository,
        command_producer: CommandProducer,
        dl_service: DocumentLayoutService,
        tl_service: TabularLayoutService,
        default_ocr_engine: str,
    ) -> None:
        self._document_proxy = document_proxy
        self._document_type_repository = document_type_repository
        self._command_producer = command_producer
        self._dl_service = dl_service
        self._tl_service = tl_service
        self._default_ocr_engine = default_ocr_engine

        self._logger = logging.getLogger(self.__class__.__name__)

    @property
    def parsing_applications_map(self) -> dict[LayoutTypeReference, ICanParseDocument]:
        return {
            DLParsingType: self._dl_service,
            TLParsingType: self._tl_service,
        }

    def perform_parsing(
        self,
        document_id: str,
        tenant_id: str,
        features: Optional[set[ParsingFeature]] = None,
        engine: Optional[str] = None,
        document_type_id: Optional[str] = None,
        language: Optional[str] = None,
        routing_info: Optional[dict[str, Any]] = None,
    ) -> Optional[EntityId]:
        if (command_channel := self._get_command_channel(document_type_id, tenant_id)) is not None:
            return self._parse_by_plugin(
                command_channel=command_channel,
                document_id=document_id,
                tenant_id=tenant_id,
                engine=engine or self._default_ocr_engine,
                features=features,
                language=language,
                extra_headers=routing_info,
            )

        parsing_type = self._determine_parsing_type(
            document_id=document_id,
            document_type_id=document_type_id,
            engine=engine or self._default_ocr_engine,
        )

        return self.parsing_applications_map[parsing_type.layout_type].parse(
            document_id=document_id,
            tenant_id=tenant_id,
            parsing_type=parsing_type.value,
            features=features,
            language=language,
        )

    def get_parsing_info(self, document_id: str, tenant_id: str) -> ParsingInfo:
        dl_info = self._dl_service.layout_info_for(document_id, tenant_id)
        tl_info = self._tl_service.layout_info_for(document_id, tenant_id)
        return ParsingInfo(layout_id=document_id, document_layout_info=dl_info, tabular_layout_info=tl_info)

    def delete_layout(self, document_id: str, tenant_id: str) -> None:
        self._dl_service.delete_document_layout(document_id, tenant_id)
        self._tl_service.delete_layout(document_id, tenant_id)

    def _get_document_extension(self, document_id: str) -> str:
        doc_info = self._document_proxy.get_brief_document_info(document_id)
        return doc_info["files"][0].split(".")[-1]

    def _determine_parsing_type(
        self,
        document_id: str,
        engine: str,
        document_type_id: Optional[str] = None,
    ) -> ParsingType:
        doc_extension = self._get_document_extension(document_id)

        if ParsingType.supports(doc_extension):
            return ParsingType(doc_extension)
        elif ParsingType.supports(engine):
            return ParsingType(engine)

        self._logger.error(
            "Can't determine ParsingType for document: %s, document_type: %s, engine: %s.",
            document_id,
            document_type_id,
            engine,
        )
        raise UnsupportedParsingType("Can't determine ParsingType")

    def _get_command_channel(self, document_type_id: Optional[str], tenant_id: str) -> Optional[str]:
        if document_type_id is not None and (  # noqa: WPS337
            document_type := self._document_type_repository.find_by_id_for_tenant(
                document_type_id,
                tenant_id,
            )
        ):
            command_channel = document_type.command_channel.name if document_type.command_channel is not None else None
            self._logger.debug("Command channel for document_type_id: %s is %s", document_type_id, command_channel)
            return command_channel

    def _parse_by_plugin(
        self,
        command_channel: str,
        document_id: str,
        tenant_id: str,
        engine: str,
        features: Optional[set[ParsingFeature]] = None,
        language: Optional[str] = None,
        extra_headers: Optional[dict[str, Any]] = None,
    ) -> None:
        command_payload = {
            "document_id": document_id,
            "tenant_id": tenant_id,
            "engine": engine,
            "features": list(features) if features is not None else None,
            "language": language,
        }

        self._logger.info(
            "Proxying Parsing command to Plugin, command_channel: %s, with payload: %s",
            command_channel,
            command_payload,
        )

        self._command_producer.send(
            command_channel,
            ParseDocument(**command_payload),
            COMMANDS_REPLIES_CHANNEL,
            headers=extra_headers if extra_headers is not None else {},
        )
