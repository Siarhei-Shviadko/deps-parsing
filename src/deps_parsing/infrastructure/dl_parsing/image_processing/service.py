import io
import logging
import uuid
from concurrent.futures import Future, ThreadPoolExecutor
from contextvars import copy_context
from dataclasses import dataclass
from typing import Any, Callable

from deps_document_layout.model import Polygon
from deps_object_storage import ObjectStorage
from PIL import Image, ImageDraw

from deps_parsing.constants import DOCUMENT_LAYOUT_FOLDER
from deps_parsing.infrastructure.proxies import AIFusionProxy, RetrievedInsight

from .config import ImageAnnotationSettings
from .parsed_image import ParsedImage
from .preparsed_image import PreparsedImage

__all__ = ["OCRLayoutImageProcessingService"]

ImageBytes = bytes
_EMPTY, _FILLED = 0, 255


@dataclass
class ImageSize:
    width: int
    height: int
    bytes_size: int


def _run_with_user_context(executor: ThreadPoolExecutor, func: Callable, *args: Any, **kwargs: Any) -> Future:
    """This method allows us to share user context with threads so we can perform REST API calls"""
    context = copy_context()
    return executor.submit(lambda: context.run(func, *args, **kwargs))


class OCRLayoutImageProcessingService:
    _title_code: str = "title"
    _description_code: str = "description"

    def __init__(
        self,
        storage: ObjectStorage,
        image_recognizer: AIFusionProxy,
    ) -> None:
        self._storage = storage
        self._image_recognizer = image_recognizer
        self._config = ImageAnnotationSettings()

        self._logger = logging.getLogger(self.__class__.__name__)

    def process_preparsed_images(self, preparsed_images: list[PreparsedImage]) -> list[ParsedImage]:
        parsed_images: list[ParsedImage] = []

        with ThreadPoolExecutor(max_workers=self._config.parallelism_factor) as executor:
            futures: list[Future] = [
                _run_with_user_context(executor, self.process_preparsed_image, preparsed_image)
                for preparsed_image in preparsed_images
            ]

            for future in futures:
                try:
                    parsed_images.append(future.result())
                except Exception as ex:
                    self._logger.error(f"Error processing image `{ex.__class__.__name__}`: `{ex}`")

        return parsed_images

    def process_preparsed_image(self, preparsed_image: PreparsedImage) -> ParsedImage:
        raw_image, image_size = self._crop_image(preparsed_image.page_image, preparsed_image.polygon)

        saved_image_filepath = self._save_image(raw_image=raw_image, layout_id=preparsed_image.layout_id)

        parsed_image = ParsedImage(
            title=preparsed_image.layout_id,
            description="",
            filepath=saved_image_filepath,
            page_coordinates=preparsed_image.polygon,
        )

        if self.annotations_enabled(image_size):
            parsed_image = self.annotate_parsed_image(image=parsed_image)

        return parsed_image

    def annotations_enabled(self, image_size: ImageSize) -> bool:
        if not bool(self._config.annotation_llm):
            return False

        h_ok = not self._config.height_pixels_threshold or image_size.height >= self._config.height_pixels_threshold
        w_ok = not self._config.width_pixels_threshold or image_size.width >= self._config.width_pixels_threshold
        size_ok = (
            not self._config.image_size_bytes_threshold
            or image_size.bytes_size >= self._config.image_size_bytes_threshold
        )

        return h_ok and w_ok and size_ok

    def annotate_parsed_image(self, image: ParsedImage) -> ParsedImage:
        annotations_query = {
            self._title_code: self._config.title_prompt,
            self._description_code: self._config.description_prompt,
        }

        try:
            annotations = self._image_recognizer.retrieve_image_insights(
                llm_reference=self._config.annotation_llm,
                image_path=image.filepath,
                questions=annotations_query,
                temperature=self._config.temperature,
                grouping_factor=self._config.grouping_factor,
                custom_instructions=self._config.custom_instructions,
            )
        except Exception as ex:
            self._logger.error(f"Couldn't perform image recognition for `{image.filepath}`. Reason: `{ex}`")
            annotations = {}

        return self._update_parsed_image_with_annotations(image=image, annotations=annotations)

    def _crop_image(self, page_image: bytes, image_polygon: Polygon) -> tuple[ImageBytes, ImageSize]:
        with Image.open(io.BytesIO(page_image)) as img:
            img = img.convert("RGBA")
            width, height = img.size

            polygon_px: list[tuple[int, int]] = [
                (int(point.x * width), int(point.y * height)) for point in image_polygon
            ]

            mask = Image.new(mode="L", size=(width, height), color=_EMPTY)
            ImageDraw.Draw(mask).polygon(polygon_px, fill=_FILLED)

            result = Image.new(mode="RGBA", size=(width, height))
            result.paste(img, mask=mask)

            # Crop to bounding box of the polygon
            bbox = mask.getbbox()
            if bbox is not None:
                result = result.crop(bbox)

        with io.BytesIO() as output:
            result.save(output, format="PNG")
            image_bytes = output.getvalue()
            image_size = len(image_bytes)

            return output.getvalue(), ImageSize(width=result.size[0], height=result.size[1], bytes_size=image_size)

    def _save_image(self, raw_image: ImageBytes, layout_id: str) -> str:
        file_path = f"{DOCUMENT_LAYOUT_FOLDER}/{layout_id}/images/{uuid.uuid4().hex}.png"

        self._storage.upload(
            path=file_path,
            content=raw_image,
            replace_if_exists=True,
        )

        return file_path

    def _update_parsed_image_with_annotations(
        self,
        image: ParsedImage,
        annotations: dict[str, RetrievedInsight],
    ) -> ParsedImage:
        title_insight = annotations.get(self._title_code)
        if title_insight is None or title_insight["errorOccurred"]:
            title = "Annotation error occurred"
        else:
            title = title_insight["content"]

        description_insight = annotations.get(self._description_code)
        if description_insight is None:
            description = "Error occurred..."
        elif description_insight["errorOccurred"]:
            description = f"Error occurred: {description_insight['content']}"
        else:
            description = description_insight["content"]

        return image.with_updated_annotations(title=title, description=description)
