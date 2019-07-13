import uuid

import django.db.models.deletion
import django_mysql.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("boxes", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Json",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        help_text="a uuid identification",
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, help_text="creation date"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, help_text="last update date"
                    ),
                ),
                (
                    "data",
                    django_mysql.models.JSONField(default=dict, help_text="the json document"),
                ),
                (
                    "box",
                    models.ForeignKey(
                        help_text="the box that owns this object",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="+",
                        to="boxes.Box",
                    ),
                ),
            ],
            options={"ordering": ("-created_at",)},
        )
    ]
