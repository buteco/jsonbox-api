from io import StringIO

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from apps.boxes.models import Box

pytestmark = pytest.mark.django_db


def test_box_create():
    stdout = StringIO()
    call_command("box_create", "box name", stdout=stdout)
    output = stdout.getvalue()

    assert Box.objects.filter(name="box-name").exists()
    box = Box.objects.get(name="box-name")

    assert box.name in output
    assert box.token.key in output


def test_box_create_already_exists(box):
    with pytest.raises(CommandError) as exc:
        call_command("box_create", box.name)

    assert "already exists" in str(exc)


def test_box_list(box):
    stdout = StringIO()
    call_command("box_list", stdout=stdout)
    output = stdout.getvalue()

    assert box.name in output
    assert box.token.key in output
