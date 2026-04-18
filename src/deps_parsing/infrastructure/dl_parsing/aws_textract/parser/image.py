from typing import cast

from deps_document_layout.model import PageBuilder

from ...image_processing import ParsedImage
from .base_page_element import PageElementParser


class ImageDataParser(PageElementParser):
    def add_image(self, builder: PageBuilder, image: ParsedImage) -> PageBuilder:
        builder = (
            builder.with_image()
            .with_polygon(image.page_coordinates)
            .with_title(image.title)
            .with_file_path(image.filepath)
            .with_description(image.description)
        )

        return cast(PageBuilder, builder)
