import json
import tempfile
from typing import Any, Optional

import requests
from google.auth.identity_pool import Credentials
from google.cloud.documentai_v1 import DocumentProcessorServiceClient

from .base import BaseGoogleAuth

__all__ = ["WorkloadIdentityFederationAuth"]


class WorkloadIdentityFederationAuth(BaseGoogleAuth):
    def create_document_ai_client(self) -> Optional[DocumentProcessorServiceClient]:
        if not self._credentials_are_passed():
            return None

        if (access_token := self._fetch_access_token()) is None:
            return None

        if (raw_workload_identity_credentials := self._build_workload_identity_credentials(access_token)) is None:
            return None

        creds = Credentials.from_info(raw_workload_identity_credentials)

        return DocumentProcessorServiceClient(
            credentials=creds,
            client_options=self._make_client_options(),
        )

    def _credentials_are_passed(self) -> bool:
        return (
            bool(self._config["account_info_json"])
            and bool(self._config["idp_client_id"])
            and bool(self._config["idp_token_url"])
            and bool(self._config["idp_client_secret"])
        )

    def _fetch_access_token(self) -> Optional[str]:
        data = {
            "client_id": self._config["idp_client_id"],
            "client_secret": self._config["idp_client_secret"],
            "grant_type": "client_credentials",
        }

        try:
            response = requests.post(self._config["idp_token_url"], data=data, timeout=60)
            response.raise_for_status()

            return response.json().get("access_token")
        except requests.RequestException as ex:
            self._logger.warning(f"Failed to fetch access token: {ex.__class__.__name__}: {ex}")
            return None

    def _build_workload_identity_credentials(self, access_token: str) -> Optional[dict[str, Any]]:
        try:
            creds = json.loads(self._config["account_info_json"])

            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(access_token.encode())
                temp_file_path = temp_file.name

            creds["credential_source"]["file"] = temp_file_path

            return creds
        except json.JSONDecodeError as ex:
            self._logger.warning(f"Failed to parse account info JSON: {ex.__class__.__name__}: {ex}")
            return None
