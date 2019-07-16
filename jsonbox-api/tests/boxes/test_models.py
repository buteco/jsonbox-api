import pytest
from django.db import IntegrityError

from .factories import BoxFactory

pytestmark = pytest.mark.django_db


def test_create_box():
    box = BoxFactory(box_name="box sample", username="boxuser")
    assert box
    assert box.name == "box-sample"
    assert box.token


def test_duplicate_box(box):
    with pytest.raises(IntegrityError):
        BoxFactory(box_name=box.name, username=box.name)
