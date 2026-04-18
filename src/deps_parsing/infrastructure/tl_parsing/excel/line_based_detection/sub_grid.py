from dataclasses import dataclass

import pandas as pd

__all__ = ["SubGrid"]


@dataclass
class SubGrid:
    """
    This object represents the sub part of the Excel Sheet split by empty rows/columns.
    """

    data: pd.DataFrame
    column_border: tuple[int, int]
    row_border: tuple[int, int]

    def truncate_empty_columns(self) -> None:
        """
        Removing the completely empty columns from the left and right sides of the subgrid.
        We are looking for a columns with at least one non-zero value and then truncate the subgrid to these columns.
        """
        non_zero_columns = self.data.columns[self.data.ne(0).any()]

        left_non_empty_column = non_zero_columns[0]
        right_non_empty_column = non_zero_columns[-1]

        self._adjust_column_borders(new_left_column=left_non_empty_column, new_right_column=right_non_empty_column)
        self.data = self.data.loc[:, left_non_empty_column:right_non_empty_column]

    def _adjust_column_borders(self, new_left_column: str, new_right_column: str) -> None:
        new_left_idx: int = self.data.columns.get_loc(new_left_column)
        new_right_idx: int = self.data.columns.get_loc(new_right_column)

        shift_left: int = new_left_idx - self.data.columns.get_loc(self.data.columns[0])
        shift_right: int = new_right_idx - self.data.columns.get_loc(self.data.columns[-1])

        self.column_border = (self.column_border[0] + shift_left, self.column_border[1] + shift_right)
