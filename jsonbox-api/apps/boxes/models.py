import uuid

from django.db import models
from rest_framework.authtoken.models import Token

from .managers import BoxManager


class Box(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    name = models.SlugField(max_length=32, unique=True)
    token = models.ForeignKey(Token, related_name="+", on_delete=models.CASCADE)

    objects = BoxManager()

    class Meta:
        ordering = ("-created_at",)
