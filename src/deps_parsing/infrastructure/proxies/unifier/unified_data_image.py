from dataclasses import dataclass
from typing import Any, Optional

__all__ = ["UnifiedDataImage", "AppliedTransformation", "TransformationParameters"]


@dataclass
class TransformationParameters:
    args: tuple[Any, ...]
    kwargs: dict[str, Any]

    @classmethod
    def from_dict(cls, parameters: dict[str, Any]) -> "TransformationParameters":
        return cls(
            args=parameters["args"],
            kwargs=parameters["kwargs"],
        )


@dataclass
class AppliedTransformation:
    name: str
    parameters: TransformationParameters

    @classmethod
    def from_dict(cls, transformation: dict[str, Any]) -> "AppliedTransformation":
        return cls(
            name=transformation["name"],
            parameters=TransformationParameters.from_dict(transformation["parameters"]),
        )


@dataclass
class UnifiedDataImage:
    id: str
    page: int
    blob_name: str
    width: int
    height: int
    applied_transformation: Optional[AppliedTransformation] = None
    original_image_id: Optional[str] = None

    @classmethod
    def from_dict(cls, image: dict[str, Any]) -> "UnifiedDataImage":
        applied_transformation = (
            None
            if image.get("appliedTransformation") is None
            else AppliedTransformation.from_dict(image["appliedTransformation"])
        )
        return cls(
            id=image["id"],
            page=image["page"],
            blob_name=image["blobName"],
            width=image["width"],
            height=image["height"],
            applied_transformation=applied_transformation,
            original_image_id=image.get("originalImageId"),
        )
