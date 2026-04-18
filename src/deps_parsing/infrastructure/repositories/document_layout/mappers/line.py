from deps_document_layout.model import (
    Barcode,
    Formula,
    Line,
    RawBarcode,
    RawFormula,
    RawLine,
    RawSelectionMark,
    RawSignature,
    SelectionMark,
    Signature,
)

from .base_element import BaseLineElementMapper
from .polygon import PolygonMapper
from .word import WordMapper

__all__ = ["LineMapper"]


class LineMapper:
    @classmethod
    def to_dict(cls, line: Line) -> RawLine:
        return {
            "order": line.order,
            "content": line.content,
            "confidence": line.confidence,
            "polygon": PolygonMapper.to_dict(line.polygon),
            "words": [WordMapper.to_dict(word) for word in line.words],
            "selection_marks": [cls._selection_mark_to_dict(selection_mark) for selection_mark in line.selection_marks],
            "barcodes": [cls._barcode_to_dict(barcode) for barcode in line.barcodes],
            "formulas": [cls._formula_to_dict(formula) for formula in line.formulas],
            "signatures": [cls._signture_to_dict(signature) for signature in line.signatures],
        }

    @classmethod
    def from_dict(cls, line: RawLine) -> Line:
        return Line(
            order=line["order"],
            content=line["content"],
            confidence=line["confidence"],
            polygon=PolygonMapper.from_dict(line["polygon"]),
            words=tuple(WordMapper.from_dict(word) for word in line["words"]),
            selection_marks=tuple(
                cls._selection_mark_from_dict(selection_mark) for selection_mark in line["selection_marks"]
            ),
            barcodes=tuple(cls._barcode_from_dict(barcode) for barcode in line["barcodes"]),
            formulas=tuple(cls._formula_from_dict(formula) for formula in line["formulas"]),
            signatures=tuple(cls._signature_from_dict(signature) for signature in line["signatures"]),
        )

    @classmethod
    def _selection_mark_to_dict(cls, selection_mark: SelectionMark) -> RawSelectionMark:
        return {
            "state": selection_mark.state,
            **BaseLineElementMapper.to_dict(selection_mark),
        }

    @classmethod
    def _selection_mark_from_dict(cls, selection_mark: RawSelectionMark) -> SelectionMark:
        return SelectionMark(
            state=selection_mark["state"],
            **BaseLineElementMapper.from_dict(selection_mark),
        )

    @classmethod
    def _barcode_to_dict(cls, barcode: Barcode) -> RawBarcode:
        return {
            "value": barcode.value,
            "kind": barcode.kind,
            **BaseLineElementMapper.to_dict(barcode),
        }

    @classmethod
    def _barcode_from_dict(cls, barcode: RawBarcode) -> Barcode:
        return Barcode(
            value=barcode["value"],
            kind=barcode["kind"],
            **BaseLineElementMapper.from_dict(barcode),
        )

    @classmethod
    def _formula_to_dict(cls, formula: Formula) -> RawFormula:
        return {
            "value": formula.value,
            "kind": formula.kind,
            **BaseLineElementMapper.to_dict(formula),
        }

    @classmethod
    def _formula_from_dict(cls, formula: RawFormula) -> Formula:
        return Formula(
            value=formula["value"],
            kind=formula["kind"],
            **BaseLineElementMapper.from_dict(formula),
        )

    @classmethod
    def _signture_to_dict(cls, signature: Signature) -> RawSignature:
        return {
            "value": signature.value,
            **BaseLineElementMapper.to_dict(signature),
        }

    @classmethod
    def _signature_from_dict(cls, signature: RawSignature) -> Signature:
        return Signature(
            value=signature["value"],
            **BaseLineElementMapper.from_dict(signature),
        )
