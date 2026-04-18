from deps_document_layout.model import (
    Blurring,
    RawBlurring,
    RawTransformations,
    Thresholding,
    Transformations,
)

__all__ = ["TransformationsMapper"]


class TransformationsMapper:
    @classmethod
    def to_dict(cls, transformations: Transformations) -> RawTransformations:
        return {
            "blurring": cls._blurring_to_dict(transformations.blurring) if transformations.blurring else None,
            "grayscaling": transformations.grayscaling,
            "orientation": transformations.orientation,
            "angle": transformations.angle,
            "thresholding": cls._thresholding_to_dict(transformations.thresholding)
            if transformations.thresholding
            else None,
        }

    @classmethod
    def from_dict(cls, raw_transformations: RawTransformations) -> Transformations:
        return Transformations(
            blurring=cls._blurring_from_dict(raw_transformations["blurring"])
            if raw_transformations.get("blurring")
            else None,
            grayscaling=raw_transformations["grayscaling"],
            orientation=raw_transformations.get("orientation"),
            angle=raw_transformations.get("angle"),
            thresholding=cls._thresholding_from_dict(raw_transformations["thresholding"])
            if raw_transformations.get("thresholding")
            else None,
        )

    @classmethod
    def _blurring_to_dict(cls, blurring: Blurring) -> RawBlurring:
        return {
            "kernel": list(blurring.kernel),
            "sigma": blurring.sigma,
        }

    @classmethod
    def _blurring_from_dict(cls, blurring: RawBlurring) -> Blurring:
        return Blurring(
            kernel=tuple(blurring["kernel"]),
            sigma=blurring["sigma"],
        )

    @classmethod
    def _thresholding_to_dict(cls, thresholding: Thresholding) -> dict[str, int]:
        return {
            "low_value": thresholding.low_value,
            "high_value": thresholding.high_value,
            "flag": thresholding.flag,
        }

    @classmethod
    def _thresholding_from_dict(cls, thresloding: dict[str, int]) -> Thresholding:
        return Thresholding(
            low_value=thresloding["low_value"],
            high_value=thresloding["high_value"],
            flag=thresloding["flag"],
        )
