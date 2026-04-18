import logging
from abc import ABC
from typing import Any, Optional

from deps_document_layout.model import ParsingFeature, ParsingType
from deps_message_flow.sagas.orchestration import SagaInstanceFactory
from deps_message_flow.sagas.orchestration_simple_dsl import SimpleSaga

from deps_parsing.messaging.sagas import PageParsingSaga
from deps_parsing.messaging.sagas_data import PageParsingSagaData

from ...abstract_engine import OCREngine

__all__ = ["BaseDepsOCREngine"]


class BaseDepsOCREngine(OCREngine, ABC):
    parsing_type: ParsingType

    def __init__(self, sagas: list[SimpleSaga], saga_factory: SagaInstanceFactory) -> None:
        self._sagas = {saga.__class__: saga for saga in sagas}
        self._saga_factory = saga_factory

        self._logger = logging.getLogger(self.__class__.__name__)

    def recognize_blob(
        self,
        blob: bytes,
        features: set[ParsingFeature],
        language: Optional[str] = None,
        filename: Optional[str] = None,
    ) -> Any:
        self._logger.info("Start page saga ...")

        sd = PageParsingSagaData(blob, self.parsing_type, features, language)
        self._saga_factory.create(self._sagas[PageParsingSaga], sd)

        return sd.parsing_result

    @staticmethod
    def fetch_received_features(features: set[ParsingFeature]) -> set[ParsingFeature]:
        if ParsingFeature.TABLES in features:
            return {ParsingFeature.TEXT, ParsingFeature.TABLES}

        return {ParsingFeature.TEXT}
