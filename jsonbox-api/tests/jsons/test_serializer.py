import pytest

from apps.jsons.serializers import JsonSerializer


@pytest.mark.parametrize(
    "data",
    ["{}", '{"key": "value"}', '{"key": 123}', '{"key": ["val", "ue"]}', '{"key": {"a": "b"}}'],
)
def test_json_serializer_validation_ok(data):
    ser = JsonSerializer(data={"data": data})
    assert ser.is_valid() is True


@pytest.mark.parametrize("data", ["", 1234, None, [], "1234", '[{"key": "value"}]'])
def test_json_serializer_validation_error(data):
    ser = JsonSerializer(data={"data": data})
    assert ser.is_valid() is False
