import pytest
from django.db import IntegrityError

from apps.boxes.models import Box

pytestmark = pytest.mark.django_db


def test_create_box():
    box = Box.objects.create_for_username("box sample", "boxuser")
    assert box
    assert box.name == "box-sample"
    assert box.token


def test_duplicate_box(box):
    with pytest.raises(IntegrityError):
        Box.objects.create_for_username(box.name, box.name)
