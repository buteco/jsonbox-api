import pytest

from .factories import JsonFactory

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "data", [{"key": "value"}, {"key": 1234}, {"key": ["val", "ue"]}, {"key": {"is": "nested"}}]
)
def test_create_json(data):
    js = JsonFactory(data=data)

    assert js.data == data


def test_create_json_default(box):
    js = JsonFactory(box=box)

    assert js.data == {}
