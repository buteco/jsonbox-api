import pytest
from rest_framework.test import APIClient

from apps.boxes.models import Box


@pytest.fixture
def box():
    box = Box.objects.create_for_username("bobox", "bobox")
    box.save()
    return box


@pytest.fixture
def box_secondary():
    box = Box.objects.create_for_username("bombox", "bombox")
    box.save()
    return box


@pytest.fixture
def client_api_anon():
    return APIClient()


@pytest.fixture
def client_api(box):
    token = box.token.key
    client = APIClient(HTTP_AUTHORIZATION="Token {}".format(token))
    return client


@pytest.fixture
def client_api_secondary(box_secondary):
    token = box_secondary.token.key
    client = APIClient(HTTP_AUTHORIZATION="Token {}".format(token))
    return client
