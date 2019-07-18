import pytest
from rest_framework.test import APIClient

from .boxes.factories import BoxFactory


@pytest.fixture
def box():
    return BoxFactory(box_name="bobox", username="bobox")


@pytest.fixture
def box_secondary():
    return BoxFactory(box_name="bombox", username="bombox")


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
