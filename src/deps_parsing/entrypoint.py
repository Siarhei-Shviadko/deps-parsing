import logging
import os
from typing import Awaitable, Callable

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import Response

from deps_parsing import api, constants, messaging
from deps_parsing.api.error_handlers import (
    json_parsing_error_handler,
    register_error_handler,
)
from deps_parsing.containers import Containers
from deps_parsing.domain.exceptions import AuthError
from deps_parsing.extras.fastapi_utils import add_auth_to_openapi
from deps_parsing.infrastructure.access_management import user
from deps_parsing.settings import Settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_containers() -> Containers:
    settings = Settings()
    containers = Containers(messaging_driver_settings=settings.messaging_driver_settings)
    containers.config.from_dict(settings.model_dump())
    containers.init_resources()
    containers.wire(
        packages=[api, messaging],
    )

    containers.message_brokers.broker_client().user_context = user

    if containers.config.instrumentation_enabled():
        from deps_observability_instrumentation import (  # noqa: WPS433
            instrument_external_clients,
            instrument_messaging,
            setup_instrumentation,
        )

        setup_instrumentation()
        instrument_messaging(containers.messaging.producer(), containers.messaging.consumer())
        instrument_external_clients(
            [
                containers.external_services.unifier(),
                containers.external_services.tables(),
                containers.external_services.ocr(),
                containers.external_services.document(),
            ],
        )
        logger.info("Instrumentation enabled.")

    containers.core.wire(
        modules=[api.endpoints.service_info],
    )
    containers.datasources.wire(
        modules=[api.endpoints.healthcheck],
    )

    return containers


def create_fastapi() -> FastAPI:
    containers: Containers = init_containers()

    fastapi_app = FastAPI(
        title=constants.PROJECT_NAME,
        version=containers.config.version(),
        docs_url=f"{constants.V1_API_PREFIX}{constants.SWAGGER_DOC_URL}"
        if containers.config.documentation_enabled()
        else None,
        description=constants.DESCRIPTION,
        openapi_url=f"{constants.V1_API_PREFIX}/openapi.json" if containers.config.documentation_enabled() else None,
    )
    fastapi_app.include_router(api.debug_router, prefix=constants.BASE_API_PREFIX)
    fastapi_app.include_router(api.healthcheck_router, prefix=constants.BASE_API_PREFIX)
    fastapi_app.include_router(api.service_info_router, prefix=constants.BASE_API_PREFIX)
    fastapi_app.include_router(api.v1_router, prefix=constants.V1_API_PREFIX)
    fastapi_app.include_router(api.v2_router, prefix=constants.V2_API_PREFIX)
    fastapi_app.containers = containers

    register_auth(fastapi_app)
    register_error_handler(fastapi_app)

    return fastapi_app


def register_auth(app: FastAPI):
    add_auth_to_openapi(app)

    @app.middleware("http")
    async def handle_authorization(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        try:
            api.auth.set_user_from_token(request)
        except AuthError as err:
            return json_parsing_error_handler(err, err.status_code)
        return await call_next(request)


def run_api():
    use_web_concurrency = "WEB_CONCURRENCY" in os.environ
    options = {
        "host": "0.0.0.0",  # noqa: S104
        "port": 8000,
        "log_level": "info",
        "workers": os.getenv("WEB_CONCURRENCY") if use_web_concurrency else 3,
        "reload": os.getenv("ENV", "prod") == "development",
    }

    uvicorn.run("deps_parsing.entrypoint:create_fastapi", **options)


def run_message_dispatcher() -> None:
    containers: Containers = init_containers()

    containers.applications.document_type_service().initialize()

    dispatcher = containers.message_dispatcher()
    dispatcher.start_consuming()
