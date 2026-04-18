import logging

from deps_message_flow.commands.producer import CommandProducer

from deps_parsing.constants import COMMANDS_CHANNEL, COMMANDS_REPLIES_CHANNEL
from deps_parsing.domain.model import DocumentTypeFactory, IDocumentTypeRepository
from deps_parsing.messaging.commands import GetDocumentTypes

__all__ = ["DocumentTypeService"]


class DocumentTypeService:
    def __init__(
        self,
        document_type_repository: IDocumentTypeRepository,
        command_producer: CommandProducer,
    ) -> None:
        self._document_type_repository = document_type_repository
        self._command_producer = command_producer

        self._logger = logging.getLogger(self.__class__.__name__)

    def initialize(self):
        self._command_producer.send(
            COMMANDS_CHANNEL,
            GetDocumentTypes(),
            COMMANDS_REPLIES_CHANNEL,
        )

    def save_document_types(self, document_types: list[dict[str, str]]) -> None:
        self._document_type_repository.save_all([DocumentTypeFactory.create(**doc_type) for doc_type in document_types])

    def save_document_type(self, document_type_id: str, tenant_id: str) -> None:
        self._document_type_repository.save(
            DocumentTypeFactory.create(document_type_id=document_type_id, tenant_id=tenant_id),
        )

    def delete_document_type(self, document_type_id: str) -> None:
        self._document_type_repository.delete(document_type_id)

    def attach_parsing_plugin(self, document_type_id: str, command_channel: str) -> None:
        if doc_type := self._document_type_repository.find_by_id(document_type_id):
            doc_type.attach_command_channel(command_channel)
            self._document_type_repository.save(doc_type)
            self._logger.info("Parsing plugin attached to the document type %s", document_type_id)
        else:
            self._logger.error("Parsing plugin wasn't attached. Document type %s doesn't exist.", document_type_id)
