from deps_document_layout.model import LineBuilder, ParagraphBuilder, Point
from docx.shared import Pt
from docx.text.run import Run as DocxRun

__all__ = ["DOCXElementParser"]


class DOCXElementParser:
    DEFAULT_CONFIDENCE = 1.0
    POLYGON = (Point(x=0.0, y=0.0),)

    def _add_word_to_line(self, builder: LineBuilder, word_data: DocxRun) -> LineBuilder:
        return (
            builder.with_word()
            .with_content(word_data.text.strip())
            .with_confidence(self.DEFAULT_CONFIDENCE)
            .with_polygon(self.POLYGON)
            .with_style(
                color="#{:02x}{:02x}{:02x}".format(*word_data.font.color.rgb) if word_data.font.color.rgb else None,
                bold=bool(word_data.bold),
                italic=bool(word_data.italic),
                font_type=word_data.font.name,
                font_size=str(word_data.font.size) + "pt"  # noqa: WPS336
                if isinstance(word_data.font.size, Pt)
                else str(word_data.font.size),
                underlined=bool(word_data.underline),
                strikeout=bool(word_data.font.strike),
                subscript=bool(word_data.font.subscript),
                superscript=bool(word_data.font.superscript),
                smallcaps=bool(word_data.font.small_caps),
            )
        )

    def _add_paragraph_and_line(
        self,
        builder: ParagraphBuilder,
        content: str,
    ) -> LineBuilder:
        return (
            builder.with_confidence(self.DEFAULT_CONFIDENCE)
            .with_content(content)
            .with_polygon(self.POLYGON)
            .with_line()
            .with_confidence(self.DEFAULT_CONFIDENCE)
            .with_polygon(self.POLYGON)
            .with_content(content)
        )
