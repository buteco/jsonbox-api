import uuid

from django.db import models
from django_mysql.models import JSONField

from apps.boxes.models import Box


class Json(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, help_text="a uuid identification"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, help_text="creation date")
    updated_at = models.DateTimeField(auto_now=True, db_index=True, help_text="last update date")

    box = models.ForeignKey(
        Box, related_name="+", on_delete=models.CASCADE, help_text="the box that owns this object"
    )
    data = JSONField(help_text="the json document")

    class Meta:
        ordering = ("-created_at",)
