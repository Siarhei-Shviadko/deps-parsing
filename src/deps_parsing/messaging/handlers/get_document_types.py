import logging

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.common import CommandReplyOutcome, ReplyMessageHeaders
from deps_message_flow.commands.consumer.command_message import CommandMessage

from deps_parsing.application import DocumentTypeService
from deps_parsing.containers import Containers

__all__ = ["get_document_types_reply_handler"]

logger = logging.getLogger(__name__)


def is_command_successful(command_message: CommandMessage) -> bool:
    return (
        command_message.message.get_required_header(ReplyMessageHeaders.REPLY_OUTCOME)
        == CommandReplyOutcome.SUCCESS.name
    )


@inject
def get_document_types_reply_handler(  # noqa: WPS463
    command_message: CommandMessage,
    service: DocumentTypeService = Provide[Containers.applications.document_type_service],
):
    if is_command_successful(command_message):
        document_types = command_message.command.document_types
        service.save_document_types(document_types)

        logger.info("Document types updated successfully")

    else:
        logger.error(f"Failed to get document types. Command headers: {command_message.message.headers}")
