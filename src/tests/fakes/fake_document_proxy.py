__all__ = ["FakeDocumentProxy"]


class FakeDocumentProxy:
    def __init__(self) -> None:
        self.mocked_file: bytes = b""

    def get_document_files(self, *args, **kwargs) -> bytes:
        return self.mocked_file

    def set_mocked_file(self, file: bytes) -> None:
        self.mocked_file = file
