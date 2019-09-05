import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from .factories import JsonFactory

pytestmark = pytest.mark.django_db


@pytest.fixture
def sample_json(box):
    return JsonFactory(box=box, data={"key": "value", "lol": {"name": "hue", "age": 1}})


@pytest.mark.parametrize("method", ["get", "post", "put", "patch", "delete"])
def test_unauthorized(client_api_anon, method):
    url = reverse("jsons:jsons-list")
    response = getattr(client_api_anon, method)(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_jsons_list(client_api):
    url = reverse("jsons:jsons-list")
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 0
    assert data["next"] is None
    assert data["previous"] is None
    assert data["results"] == []


def test_get_jsons_list_simple(client_api, sample_json):
    url = reverse("jsons:jsons-list")
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0] == {"id": str(sample_json.id), "data": sample_json.data}


def test_get_jsons_with_jsonmask(client_api, sample_json):
    url = reverse("jsons:jsons-list") + "?fields=data(lol(name))"
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0] == {"data": {"lol": {"name": "hue"}}}


@pytest.mark.parametrize("search", ["key:value", "data__key:value"])
def test_get_jsons_filter_simple(client_api, sample_json, search):
    url = reverse("jsons:jsons-list") + "?search={}".format(search)
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == 1
    assert data["results"][0]["data"]["key"] == "value"


@pytest.mark.parametrize(
    "search,expected",
    [
        ("key:value", 2),
        ("lol:yolo", 1),
        ("lol:", 1),
        ("key:value,lol:yolo", 1),
        ("key:value,lol:", 1),
        ("key:,lol:yolo", 0),
        ("key:,lol:", 0),
    ],
)
def test_get_jsons_filter_by_multiple_keys(client_api, box, search, expected):
    JsonFactory(box=box, data={"key": "value", "lol": "yolo"})
    JsonFactory(box=box, data={"key": "value", "lol": ""})
    url = reverse("jsons:jsons-list") + "?search={}".format(search)
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["count"] == expected


@pytest.mark.parametrize("search", ["value", "some:value,other"])
def test_get_jsons_filter_with_invalid_search(client_api, search):
    url = reverse("jsons:jsons-list") + "?search={}".format(search)
    response = client_api.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_json_detail(client_api, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(sample_json.id)
    assert data["data"] == sample_json.data


def test_get_json_detail_from_other_box(client_api_secondary, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    response = client_api_secondary.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()
    assert "not found" in data["detail"].lower()


def test_get_json_detail_with_jsonmask(client_api, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id]) + "?fields=data(lol(age))"
    response = client_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data == {"data": {"lol": {"age": 1}}}


def test_delete_json(client_api, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    response = client_api.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_delete_json_from_other_box(client_api_secondary, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    response = client_api_secondary.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_patch_json(client_api, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    payload = {"data": {"other": "whatever"}}
    response = client_api.patch(url, data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == payload["data"]


@pytest.mark.parametrize("data", [{}, "", 123, None])
def test_patch_json_invalid(client_api, sample_json, data):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    payload = {"data": data}
    response = client_api.patch(url, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_patch_json_from_other_box(client_api_secondary, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    payload = {"data": {"other": "whatever"}}
    response = client_api_secondary.patch(url, data=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_put_json(client_api, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    payload = {"data": {"other": "whatever"}}
    response = client_api.put(url, data=payload)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"] == payload["data"]


@pytest.mark.parametrize("data", [{}, "", 123, None])
def test_put_json_invalid(client_api, sample_json, data):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    payload = {"data": data}
    response = client_api.put(url, data=payload)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_put_json_from_other_box(client_api_secondary, sample_json):
    url = reverse("jsons:jsons-detail", [sample_json.id])
    payload = {"data": {"other": "whatever"}}
    response = client_api_secondary.put(url, data=payload)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_post_json_empty(client_api):
    url = reverse("jsons:jsons-list")
    response = client_api.post(url, data={})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "is required" in response.json()["data"][0]


def test_post_json_invalid(client_api):
    url = reverse("jsons:jsons-list")
    response = client_api.post(url, data="abc")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "invalid" in response.json()["non_field_errors"][0].lower()


def test_post_json_simple(client_api):
    url = reverse("jsons:jsons-list")
    payload = {"data": {"key": "value"}}
    response = client_api.post(url, data=payload)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "id" in data
    assert data["data"] == payload["data"]


def test_post_json_complex(client_api):
    url = reverse("jsons:jsons-list")
    payload = {
        "data": {
            "key": "value",
            "foobar": {"nested": 1, "lalala": ["la", "la", "la"]},
            "alist": [3.14],
        }
    }
    response = client_api.post(url, data=payload)

    assert response.status_code == status.HTTP_201_CREATED
