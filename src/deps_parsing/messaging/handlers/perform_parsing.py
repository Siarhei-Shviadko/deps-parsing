import logging
import sys

from dependency_injector.wiring import Provide, inject
from deps_message_flow.commands.common import make_message_for_command
from deps_message_flow.commands.consumer import CommandHandlerReplyBuilder
from deps_message_flow.commands.consumer.command_message import CommandMessage
from deps_message_flow.events.mappers import JsonMapper
from deps_message_flow.sagas.participant import make_routing_info
from more_itertools import first

from deps_parsing.application.v2 import ParsingServiceV2
from deps_parsing.containers import Containers
from deps_parsing.domain.exceptions import BusinessException

from ..commands import PerformParsing, PerformParsingReply
from ..error_type import ErrorType

__all__ = ["perform_parsing_handler"]


logger = logging.getLogger(__name__)


@inject
def perform_parsing_handler(
    command_message: CommandMessage[PerformParsing],
    parsing_service: ParsingServiceV2 = Provide[Containers.applications.parsing_service_v2],
):
    logger.debug("Start handling PerformParsing command with payload: %s", command_message.command.__dict__)
    error_type, error_message, trace_info = None, None, None
    parsing_is_performed_locally = False
    try:
        layout_id = parsing_service.perform_parsing(
            tenant_id=command_message.command.tenant_id,
            entity_id=str(command_message.command.document_id),
            file_path=first(command_message.command.files),
            engine=command_message.command.engine,
            features=set(command_message.command.features) if command_message.command.features else None,
            document_type_id=command_message.command.document_type_id,
            language=command_message.command.language,
            routing_info=make_routing_info(command_message),
        )

        parsing_is_performed_locally = layout_id is not None

    except BusinessException as e:
        error_type, error_message, trace_info = ErrorType.BUSINESS, str(e), sys.exc_info()

    except Exception as e:
        error_type, error_message, trace_info = ErrorType.SYSTEM, str(e), sys.exc_info()

    if error_type is not None:
        logger.error(
            f"Failed to parse entity with id {command_message.command.document_id}! \n Reason: {error_message}",
            exc_info=trace_info,
        )

    if error_type is not None or parsing_is_performed_locally:
        reply = PerformParsingReply(error_type=error_type, error_message=error_message)
        reply_command_message = make_message_for_command(
            channel="NONE",
            payload=JsonMapper().serialize(reply),
            command_type=reply.__class__.__name__,
            reply_to="NONE",
        )

        return [CommandHandlerReplyBuilder.with_success(reply_command_message)]
