import json
from typing import Optional

from google.cloud.documentai_v1 import DocumentProcessorServiceClient
from google.oauth2.service_account import Credentials

from .base import BaseGoogleAuth

__all__ = ["ServiceAccountAuth"]


class ServiceAccountAuth(BaseGoogleAuth):
    def create_document_ai_client(self) -> Optional[DocumentProcessorServiceClient]:
        if not self._config["account_info_json"]:
            return None

        try:
            service_account_info = json.loads(self._config["account_info_json"])

            credentials = Credentials.from_service_account_info(service_account_info)

            return DocumentProcessorServiceClient(
                credentials=credentials,
                client_options=self._make_client_options(),
            )
        except KeyError:  # if workload identity user passed instead of service account
            return None
        except Exception as ex:
            self._logger.warning(f"Service account info creds are passed, but invalid, {ex.__class__.__name__}: {ex}")
            return None
