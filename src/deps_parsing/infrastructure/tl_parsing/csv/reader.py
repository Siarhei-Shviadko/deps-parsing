import csv
import logging
from io import StringIO
from itertools import islice
from typing import Iterator, Type

from ...exceptions import ParsingCsvError

__all__ = ["CsvReader"]


class CsvReader:
    def __init__(self, file: StringIO) -> None:
        self._file = file
        self._logger = logging.getLogger(self.__class__.__name__)

        self._initialize()

    @property
    def rows(self) -> Iterator[list[str]]:
        return self._reader

    def _initialize(self) -> None:
        self._dialect = self._get_csv_dialect()
        self._reader = self._get_reader()
        self.table_size = self._determine_table_size()

    def _determine_table_size(self) -> tuple[int, int]:
        self._file.seek(0)

        reader = csv.reader(self._file, dialect=self._dialect)
        cols = len(next(reader, [])) - 1  # we are minusing 1 because indexation starts from 0
        rows = sum(1 for _ in reader)

        self._file.seek(0)
        return cols, rows

    def _get_reader(self) -> Iterator[list[str]]:
        return csv.reader(self._file, dialect=self._dialect)

    def _get_csv_dialect(self) -> Type[csv.Dialect]:
        try:
            return csv.Sniffer().sniff(self._get_csv_head())
        except csv.Error as err:
            self._logger.error("Can't determine csv dialect. Error: %s", err, exc_info=True)
            raise ParsingCsvError("Can't determine csv dialect.")

    def _get_csv_head(self) -> str:
        rows_in_head = 3
        csv_head = "".join(islice(self._file, rows_in_head))
        self._file.seek(0)

        return csv_head
