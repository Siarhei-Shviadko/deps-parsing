from typing import Any

import pytest
from faker.proxy import Faker


@pytest.fixture
def update_paragraph_payload(faker: Faker, polygon_factory) -> dict[str, Any]:
    return {
        "lines": [
            {
                "content": faker.text(max_nb_chars=30),
                "order": 0,
                "polygon": [{"x": p.x, "y": p.y} for p in polygon_factory()],
            },
            {
                "content": faker.text(max_nb_chars=30),
                "order": 1,
                "polygon": [{"x": p.x, "y": p.y} for p in polygon_factory()],
            },
            {
                "content": faker.text(max_nb_chars=30),
                "order": 2,
                "polygon": [{"x": p.x, "y": p.y} for p in polygon_factory()],
            },
        ],
    }


@pytest.fixture
def update_image_payload(faker: Faker, polygon_factory) -> dict[str, Any]:
    return {
        "title": faker.text(max_nb_chars=30),
        "description": faker.text(max_nb_chars=100),
        "polygon": [{"x": p.x, "y": p.y} for p in polygon_factory()],
        "filepath": faker.file_path(depth=1, extension="jpg"),
    }


@pytest.fixture
def update_table_payload(faker: Faker) -> dict[str, Any]:
    return {
        "cells": [
            {
                "content": faker.text(max_nb_chars=30),
                "rowIndex": 0,
                "columnIndex": 0,
            },
            {
                "content": faker.text(max_nb_chars=30),
                "rowIndex": 0,
                "columnIndex": 1,
            },
            {
                "content": faker.text(max_nb_chars=30),
                "rowIndex": 0,
                "columnIndex": 2,
            },
        ],
    }


@pytest.fixture
def update_key_value_pair_payload(faker: "Faker", polygon_factory, paragraph_id, paragraph2_id) -> dict[str, Any]:
    return {
        "key": {
            "content": faker.text(max_nb_chars=15),
            "polygon": [{"x": p.x, "y": p.y} for p in polygon_factory()],
            "paragraphId": str(paragraph_id()),
        },
        "value": {
            "content": faker.text(max_nb_chars=15),
            "polygon": [{"x": p.x, "y": p.y} for p in polygon_factory()],
            "paragraphId": str(paragraph2_id()),
        },
    }
