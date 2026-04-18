__all__ = ["FakeFileProxy"]


class FakeFileProxy:
    def __init__(self) -> None:
        self.mocked_file: bytes = b""

    def get_file_content(self, *args, **kwargs) -> bytes:
        return self.mocked_file

    def set_mocked_file(self, file: bytes) -> None:
        self.mocked_file = file
