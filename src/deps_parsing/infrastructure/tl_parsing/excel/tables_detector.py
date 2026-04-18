from typing import Protocol

from openpyxl.worksheet.worksheet import Worksheet

from ..table_reference import TableReference

__all__ = ["IDetectTables"]


class IDetectTables(Protocol):
    def detect_tables(self, sheet: Worksheet) -> list[TableReference]:
        pass
