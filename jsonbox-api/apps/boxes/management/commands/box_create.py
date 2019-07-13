from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

from apps.boxes.models import Box


class Command(BaseCommand):
    help = "Create boxes"

    def add_arguments(self, parser):
        parser.add_argument("name", action="store", type=str, help="the box name (slug)")

    def handle(self, *args, **options):
        name = slugify(options["name"].strip())
        boxes = Box.objects.filter(name=name)
        if boxes.count() > 0:
            raise CommandError('Box "{}" already exists!'.format(name))

        box = Box.objects.create_for_username(box_name=name, username=name)
        box.save()

        msg = "Box: {} / Token: {}".format(box.name, box.token.key)
        self.stdout.write(self.style.SUCCESS(msg))
