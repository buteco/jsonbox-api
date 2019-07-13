import json

from rest_framework import serializers
from rest_framework_jsonmask.serializers import FieldsListSerializerMixin
from rest_framework_jsonmask.utils import apply_json_mask_from_request

from .models import Json


class JsonSerializer(FieldsListSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Json
        fields = ("id", "data")
        extra_kwargs = {"data": {"required": True}}

    def validate_data(self, value):
        if not value:
            raise serializers.ValidationError("`data` should not be empty")

        if isinstance(value, dict):
            return value

        try:
            data = json.loads(value)
        except (json.decoder.JSONDecodeError, TypeError):
            raise serializers.ValidationError("invalid json object: `{!r}`".format(value))

        if not isinstance(data, dict):
            raise serializers.ValidationError("`data` should be an json object")

        return data

    def to_representation(self, obj):
        data = super().to_representation(obj)
        return apply_json_mask_from_request(data, self.context["request"])
