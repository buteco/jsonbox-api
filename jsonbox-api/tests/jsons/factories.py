import factory

from apps.jsons.models import Json
from tests.boxes.factories import BoxFactory


class JsonFactory(factory.django.DjangoModelFactory):
    box = factory.SubFactory(BoxFactory, box_name="testbox", username="testbox")

    class Meta:
        model = Json
