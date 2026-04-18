import json
import logging
from typing import Optional

from deps_object_storage.gcp.settings import Settings
from google.cloud import documentai_v1 as docai
from google.cloud import storage
from google.oauth2.service_account import Credentials as CredentialsServiceAccount

from .auth import BaseGoogleAuth, ServiceAccountAuth, WorkloadIdentityFederationAuth
from .exceptions import DocumentAIEngineDisabled
from .raw_config import RawDocAIConfig
from .retry import retry_with_callback

__all__ = ["GCPDocumentAIProxy"]


class GCPDocumentAIProxy:
    def __init__(
        self,
        config: RawDocAIConfig,
    ) -> None:
        self._auth_clients: list[BaseGoogleAuth] = [
            ServiceAccountAuth(config),
            WorkloadIdentityFederationAuth(config),
        ]

        self._project_id = config["project_id"]
        self._location = config["location"]
        self._form_recognition_processor_id = config["form_recognition_processor_id"]

        self._logger = logging.getLogger(self.__class__.__name__)

        self._client = self._create_document_ai_client()
        self._storage_settings = Settings()

    def perform_form_recognition(
        self,
        document_content: bytes,
        mime_type: str,
    ) -> docai.Document:
        if self._client is None:
            raise DocumentAIEngineDisabled("Document AI engine is disabled. No valid credentials provided.")

        processor_path = self._client.processor_path(
            self._project_id,
            self._location,
            self._form_recognition_processor_id,
        )

        retried_request = retry_with_callback(
            function=self._processor_request,
            callback=self._reinitialize_client,
            retries=1,
        )

        return retried_request(
            document=document_content,
            mime_type=mime_type,
            processor_path=processor_path,
        )

    def perform_full_document_recognition(
        self,
        gcs_input_uri: str,
        gcs_output_uri: str,
        mime_type: str = "application/pdf",
        timeout: int = 600,
    ) -> docai.Document:
        """
        :param gcs_input_uri: path/to/file.pdf
        :param gcs_output_uri: gs://bucket/output/ (directory)
        :param mime_type: MIME-type of input file
        :param timeout: wait time (in seconds)
        :return: docai.Document — parsed document
        """
        if self._client is None:
            raise DocumentAIEngineDisabled("Document AI engine is disabled. No valid credentials provided.")

        processor_path = self._client.processor_path(
            self._project_id,
            self._location,
            self._form_recognition_processor_id,
        )

        gcs_input_uri = f"gs://{self._storage_settings.bucket_name}/{gcs_input_uri}"
        gcs_input = docai.GcsDocument(gcs_uri=gcs_input_uri, mime_type=mime_type)
        input_config = docai.BatchDocumentsInputConfig(gcs_documents=docai.GcsDocuments(documents=[gcs_input]))

        final_output_uri = f"{gcs_output_uri.rstrip('/')}/"

        gcs_output_config = docai.DocumentOutputConfig.GcsOutputConfig(gcs_uri=final_output_uri)
        output_config = docai.DocumentOutputConfig(gcs_output_config=gcs_output_config)

        request = docai.BatchProcessRequest(
            name=processor_path,
            input_documents=input_config,
            document_output_config=output_config,
        )

        retried_request = retry_with_callback(
            function=self._batch_processor_request,
            callback=self._reinitialize_client,
            retries=1,
        )
        output_uris = retried_request(request, timeout=timeout)

        if not output_uris:
            raise RuntimeError("No output URIs returned from batch processing")

        # There will be only 1 json as long as we send only 1 input file
        first_output_uri = output_uris[0]
        return self._download_document_from_gcs(first_output_uri)

    def _batch_processor_request(  # noqa: WPS231
        self,
        request: docai.BatchProcessRequest,
        timeout: int = 600,
    ) -> list[str]:
        operation = self._client.batch_process_documents(request=request)
        self._logger.info("Waiting for batch processing to complete...")
        operation.result(timeout=timeout)
        metadata = operation.metadata
        self._logger.info("Batch processing finished, parsing metadata...")

        output_uris: list[str] = []

        if hasattr(metadata, "individual_process_statuses"):
            for status in metadata.individual_process_statuses:
                status_msg = getattr(status, "status", None)
                if status_msg and getattr(status_msg, "code", None) != 0:
                    self._logger.error(
                        "Error while processing %s: %s",
                        getattr(status, "input_gcs_source", "<unknown>"),
                        getattr(status_msg, "message", "<no message>"),
                    )
                    continue

                out = getattr(status, "output_gcs_destination", None)
                if out:
                    output_uris.append(out)
                else:
                    self._logger.warning(
                        "No output_gcs_destination for input %s (status: %s)",
                        getattr(status, "input_gcs_source", "<unknown>"),
                        status_msg,
                    )

        return output_uris

    def _download_document_from_gcs(self, gcs_output_uri: str) -> docai.Document:
        self._logger.info(f"Downloading Document AI output from {gcs_output_uri}")

        parsed = gcs_output_uri.replace("gs://", "").split("/", 1)
        bucket_name = parsed[0]
        prefix = parsed[1].rstrip("/")

        client = self._create_storage_client()
        bucket = client.bucket(bucket_name)

        blobs = list(bucket.list_blobs(prefix=prefix))
        json_blobs = [b for b in blobs if b.name.endswith(".json")]
        if not json_blobs:
            raise FileNotFoundError(f"No JSON output found in {gcs_output_uri}")

        try:  # noqa: WPS501
            blob = json_blobs[0]
            json_data = blob.download_as_text()
            document_dict = json.loads(json_data)
        finally:
            bucket.delete_blobs(json_blobs)

        return docai.Document.from_json(json.dumps(document_dict))

    def _processor_request(
        self,
        document: bytes,
        mime_type: str,
        processor_path: str,
    ) -> docai.Document:
        raw_document = docai.RawDocument(
            content=document,
            mime_type=mime_type,
        )

        request = docai.ProcessRequest(
            name=processor_path,
            raw_document=raw_document,
        )

        response = self._client.process_document(request=request)

        return response.document

    def _create_document_ai_client(self) -> Optional[docai.DocumentProcessorServiceClient]:
        client = None

        for auth_client in self._auth_clients:
            client = auth_client.create_document_ai_client()

            if client is not None:
                break

        if client is None:
            self._logger.warning("Document AI engine is disabled. No valid credentials provided.")

        return client

    def _create_storage_client(self) -> Optional[storage.Client]:
        json_data = json.loads(self._storage_settings.auth_key)
        project_id = json_data.get("project_id")
        credentials = CredentialsServiceAccount.from_service_account_info(
            json_data,
        )
        return storage.Client(
            project=project_id,
            credentials=credentials,
        )

    def _reinitialize_client(self) -> None:
        self._client = self._create_document_ai_client()
