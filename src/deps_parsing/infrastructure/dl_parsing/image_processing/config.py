from typing import Optional

from pydantic import Field, ValidationInfo, field_validator
from pydantic_settings import BaseSettings

__all__ = ["ImageAnnotationSettings"]

_DEFAULT_TEMPERATURE = 0.3
_DEFAULT_GROUPING_FACTOR = 2
_DEFAULT_PARALLELISM_FACTOR = 3
_DEFAULT_CUSTOM_INSTRUCTIONS = """\
You are an expert technical writer and visual content analyst. Your job is to analyze visual elements extracted from documents (e.g., diagrams, images, charts) and generate metadata that optimizes them for semantic search in a Retrieval-Augmented Generation (RAG) system.

Your outputs must be:

- Descriptive, accurate, and self-contained
- Optimized for search relevance
- Neutral in tone and professional in language
- Avoid vague terms like “image” or “picture”
- Use domain-specific terminology if context is available

Focus on what the visual conveys: structure, entities, data trends, relationships, and any key labels or legends.\
"""
_DEFAULT_TITLE_INSTRUCTIONS = """\
Given the following image content extracted from document, generate a concise and self-contained title for the visual. Avoid vague terms like "Image" or "Picture". Use domain-specific language when possible.

Instructions:
- Keep the title under 10 words
- Capture the most distinctive concept, object, or relationship shown
- Be specific enough to differentiate it from similar visuals

Respond only with the generated title.\
"""
_DEFAULT_DESCRIPTION_INSTRUCTIONS = """\
Given the following image content extracted from document, generate a detailed description to support semantic search in a RAG system.

Instructions:
- Describe what the image shows as if the reader cannot see it
- Focus on informative elements: structure, objects, flow, labels, connections, entities
- Mention visible text, orientation, relationships, data trends, and notable visual features
- Avoid interpretation unless context makes it obvious
- Use domain-specific vocabulary

Respond only with the generated description.\
"""


class ImageAnnotationSettings(BaseSettings):
    annotation_llm: Optional[str] = Field(
        default=None,
        validation_alias="IMG_ANNOTATION_LLM",
        description="LLM reference for AI Fusion to be used for image annotation. Must be blob-based model, error otherwise.",
    )
    title_prompt: str = Field(
        default=_DEFAULT_TITLE_INSTRUCTIONS,
        validation_alias="IMG_ANNOTATION_TITLE_PROMPT",
    )
    description_prompt: str = Field(
        default=_DEFAULT_DESCRIPTION_INSTRUCTIONS,
        validation_alias="IMG_ANNOTATION_DESCRIPTION_PROMPT",
    )
    temperature: float = Field(
        default=_DEFAULT_TEMPERATURE,
        validation_alias="IMG_ANNOTATION_TEMPERATURE",
    )
    grouping_factor: int = Field(
        default=_DEFAULT_GROUPING_FACTOR,
        validation_alias="IMG_ANNOTATION_GROUPING_FACTOR",
    )
    custom_instructions: str = Field(
        default=_DEFAULT_CUSTOM_INSTRUCTIONS,
        validation_alias="IMG_ANNOTATION_CUSTOM_INSTRUCTIONS",
    )
    parallelism_factor: int = Field(
        default=_DEFAULT_PARALLELISM_FACTOR,
        validation_alias="IMG_ANNOTATION_PARALLELISM_FACTOR",
        description="Number of parallel requests to be sent to the AI Fusion for image annotation.",
    )

    width_pixels_threshold: int | None = Field(
        default=None,
        validation_alias="IMG_ANNOTATION_WIDTH_PIXELS_THRESHOLD",
        gt=0,
    )
    height_pixels_threshold: int | None = Field(
        default=None,
        validation_alias="IMG_ANNOTATION_HEIGHT_PIXELS_THRESHOLD",
        gt=0,
    )
    image_size_bytes_threshold: int | None = Field(
        default=None,
        validation_alias="IMG_ANNOTATION_SIZE_BYTES_THRESHOLD",
        gt=0,
    )

    @field_validator(
        "title_prompt",
        "description_prompt",
        "custom_instructions",
        "width_pixels_threshold",
        "height_pixels_threshold",
        "image_size_bytes_threshold",
        mode="before",
    )
    @classmethod
    def fill_defaults(cls, value: str | int | None, info: ValidationInfo) -> str | int | None:
        if not value:
            if info.field_name == "title_prompt":
                return _DEFAULT_TITLE_INSTRUCTIONS
            if info.field_name == "description_prompt":
                return _DEFAULT_DESCRIPTION_INSTRUCTIONS
            if info.field_name == "custom_instructions":
                return _DEFAULT_CUSTOM_INSTRUCTIONS
            return None

        return value
