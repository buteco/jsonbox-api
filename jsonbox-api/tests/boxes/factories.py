import factory

from apps.boxes.models import Box


class BoxFactory(factory.DjangoModelFactory):
    class Meta:
        model = Box

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        return manager.create_for_username(*args, **kwargs)
