import logging
import time
from typing import Any

import boto3
from botocore.client import BaseClient
from deps_document_layout.model import ParsingFeature

from .aws_features import AWSFeature
from .type_to_feature import PARSING_TYPE_TO_AWS_FEATURE_MAPPING

__all__ = ["AWSTextractProxy"]


class AWSTextractProxy:
    def __init__(self, region_name: str, aws_access_key_id: str, aws_secret_access_key: str) -> None:
        self._region = region_name
        self._access_key_id = aws_access_key_id
        self._secret_access_key = aws_secret_access_key

        self._client = self._authenticate_client()
        self._logger = logging.getLogger(self.__class__.__name__)

    def analyze_document_with_features(self, content: bytes, features: list[ParsingFeature]) -> dict:
        if features == [ParsingFeature.TEXT]:
            return self._extract_text_only(content)

        return self._extract_text_with_features(content, self._map_parsing_features_to_aws_features(features))

    def async_analyze_document_with_features(  # noqa: WPS231
        self,
        bucket_name: str,
        key: str,
        features: list[ParsingFeature],
    ) -> dict[str, Any]:
        serialized_features = [feature.value for feature in self._map_parsing_features_to_aws_features(features)]
        doc_location = {"S3Object": {"Bucket": bucket_name, "Name": key}}

        if features == [ParsingFeature.TEXT]:
            start_response = self._client.start_document_text_detection(
                DocumentLocation=doc_location,
            )
        else:
            start_response = self._client.start_document_analysis(
                DocumentLocation=doc_location,
                FeatureTypes=serialized_features,
            )
        job_id = start_response["JobId"]

        while True:
            if features == [ParsingFeature.TEXT]:
                response = self._client.get_document_text_detection(JobId=job_id)
            else:
                response = self._client.get_document_analysis(JobId=job_id)

            status = response["JobStatus"]
            if status == "SUCCEEDED":
                break
            elif status in {"FAILED", "PARTIAL_SUCCESS"}:
                raise RuntimeError(f"Textract job {job_id} failed. AWS response: {response}")

            self._logger.debug(f"Got {status} status from AWS Textract for {key}. Waiting...")
            time.sleep(1)

        all_blocks = response.get("Blocks", [])
        next_token = response.get("NextToken")

        while next_token:
            if features == [ParsingFeature.TEXT]:
                response = self._client.get_document_text_detection(JobId=job_id, NextToken=next_token)
            else:
                response = self._client.get_document_analysis(JobId=job_id, NextToken=next_token)

            all_blocks.extend(response.get("Blocks", []))
            next_token = response.get("NextToken")

        response["Blocks"] = all_blocks
        return response

    def _extract_text_only(self, content: bytes) -> dict:
        return self._client.detect_document_text(Document={"Bytes": content})

    def _extract_text_with_features(self, content: bytes, features: list[AWSFeature]) -> dict:
        serialized_features = [feature.value for feature in features]
        return self._client.analyze_document(Document={"Bytes": content}, FeatureTypes=serialized_features)

    @staticmethod
    def _map_parsing_features_to_aws_features(parsing_features: list[ParsingFeature]) -> list[AWSFeature]:
        unfiltered_features = (PARSING_TYPE_TO_AWS_FEATURE_MAPPING.get(feature) for feature in parsing_features)
        return [*filter(lambda feature: isinstance(feature, AWSFeature), unfiltered_features)]  # noqa: WPS356

    def _authenticate_client(self) -> BaseClient:
        aws_auth_params = {}
        if self._access_key_id:
            aws_auth_params["aws_access_key_id"] = self._access_key_id
        if self._secret_access_key:
            aws_auth_params["aws_secret_access_key"] = self._secret_access_key

        return boto3.client(
            "textract",
            region_name=self._region,
            **aws_auth_params,
        )
