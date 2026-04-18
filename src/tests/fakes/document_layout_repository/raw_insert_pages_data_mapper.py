from collections import defaultdict

from deps_document_layout.model import Page, RawInsertPagesData, RawPageFromDB

from deps_parsing.infrastructure.repositories.document_layout.mappers import PageMapper

__all__ = ["RawInsertPagesDataMapper"]


class RawInsertPagesDataMapper:
    def __init__(self, raw_data: RawInsertPagesData) -> None:
        self.raw_pages = raw_data["pages"]
        self.mapped_images = defaultdict(list)
        self.mapped_paragraphs = defaultdict(list)
        self.mapped_tables = defaultdict(list)
        self.mapped_key_value_pairs = defaultdict(list)
        self.pages: list[Page] = []

        for image in raw_data["images"]:
            self.mapped_images[(image["page_id"], image["parsing_type"])].append(image)
        for paragraph in raw_data["paragraphs"]:
            self.mapped_paragraphs[(paragraph["page_id"], paragraph["parsing_type"])].append(paragraph)
        for table in raw_data["tables"]:
            self.mapped_tables[(table["page_id"], table["parsing_type"])].append(table)
        for kvp in raw_data["key_value_pairs"]:
            self.mapped_key_value_pairs[(kvp["page_id"], kvp["parsing_type"])].append(kvp)

    def to_models(self) -> list[Page]:
        for page in self.raw_pages:
            page_id = page["id"]
            parsing_type = page["parsing_type"]

            self.pages.append(
                PageMapper.from_dict(
                    RawPageFromDB(
                        id=page["id"],
                        page_number=page["page_number"],
                        parsing_type=page["parsing_type"],
                        dimension=page["dimension"],
                        languages=page["languages"],
                        file_path=page["file_path"],
                        transformations=page["transformations"],
                        document_layout_id=page["document_layout_id"],
                        groups=page["groups"],
                        images=self.mapped_images[(page_id, parsing_type)],
                        paragraphs=self.mapped_paragraphs[(page_id, parsing_type)],
                        tables=self.mapped_tables[(page_id, parsing_type)],
                        key_value_pairs=self.mapped_key_value_pairs[(page_id, parsing_type)],
                    ),
                ),
            )

        return self.pages
