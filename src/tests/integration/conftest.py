from uuid import uuid4

import pytest
from deps_tabular_layout.models import Cell, EntityId, TabularLayout

from deps_parsing.domain.interfaces import (
    ICellCommandRepository,
    ITabularLayoutCommandRepository,
    ITabularLayoutQueryRepository,
)
from deps_parsing.infrastructure.dl_parsing import BaseDepsOCREngine
from deps_parsing.infrastructure.repositories import (
    DocumentLayoutRepository,
    DocumentTypeRepository,
)
from tests.factories.tabular_layout import (
    CellFactory,
    PointFactory,
    SheetFactory,
    TableFactory,
    TabularLayoutFactory,
)

from .helper import TLQueryHelper


@pytest.fixture(autouse=True)
def session(containers):
    database = containers.datasources.postgres_datasource()
    connection = database.get_connection()

    class TrapForThreadLocalConnections:
        """
        This class is used instead of threading.local in Database, for allowing connection transactions management
        """

        connection = None

    TrapForThreadLocalConnections.connection = connection
    connection.begin()
    transaction = connection.begin_nested()
    database._registry = TrapForThreadLocalConnections
    try:
        yield
    finally:
        transaction.rollback()
    database.close()


@pytest.fixture
def document_layout_repository(repositories) -> DocumentLayoutRepository:
    return repositories.document_layout()


@pytest.fixture
def cell_command_repository(repositories) -> ICellCommandRepository:
    return repositories.cell_command()


@pytest.fixture
def tabular_layout_command_repository(repositories) -> ITabularLayoutCommandRepository:
    return repositories.tabular_layout_command()


@pytest.fixture
def tabular_layout_query_repository(repositories) -> ITabularLayoutQueryRepository:
    return repositories.tabular_layout_query()


@pytest.fixture
def document_type_repository(repositories) -> DocumentTypeRepository:
    return repositories.document_type()


@pytest.fixture
def test_saved_document_type(test_document_type, document_type_repository):
    document_type_repository.save(test_document_type)
    return test_document_type


@pytest.fixture
def deps_engine(engines) -> BaseDepsOCREngine:
    return engines.deps()


@pytest.fixture
def tesseract_engine(engines):
    return engines.tesseract()


@pytest.fixture
def easy_ocr_engine(engines):
    return engines.easy_ocr()


@pytest.fixture
def craft_tesseract_engine(engines):
    return engines.craft_tesseract()


@pytest.fixture
def paddle_ocr_engine(engines):
    return engines.paddle_ocr()


@pytest.fixture
def datasource(containers):
    return containers.datasources.postgres_datasource()


@pytest.fixture
def tl_query_helper(datasource) -> TLQueryHelper:
    return TLQueryHelper(datasource)


@pytest.fixture
def test_saved_tl_and_ordered_cells(
    tabular_layout_command_repository,
    cell_command_repository,
) -> tuple[TabularLayout, list[Cell]]:
    sheet_ids = [EntityId(uuid4().hex) for i in range(3)]
    tl = TabularLayoutFactory.create(
        sheets=[
            SheetFactory.create(id_=sheet_ids[i], tables=[TableFactory(sheet_id=sheet_ids[i]) for _ in range(2)])
            for i in range(3)
        ]
    )
    tabular_layout_command_repository.save(tl)
    all_cells = []
    for sheet in tl.sheets:
        for table in sheet.tables:
            cells = [
                CellFactory.create(table_id=table.id, relative_position=PointFactory(x=x, y=y))
                for y, x in ((0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2))
            ]
            cell_command_repository.save_batch(tl.id(), cells)
            all_cells.extend(cells)

    return tl, all_cells


@pytest.fixture
def test_saved_tl_with_ordered_cells(test_saved_tl_and_ordered_cells) -> TabularLayout:
    return test_saved_tl_and_ordered_cells[0]


@pytest.fixture
def test_saved_ordered_cells(test_saved_tl_and_ordered_cells) -> list[Cell]:
    return test_saved_tl_and_ordered_cells[1]
