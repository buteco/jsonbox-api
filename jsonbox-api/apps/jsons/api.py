from rest_framework.viewsets import ModelViewSet
from rest_framework_jsonmask.views import OptimizedQuerySetMixin

from .models import Json
from .serializers import JsonSerializer
from apps.boxes.models import Box


class JsonViewSet(OptimizedQuerySetMixin, ModelViewSet):
    serializer_class = JsonSerializer

    def get_queryset(self):
        user = self.request.user
        return Json.objects.filter(box__token=user.auth_token)

    def perform_create(self, serializer):
        box = Box.objects.get(token=self.request.user.auth_token)
        return serializer.save(box=box)
