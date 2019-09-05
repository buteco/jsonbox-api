from rest_framework import filters
from rest_framework.serializers import ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework_jsonmask.views import OptimizedQuerySetMixin

from .models import Json
from .serializers import JsonSerializer
from apps.boxes.models import Box


class JsonDataFilter(filters.BaseFilterBackend):
    """
    Simple filter to query Json model using a custom notation.
    Querystrings are expected to be formatted as "search=key1:value1,key2:value".

    Those pairs of keys and values should exist in the JsonField of the related model,
    but not all fields are required in order to perform the filtering.

    Filter limitations:
        - Should use ":" to split key and value to be matched
        - Match the top-level keys
        - Match only strings
        - Multiple pairs should be separated by ","
        - Multiple pairs are handled as "AND" constraints
        - Repeated keys are not handled (the last value found should be used)
    """

    def _build_filters(self, search_params):
        filters = {}
        for params in search_params.split(","):
            if ":" not in params:
                raise ValidationError('Search parameters should have pairs of "key:value"')

            key, value = params.split(":")
            key = key.strip()
            if not key.startswith("data__"):
                key = "data__{}".format(key)

            filters[key] = value.strip()

        return filters

    def filter_queryset(self, request, queryset, view):
        search_params = request.query_params.get("search")
        if not search_params:
            return queryset

        filters = self._build_filters(search_params)
        return queryset.filter(**filters)


class JsonViewSet(OptimizedQuerySetMixin, ModelViewSet):
    serializer_class = JsonSerializer
    filter_backends = (JsonDataFilter,)

    def get_queryset(self):
        user = self.request.user
        return Json.objects.filter(box__token=user.auth_token)

    def perform_create(self, serializer):
        box = Box.objects.get(token=self.request.user.auth_token)
        return serializer.save(box=box)
