import openpyxl as xl
from deps_tabular_layout.models import (
    AlignmentInput,
    BordersInput,
    FormatInput,
    StyleInput,
)

__all__ = ["FormatMapper"]


class FormatMapper:
    @classmethod
    def from_cell(cls, cell: xl.cell.cell.Cell) -> FormatInput:
        return FormatInput(
            style=cls._map_style(cell),
            borders=cls._map_borders(cell),
            alignment=cls._map_alignment(cell),
        )

    @classmethod
    def _map_style(cls, cell: xl.cell.cell.Cell) -> StyleInput:
        return StyleInput(
            background_color=str(cell.fill.bgColor.rgb) if cell.fill.bgColor is not None else None,
            color=str(cell.font.color.rgb) if cell.font.color is not None else None,
            hyperlink=cell.hyperlink is not None,
            bold=cell.font.bold,
            italic=cell.font.italic,
            font_name=cell.font.name,
            font_size=str(cell.font.size),
            underlined=cell.font.underline is not None,
            strikethrough=cell.font.strike,
        )

    @classmethod
    def _map_borders(cls, cell: xl.cell.cell.Cell) -> BordersInput:
        return BordersInput(
            top=cell.border.top.style,
            bottom=cell.border.bottom.style,
            left=cell.border.left.style,
            right=cell.border.right.style,
        )

    @classmethod
    def _map_alignment(cls, cell: xl.cell.cell.Cell) -> AlignmentInput:
        return AlignmentInput(
            vertical=cell.alignment.vertical,
            horizontal=cell.alignment.horizontal,
            rotation=cell.alignment.textRotation,
        )
