from fastapi import Query

from deps_parsing.domain.dtos import TabularLayoutFilter

__all__ = ["TabularLayoutFeaturesFilterFactory"]


class TabularLayoutFeaturesFilterFactory:
    @classmethod
    def make_filter(
        cls,
        tables: list[str] | None = Query(None),
        row_span: tuple[int, int] | None = Query(None, alias="rowSpan"),
        col_span: tuple[int, int] | None = Query(None, alias="colSpan"),
    ) -> TabularLayoutFilter:
        if row_span is not None and any(row_element < 0 for row_element in row_span):
            raise ValueError("Value must be greater than or equal to 0")

        if col_span is not None and any(col_element < 0 for col_element in col_span):
            raise ValueError("Value must be greater than or equal to 0")

        return TabularLayoutFilter(
            tables=tables,
            row_span=row_span,
            col_span=col_span,
        )
