import logging
from abc import ABC, abstractmethod
from typing import Optional

from google.api_core.client_options import ClientOptions
from google.cloud.documentai_v1 import DocumentProcessorServiceClient

from ..raw_config import RawDocAIConfig

__all__ = ["BaseGoogleAuth"]


class BaseGoogleAuth(ABC):
    def __init__(self, config: RawDocAIConfig) -> None:
        self._config = config
        self._logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def create_document_ai_client(self) -> Optional[DocumentProcessorServiceClient]:
        pass

    def _make_client_options(self) -> ClientOptions:
        return ClientOptions(
            api_endpoint=f"{self._config['location']}-documentai.googleapis.com",
        )
