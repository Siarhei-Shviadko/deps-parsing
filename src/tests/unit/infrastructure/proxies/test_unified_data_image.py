from deps_parsing.infrastructure.proxies import (
    AppliedTransformation,
    TransformationParameters,
    UnifiedDataImage,
)
from tests.data import unified_image_page1


def test_from_dict__unified_data_image__ok():
    image = UnifiedDataImage.from_dict(unified_image_page1)

    assert image.id == unified_image_page1["id"]
    assert image.page == unified_image_page1["page"]
    assert image.blob_name == unified_image_page1["blobName"]
    assert image.width == unified_image_page1["width"]
    assert image.height == unified_image_page1["height"]
    assert image.applied_transformation == AppliedTransformation.from_dict(unified_image_page1["appliedTransformation"])
    assert image.original_image_id == unified_image_page1["originalImageId"]


def test_from_dict__applied_transformation__ok():
    transformation_dict = unified_image_page1["appliedTransformation"]
    transformation = AppliedTransformation.from_dict(transformation_dict)

    assert transformation.name == transformation_dict["name"]
    assert transformation.parameters == TransformationParameters.from_dict(transformation_dict["parameters"])


def test_from_dict__transformation_parameters__ok():
    parameters_dict = unified_image_page1["appliedTransformation"]["parameters"]
    parameters = TransformationParameters.from_dict(parameters_dict)

    assert parameters.args == parameters_dict["args"]
    assert parameters.kwargs == parameters_dict["kwargs"]
