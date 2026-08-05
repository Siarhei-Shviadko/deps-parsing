import pytest

from deps_parsing.infrastructure.proxies import FileProxy, SemanticParsingProxy


@pytest.fixture
def file_proxy(containers) -> FileProxy:
    config = containers.config()
    return containers.external_services.file.cls(
        base_url=config["file"]["url"],
        timeout=config["file"]["proxy_timeout"],
        ssl_verify=config["ssl_verify"],
    )


@pytest.fixture
def semantic_parsing_proxy(containers) -> SemanticParsingProxy:
    return containers.external_services.semantic_parsing()
