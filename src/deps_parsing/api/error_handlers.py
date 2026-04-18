import logging
from http import HTTPStatus

from deps_document_layout.exceptions import BaseDocumentLayoutError
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.requests import Request

from deps_parsing.api.serializers.error import ErrorSerializer
from deps_parsing.domain.exceptions import *

logger = logging.getLogger(__name__)


def json_parsing_error_handler(error: ParsingException, status_code: int):
    error_message = ErrorSerializer(code=error.code, message=str(error)).model_dump()
    return JSONResponse(status_code=status_code, content=error_message)


def register_error_handler(app: FastAPI) -> None:
    @app.exception_handler(ParsingException)
    def handle_parsing_exception(req: Request, error: ParsingException):  # noqa: WPS430
        mapper = [
            (NotFoundError, HTTPStatus.NOT_FOUND),
            (UnifiedDataNotFound, HTTPStatus.BAD_REQUEST),
            (ParsingException, HTTPStatus.BAD_REQUEST),
        ]
        for error_type, status_code in mapper:
            if issubclass(type(error), error_type):
                return json_parsing_error_handler(error, status_code)

    @app.exception_handler(ValidationError)
    def bad_request(req: Request, exc: ValidationError):  # noqa: WPS430
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=ErrorSerializer(code="bad_request", message=str(exc)).model_dump(),
        )

    @app.exception_handler(BaseDocumentLayoutError)
    def handle_document_layout_exception(req: Request, exc: BaseDocumentLayoutError):  # noqa: WPS430
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=ErrorSerializer(code=exc.code, message=str(exc)).model_dump(),
        )

    @app.exception_handler(Exception)
    def handle_all_errors(req: Request, error: Exception):  # noqa: WPS430
        logger.error(f"Unhandled error {error}")
        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=ErrorSerializer(code="unhandled_error", message=str(error)).model_dump(),
        )
