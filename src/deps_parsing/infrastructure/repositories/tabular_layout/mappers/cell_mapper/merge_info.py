from deps_tabular_layout.models import MergeInfo

__all__ = ["MergeInfoMapper"]


class MergeInfoMapper:
    @staticmethod
    def to_dict(merge_info: MergeInfo) -> dict[str, int]:
        return {
            "column_span": merge_info.column_span,
            "row_span": merge_info.row_span,
        }

    @staticmethod
    def from_raw(raw_merge_info: dict[str, int]) -> MergeInfo:
        return MergeInfo(
            column_span=raw_merge_info["column_span"],
            row_span=raw_merge_info["row_span"],
        )
