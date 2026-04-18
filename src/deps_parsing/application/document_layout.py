import logging
from typing import Any, Optional

from deps_document_layout.model import (
    CellUpdateData,
    DocumentLayout,
    DocumentLayoutFactory,
    DocumentLayoutFeaturesFilter,
    EntityId,
    KeyValuePairUpdateData,
    LayoutWishList,
    LineUpdateData,
    Page,
    PageWishList,
    ParsingFeature,
    ParsingType,
    RawInsertPagesData,
    RawPolygon,
)
from deps_message_flow.commands.producer import CommandProducer

from deps_parsing.domain.dtos import DocumentLayoutInfo
from deps_parsing.domain.exceptions import DocumentLayoutNotFound, ParsingException
from deps_parsing.domain.model import IDocumentTypeRepository
from deps_parsing.domain.services import SplitTablesDetectionService
from deps_parsing.infrastructure.dl_parsing import IParseDocuments, OCRedPageRawResponse
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
        document_type_repository: IDocumentTypeRepository,
        command_producer: CommandProducer,
        merge_tables_enabled: bool,
    ) -> None:
        self._parsing_service_mapper = parsing_service_mapper
        self._document_layout_repository = document_layout_repository
        self._raw_document_layout_repository = raw_document_layout_repository
        self._document_type_repository = document_type_repository
        self._command_producer = command_producer
        self._split_tables_detector = split_tables_detector
        self._merge_tables_enabled = merge_tables_enabled

        self._logger = logging.getLogger(self.__class__.__name__)

    def get_or_create_document_layout(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
        language: Optional[str] = None,
    ) -> DocumentLayout:
        document_layout = self._find_or_create_document_layout(document_layout_id, tenant_id, filtering)

        if self._document_layout_should_be_parsed(  # noqa: WPS337
            document_layout=document_layout,
            parsing_type=filtering.parsing_type,
            features=filtering.features,
        ):
            return self._parse(
                document_layout=document_layout,
                parsing_type=filtering.parsing_type,
                features=filtering.features,
                language=language,
            )

        return document_layout

    def find_document_layout(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> DocumentLayout:
        if document_layout := self._find_document_layout(  # noqa: WPS:337
            document_layout_id=document_layout_id,
            tenant_id=tenant_id,
            filtering=filtering,
        ):
            return document_layout

        raise DocumentLayoutNotFound(document_layout_id)

    def get_or_create_document_layout_info(self, document_layout_id: str, tenant_id: str) -> DocumentLayout:
        return (
            layout
            if (layout := self._layout_without_pages(document_layout_id, tenant_id)) is not None
            else self._create_document_layout(document_layout_id, tenant_id)
        )

    def layout_info_for(self, document_id: str, tenant_id: str) -> Optional[DocumentLayoutInfo]:
        return self._find_document_layout_info(document_id, tenant_id)

    def save_raw_document_layout(self, raw_document_layout: dict[str, Any]) -> None:
        self._document_layout_repository.save_raw(raw_document_layout)

    def parse(
        self,
        document_id: str,
        tenant_id: str,
        parsing_type: ParsingType,
        features: Optional[set[ParsingFeature]] = None,
        language: Optional[str] = None,
    ) -> EntityId:
        document_layout = self._find_or_create_document_layout(
            document_layout_id=document_id,
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
            document_layout=document_layout,
            parsing_type=parsing_type,
            features=features,
            language=language,
        ).id

    def delete_document_layout(self, document_layout_id: str, tenant_id: str) -> None:
        document_layout = self._layout_without_pages(document_layout_id=document_layout_id, tenant_id=tenant_id)

        if not document_layout:
            self._logger.debug("Cannot delete document layout `%s`. Reason: it doesn't exist.", document_layout_id)
            return

        self._delete_document_layout(document_layout)
        self._delete_raw_document_layout(document_layout)

    def save_document_layout_info(self, document_layout: DocumentLayout) -> None:
        saved_document_layout = self._layout_without_pages(
            document_layout_id=document_layout.id(),
            tenant_id=document_layout.tenant_id(),
        )

        if saved_document_layout:
            self._update_document_layout_info(saved_document_layout, document_layout)
        else:
            self._save_document_layout(document_layout)

    def save_document_layout_pages(self, document_layout_id: str, tenant_id: str, pages: RawInsertPagesData) -> None:
        if not pages:
            self._logger.warning("Cannot save pages. Page list is empty.")
            return

        self._check_document_layout_existence(document_layout_id=document_layout_id, tenant_id=tenant_id)
        self._document_layout_repository.save_raw_pages(pages)

    def get_document_layout_pages_with_page_amount(
        self,
        document_layout_id: str,
        tenant_id: str,
        filtering: DocumentLayoutFeaturesFilter,
    ) -> tuple[list[Page], int]:
        return self._document_layout_repository.find_document_layout_pages_with_amount(
            document_layout_id=document_layout_id,
            tenant_id=tenant_id,
            filtering=filtering,
        )

    def update_paragraph(
        self,
        layout_id: str,
        tenant_id: str,
        page_id: str,
        paragraph_id: str,
        update_data: list[LineUpdateData],
    ) -> None:
        layout = self._partial_layout_of_id(
            layout_id=layout_id,
            tenant_id=tenant_id,
            wish_list=LayoutWishList(pages=[PageWishList(page_id=page_id, paragraph_ids=[paragraph_id])]),
        )
        layout.update_paragraph(
            page_id=EntityId(page_id),
            paragraph_id=EntityId(paragraph_id),
            lines_to_update=update_data,
        )
        self._save_document_layout(layout)

    def update_image(
        self,
        layout_id: str,
        tenant_id: str,
        page_id: str,
        image_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        filepath: Optional[str] = None,
        polygon: Optional[RawPolygon] = None,
    ) -> None:
        layout = self._partial_layout_of_id(
            layout_id=layout_id,
            tenant_id=tenant_id,
            wish_list=LayoutWishList(pages=[PageWishList(page_id=page_id, image_ids=[image_id])]),
        )
        layout.update_image(
            page_id=EntityId(page_id),
            image_id=EntityId(image_id),
            title=title,
            description=description,
            file_path=filepath,
            polygon=polygon,
        )
        self._save_document_layout(layout)

    def update_table(
        self,
        layout_id: str,
        tenant_id: str,
        page_id: str,
        table_id: str,
        update_data: list[CellUpdateData],
    ) -> None:
        layout = self._partial_layout_of_id(
            layout_id=layout_id,
            tenant_id=tenant_id,
            wish_list=LayoutWishList(pages=[PageWishList(page_id=page_id, table_ids=[table_id])]),
        )
        layout.update_table(
            page_id=EntityId(page_id),
            table_id=EntityId(table_id),
            cells_to_update=update_data,
        )
        self._save_document_layout(layout)

    def update_key_value_pair(
        self,
        layout_id: str,
        tenant_id: str,
        page_id: str,
        key_value_pair_id: str,
        update_data: KeyValuePairUpdateData,
    ) -> None:
        layout = self._partial_layout_of_id(
            layout_id=layout_id,
            tenant_id=tenant_id,
            wish_list=LayoutWishList(pages=[PageWishList(page_id=page_id, key_value_pair_ids=[key_value_pair_id])]),
        )
        layout.update_key_value_pair(
            page_id=EntityId(page_id),
            key_value_pair_id=EntityId(key_value_pair_id),
            update_data=update_data,
        )
        self._save_document_layout(layout)

    def clone_pages(
        self,
        document_layout_id: str,
        tenant_id: str,
        original_parsing_type: ParsingType,
    ) -> None:
        document_layout = self.find_document_layout(
            document_layout_id=document_layout_id,
            tenant_id=tenant_id,
            filtering=DocumentLayoutFeaturesFilter(parsing_type=original_parsing_type, features=set(ParsingFeature)),
        )

        document_layout.clone_pages_with_new_parsing_type(
            original_parsing_type=original_parsing_type,
            new_parsing_type=ParsingType.USER_DEFINED,
        )

        self._save_cloned_user_defined_document_layout(document_layout)

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

    def _find_document_layout_info(self, document_layout_id: str, tenant_id: str) -> Optional[DocumentLayoutInfo]:
        return self._document_layout_repository.layout_of_id_info(document_layout_id, tenant_id)

    def _layout_without_pages(self, document_layout_id: str, tenant_id: str) -> Optional[DocumentLayout]:
        return self._document_layout_repository.layout_of_id_without_pages(document_layout_id, tenant_id)

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

    def _save_cloned_user_defined_document_layout(self, document_layout: DocumentLayout) -> None:
        self._document_layout_repository.save_cloned_user_defined_document_layout(document_layout)

    def _delete_document_layout(self, document_layout: DocumentLayout) -> None:
        self._document_layout_repository.delete(document_layout)

    def _delete_raw_document_layout(self, document_layout: DocumentLayout) -> None:
        for parsing_type in document_layout.parsing_features.keys():
            self._raw_document_layout_repository.delete(layout_id=document_layout.id(), parsing_type=parsing_type)

    def _update_document_layout_info(self, old_layout: DocumentLayout, new_layout: DocumentLayout) -> None:
        if new_layout.parsing_features:
            for parsing_type, features in new_layout.parsing_features.items():
                old_layout.update_parsing_features(parsing_type=parsing_type, features=features)

            self._save_document_layout(old_layout)

    def _check_document_layout_existence(self, document_layout_id: str, tenant_id: str) -> None:
        if self._document_layout_repository.is_layout_exists(layout_id=document_layout_id, tenant_id=tenant_id):
            return

        raise DocumentLayoutNotFound(document_layout_id)

    def _parse(
        self,
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

    def _partial_layout_of_id(
        self,
        layout_id: str,
        tenant_id: str,
        wish_list: LayoutWishList,
    ) -> DocumentLayout:
        layout = self._document_layout_repository.partial_layout_of_id(
            layout_id=layout_id,
            tenant_id=tenant_id,
            wish_list=wish_list,
        )

        if layout:
            return layout

        raise DocumentLayoutNotFound(layout_id)

    @staticmethod
    def _document_layout_should_be_parsed(
        document_layout: DocumentLayout,
        parsing_type: ParsingType,
        features: set[ParsingFeature],
    ) -> bool:
        if parsing_type == ParsingType.CUSTOM:
            return False

        if parsing_type == ParsingType.USER_DEFINED:
            if document_layout.has_features(  # noqa: WPS337
                parsing_type=ParsingType.USER_DEFINED,
                features=features,
            ):
                return False
            raise ParsingException(f"Parsing for {ParsingType.USER_DEFINED} parsing type is not applicable")

        return True
