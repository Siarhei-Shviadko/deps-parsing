import logging
from typing import Optional

from deps_document_layout.model import (
    DocumentLayout,
    DocumentLayoutFactory,
    DocumentLayoutFeaturesFilter,
    EntityId,
    ParsingFeature,
    ParsingType,
)
from deps_message_flow.commands.producer import CommandProducer

from deps_parsing.domain.services import SplitTablesDetectionService
from deps_parsing.infrastructure.dl_parsing.v2 import (
    IParseDocuments,
    OCRedPageRawResponse,
)
from deps_parsing.infrastructure.repositories import (
    DocumentLayoutRepository,
    RawDocumentLayoutRepository,
)

from .i_can_parse_document import ICanParseDocument

__all__ = ["DocumentLayoutService"]


class DocumentLayoutService(ICanParseDocument[ParsingFeature, ParsingType, EntityId]):
    AGGREGATE_TYPE: str = "DocumentLayout"

    def __init__(
        self,
        parsing_service_mapper: dict[ParsingType, IParseDocuments],
        split_tables_detector: SplitTablesDetectionService,
        document_layout_repository: DocumentLayoutRepository,
        raw_document_layout_repository: RawDocumentLayoutRepository,
        command_producer: CommandProducer,
        merge_tables_enabled: bool,
    ) -> None:
        self._parsing_service_mapper = parsing_service_mapper
        self._document_layout_repository = document_layout_repository
        self._raw_document_layout_repository = raw_document_layout_repository
        self._command_producer = command_producer
        self._split_tables_detector = split_tables_detector
        self._merge_tables_enabled = merge_tables_enabled

        self._logger = logging.getLogger(self.__class__.__name__)

    def parse(
        self,
        entity_id: str,
        tenant_id: str,
        file_path: str,
        parsing_type: ParsingType,
        features: Optional[set[ParsingFeature]] = None,
        language: Optional[str] = None,
    ) -> EntityId:
        document_layout = self._find_or_create_document_layout(
            document_layout_id=entity_id,
            tenant_id=tenant_id,
            filtering=DocumentLayoutFeaturesFilter(
                parsing_type=parsing_type,
                features=features or set(),
            ),
        )

        if features is None:
            self._logger.info(
                "Skip filling DocumentLayout for id: `%s`, because no parsing features passed.",
                document_layout.id(),
            )
            self._save_document_layout(document_layout)

            return document_layout.id

        return self._parse(
            file_path=file_path,
            document_layout=document_layout,
            parsing_type=parsing_type,
            features=features,
            language=language,
        ).id

    def _find_or_create_document_layout(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> DocumentLayout:
        if document_layout := self._find_document_layout(document_layout_id, tenant_id, filtering):
            document_layout.retain_merged_tables_only_for(filtering.parsing_type)

            return document_layout

        return self._create_document_layout(document_layout_id, tenant_id)

    @staticmethod
    def _create_document_layout(document_layout_id: str, tenant_id: str) -> DocumentLayout:
        return DocumentLayoutFactory.make_document_layout(tenant_id, document_layout_id)

    def _find_document_layout(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> Optional[DocumentLayout]:
        return self._document_layout_repository.layout_of_id(
            layout_id=document_layout_id,
            tenant_id=tenant_id,
            filtering=filtering,
        )

    def _get_parsing_service_by(self, parsing_type: ParsingType) -> IParseDocuments:
        try:
            return self._parsing_service_mapper[parsing_type]
        except KeyError:
            raise NotImplementedError(f"Parsing service for {parsing_type} is not implemented")

    def _save_raw_document_layout(
        self,
        document_layout_id: str,
        raw_document_layout: OCRedPageRawResponse,
        parsing_type: ParsingType,
    ) -> None:
        self._raw_document_layout_repository.save(document_layout_id, raw_document_layout, parsing_type)

    def _save_document_layout(self, document_layout: DocumentLayout) -> None:
        self._document_layout_repository.save(document_layout)

    def _parse(
        self,
        file_path: str,
        document_layout: DocumentLayout,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
        language: Optional[str] = None,
    ) -> DocumentLayout:
        self._logger.info(
            "Start document layout parsing process for document_layout_id: %s, "
            + "parsing_type: %s, features: %s, language: %s",
            document_layout.id(),
            parsing_type,
            features,
            language,
        )

        parsing_service = self._get_parsing_service_by(parsing_type)

        processable_features = parsing_service.choose_processable_features(features)

        if not processable_features or document_layout.has_features(parsing_type, processable_features):
            self._logger.info(
                "Skip document layout parsing for id: `%s`. Reason: %s. Requested features: %s, "
                + "processable features: %s, parsing_type: %s",
                document_layout.id(),
                "features already parsed" if processable_features else "no processable features",
                features,
                processable_features,
                parsing_type,
            )
            return document_layout

        document_layout.clear()
        document_layout.clear_merged_tables(parsing_type=parsing_type)
        document_layout, raw_document_layout = parsing_service.parse(
            file_path=file_path,
            document_layout=document_layout,
            features=processable_features,
            language=language,
        )

        if self._merge_tables_enabled:
            self._merge_split_tables(document_layout, for_parsing_type=parsing_type)

        self._save_document_layout(document_layout)
        if raw_document_layout:
            self._save_raw_document_layout(document_layout.id(), raw_document_layout, parsing_type)

        return document_layout

    def _merge_split_tables(self, document_layout: DocumentLayout, for_parsing_type: ParsingType) -> None:
        if not document_layout.has_features(for_parsing_type, {ParsingFeature.TABLES}):
            self._logger.info(
                "Skip split tables merging for document layout `%s`, because it doesn't have tables.",
                document_layout.id(),
            )
            return

        try:
            self._logger.info(
                "Starting split tables merging for document layout `%s`...",
                document_layout.id(),
            )

            split_tables_groups = self._split_tables_detector.detect_split_tables(
                document_layout=document_layout,
                for_parsing_type=for_parsing_type,
            )

            self._logger.info(
                "Merged split tables for document layout `%s` on pages: `%s`",
                document_layout.id(),
                [[table.page_number for table in group.tables] for group in split_tables_groups],
            )

            for merged_table in split_tables_groups:
                document_layout.register_merged_tables(
                    raw_table=merged_table.to_raw(),
                )
        except Exception as exc:
            self._logger.error(
                "Cannot merge split tables for document layout `%s`. Reason: %s",
                document_layout.id(),
                exc,
                exc_info=True,
            )
