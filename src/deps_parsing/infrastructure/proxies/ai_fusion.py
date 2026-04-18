import logging
from typing import TypedDict
from urllib.parse import urljoin

from requests import Response

from ..exceptions import AIFusionProxyRequestError
from .generic import GenericProxy

__all__ = ["AIFusionProxy", "RetrievedInsight"]

QuestionCode = str
InsightRequest = str


class RetrievedInsight(TypedDict):
    content: str
    errorOccurred: bool


class AIFusionProxy(GenericProxy):
    v1_url_suffix = "api/ai-fusion/v1/"

    def __init__(self, base_url: str, timeout: int, ssl_verify: bool) -> None:
        super().__init__(base_url)
        self._timeout = timeout
        self._verify = ssl_verify
        self._base_v1_url = urljoin(self.base_url, self.v1_url_suffix)

        self._logger = logging.getLogger(self.__class__.__name__)

    def retrieve_image_insights(
        self,
        llm_reference: str,
        image_path: str,
        questions: dict[QuestionCode, InsightRequest],
        grouping_factor: int,
        custom_instructions: str,
        temperature: float,
    ) -> dict[QuestionCode, RetrievedInsight]:
        response = self.session.post(
            url=urljoin(self._base_v1_url, "analysis/retrieve-file-insights"),
            json={
                "filePath": image_path,
                "model": llm_reference,
                "requestedInsights": questions,
                "customInstructions": custom_instructions,
                "params": {
                    "groupingFactor": grouping_factor,
                    "temperature": temperature,
                },
            },
            timeout=self._timeout,
            verify=self._verify,
        )

        self._check_response(response)

        return response.json()["elements"]

    def _check_response(self, response: Response) -> None:
        if not response.ok:
            self._logger.error("Image recognition requests failed with error `%s`", response.content)
            raise AIFusionProxyRequestError(response.content)
