import pytest

from apps.jsons.models import Json

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    "data", [{"key": "value"}, {"key": 1234}, {"key": ["val", "ue"]}, {"key": {"is": "nested"}}]
)
def test_create_json(box, data):
    js = Json.objects.create(box=box, data=data)

    assert js.data == data


def test_create_json_default(box):
    js = Json.objects.create(box=box)

    assert js.data == {}
