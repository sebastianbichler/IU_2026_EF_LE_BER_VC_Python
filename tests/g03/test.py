import pytest
from itertools import count

from src.student_projects.g03.src.main import process_eager, process_lazy



@pytest.fixture
def sample_data():
    return [
        {"bed_id": 1, "moisture": 20.0},   # low -> included
        {"bed_id": 2, "moisture": 40.0},   # ok -> excluded
        {"bed_id": 3, "moisture": 90.0},   # high -> included
    ]


def test_process_eager_filters(sample_data):
    result = process_eager(sample_data)

    assert len(result) == 2
    assert {r["bed_id"] for r in result} == {1, 3}


def test_process_eager_irrigation_value(sample_data):
    result = process_eager(sample_data)

    r = next(x for x in result if x["bed_id"] == 1)
    assert r["irrigation_need"] == 80.0


def test_process_lazy_equals_eager(sample_data):
    eager = process_eager(sample_data)
    lazy = process_lazy(iter(sample_data))

    assert eager == lazy


def test_process_lazy_max_items(sample_data):
    result = process_lazy(iter(sample_data), max_items=1)
    assert len(result) == 1
