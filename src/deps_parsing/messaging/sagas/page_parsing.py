import logging

from deps_message_flow.sagas.orchestration_simple_dsl import SimpleSaga

from ..sagas_data import PageParsingSagaData, PageParsingSteps

__all__ = ["PageParsingSaga"]


class PageParsingSaga(SimpleSaga[PageParsingSagaData]):
    def __init__(self, steps: PageParsingSteps) -> None:
        # fmt: off
        self._saga_definition = (
            self.step()
            .invoke_local(steps.parse_text)
            .step()
            .invoke_local(steps.parse_tables)
            .build()
        )
        # fmt: on
        self._logger = logging.getLogger(self.__class__.__name__)

    def on_saga_completed_successfully(self, saga_id: str, data: PageParsingSagaData) -> None:
        self._logger.info("PageParsingSaga: %s is completed successfully", saga_id)

    def on_saga_failed(self, saga_id: str, data: PageParsingSagaData) -> None:
        self._logger.error("PageParsingSaga: is failed", saga_id)

    def on_saga_rolled_back(self, saga_id: str, data: PageParsingSagaData) -> None:
        self._logger.error("PageParsingSaga: %s is rolled back", saga_id)
