import pandas as pd
from openpyxl.worksheet.worksheet import Worksheet

from ...table_reference import Point, TableReference
from ..tables_detector import IDetectTables
from .sub_grid import SubGrid

__all__ = ["LineBasedDetectionStrategy"]


class LineBasedDetectionStrategy(IDetectTables):
    """
    ### Overview ###
    The default strategy for Tables Detection in Excel files.
    The algorithm is based on splitting an Excel Sheet by completely empty columns and rows.

    Firstly, the page is split by empty columns, then each resulting piece(sub grid) is split by empty rows.
    Each resulting rectangle is considered a table if it is not empty.
    A list of table coordinates (top left corner - bottom right corner) is returned as an answer.

    ### Advantages ###
    Handles correctly any Excel Sheet, if there are no additional empty rows and columns inside the tables.
    Processes any page without information loss.

    ### Limitations ###
    If there are additional empty columns or rows inside the tables, the response shows split tables,
        which must be detected and merged later.
    """

    def detect_tables(self, sheet: Worksheet) -> list[TableReference]:
        sheet_df = self._convert_sheet_to_dataframe(sheet)

        if sheet_df.empty:
            return []

        detected_tables: list[SubGrid] = self._split_sheet(sheet_df, sheet)

        if not detected_tables:
            # we treat the whole sheet as a table if we hadn't split the sheet.
            detected_tables = [self._treat_whole_sheet_as_table(sheet_df)]

        return self._convert_into_table_references(detected_tables)

    def _convert_sheet_to_dataframe(self, sheet: Worksheet) -> pd.DataFrame:
        rows: list[tuple] = list(sheet.iter_rows(values_only=True))

        column_names: list[str] = [
            str(column_name[0]).split(".")[-1].replace("1>", "") for column_name in sheet.columns
        ]

        sheet_df = pd.DataFrame(rows, columns=column_names)

        return self._mask_dataframe(sheet_df)

    def _split_sheet(self, sheet_dataframe: pd.DataFrame, sheet: Worksheet) -> list[SubGrid]:
        """
        This function splits sheet by zero columns and zero rows
        """
        split_data_by_columns: list[SubGrid] = self._split_dataframe_by_zero_columns(sheet_dataframe)
        split_data_by_columns_and_rows: list[SubGrid] = []

        for grid in split_data_by_columns:
            split_data_by_columns_and_rows.extend(
                self._split_dataframe_by_zeros_rows(
                    grid_data=grid.data,
                    grid_column_borders=grid.column_border,
                    sheet=sheet,
                ),
            )

        return self._postprocess_detected_grids(split_data_by_columns_and_rows)

    def _split_dataframe_by_zeros_rows(
        self,
        grid_data: pd.DataFrame,
        grid_column_borders: tuple[int, int],
        sheet: Worksheet,
    ) -> list[SubGrid]:
        """
        This function splits data frame into parts by zero rows
        """

        zero_row_indexes: list[int] = [i for i, row in grid_data.iterrows() if row.eq(0).all()]  # type: ignore

        # we have to add first and last rows of the grid, because we treat them as a delimiter as well
        indexes: list[int] = [-1] + zero_row_indexes + [len(grid_data)]
        indexes = self._filter_rows_merged_cells(indexes, sheet)

        split_sub_grids: list[SubGrid] = []

        for i in range(len(indexes) - 1):
            if indexes[i + 1] > indexes[i] + 1:
                table_border_row_indexes: tuple[int, int] = indexes[i] + 1, indexes[i + 1]
                split_sub_grids.append(
                    SubGrid(
                        data=grid_data.iloc[indexes[i] + 1 : indexes[i + 1]].reset_index(drop=True),
                        column_border=grid_column_borders,
                        row_border=table_border_row_indexes,
                    ),
                )

        return split_sub_grids

    def _split_dataframe_by_zero_columns(self, df: pd.DataFrame) -> list[SubGrid]:
        """
        This function splits data frame into parts by zero columns
        """

        # Identify columns that are entirely zero
        zero_columns_names: list[str] = [column_series for column_series in df.columns if df[column_series].eq(0).all()]

        # indexes of zero columns for division points
        indexes: list[int] = [df.columns.get_loc(name) for name in zero_columns_names]
        indexes = indexes + [len(df.columns)]

        # Collecting each segment between zero-filled columns
        split_sub_grids: list[SubGrid] = []

        segment_start_index: int = 0
        for zero_column_index in indexes:
            segment_columns = df.columns[segment_start_index:zero_column_index]

            if segment_columns.any():
                split_sub_grids.append(
                    SubGrid(
                        data=df[segment_columns],
                        column_border=(segment_start_index, zero_column_index),
                        row_border=(0, len(df) - 1),
                    ),
                )

            segment_start_index = zero_column_index + 1

        return split_sub_grids

    def _filter_rows_merged_cells(self, zero_rows_indexes: list[int], sheet: Worksheet) -> list[int]:
        """
        If even one cell from the empty row is merged with a cell from the nonempty row,
        we delete the empty row from the delimiters list
        """
        filtered_rows: list[int] = []
        merged_rows: list[int] = self._get_merged_rows(sheet)

        for row_index in zero_rows_indexes:
            # we need `+1`, because openpyxl indexes start from 1 for merged_rows
            if row_index + 1 not in merged_rows:
                if self._is_following_row(
                    target_row_index=row_index,
                    zero_rows_indexes=zero_rows_indexes,
                ):
                    filtered_rows.pop()
                    filtered_rows.append(row_index)
                else:
                    filtered_rows.append(row_index)

        return filtered_rows

    def _get_merged_rows(self, sheet: Worksheet) -> list[int]:
        """
        From the list of all merged cells, we take only cells merged vertically
        and return every cell from the merged range
        """
        merged_rows: list[int] = []

        for cells in sheet.merged_cells:
            if cells.left[0][1] == cells.right[0][1]:
                merged_rows.extend([row[0] for row in cells.left])

        return merged_rows

    def _is_following_row(self, target_row_index: int, zero_rows_indexes: list[int]) -> bool:
        """
        This function checks whether target row is going right after the zero_rows_indexes last element
        """
        if not zero_rows_indexes:
            return False

        return target_row_index - zero_rows_indexes[-1] == 1

    def _find_empty_rows_indexes(self, df: pd.DataFrame) -> list[int]:
        """
        This function returns list of empty rows indexes
        """
        rows_all_zeros: pd.DataFrame = df.eq(0).all(axis=1)
        return list(rows_all_zeros[rows_all_zeros].index)

    def _mask_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This function fills every empty cell by 0 and every nonempty cell by 1
        """
        return df.notna().astype(int)

    def _postprocess_detected_grids(self, grids: list[SubGrid]) -> list[SubGrid]:
        """
        Postprocessing includes two actions:
        1. Removing completely empty grids;
        2. Truncating empty columns of other grids;
        """
        post_processed_grids: list[SubGrid] = []

        for grid in grids:
            if grid.data.eq(0).all().all():
                continue

            grid.truncate_empty_columns()

            post_processed_grids.append(grid)

        return post_processed_grids

    def _convert_into_table_references(self, grids: list[SubGrid]) -> list[TableReference]:
        """
        This function deletes empty tables and converts others to TableReference format
        """
        return [TableReference(self._table_placement(grid)) for grid in grids]

    def _table_placement(self, grid: SubGrid) -> tuple[Point, Point]:
        left_top = Point(
            row=grid.row_border[0],
            column=grid.column_border[0],
        )
        right_bottom = Point(
            row=grid.row_border[1] - 1,  # we are minusing 1 because indexation starts from 0
            column=grid.column_border[1] - 1,
        )

        return left_top, right_bottom

    def _treat_whole_sheet_as_table(self, sheet: pd.DataFrame) -> SubGrid:
        return SubGrid(
            data=sheet,
            column_border=(0, len(sheet.columns)),
            row_border=(sheet.index[0], sheet.index[-1]),
        )
