import logging

__all__ = []  # type: ignore


class TextractorLogsFilter(logging.Filter):
    library_to_filter = "textractor"

    def filter(self, record: logging.LogRecord):
        return self.library_to_filter not in record.pathname


root_logger = logging.getLogger()
root_logger.addFilter(TextractorLogsFilter())
