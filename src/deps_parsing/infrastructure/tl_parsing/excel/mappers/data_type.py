import openpyxl as xl
from deps_tabular_layout.models import DataType

__all__ = ["DataTypeMapper"]


class DataTypeMapper:
    _type_mapping = {
        xl.cell.cell.TYPE_STRING: DataType.STRING,
        xl.cell.cell.TYPE_NUMERIC: DataType.NUMERIC,
        xl.cell.cell.TYPE_BOOL: DataType.BOOL,
        xl.cell.cell.TYPE_ERROR: DataType.ERROR,
        xl.cell.cell.TYPE_FORMULA: DataType.FORMULA,
    }

    @classmethod
    def from_cell(cls, cell: xl.cell.cell.Cell) -> DataType:
        return cls._type_mapping.get(cell.data_type, DataType.OTHER)
