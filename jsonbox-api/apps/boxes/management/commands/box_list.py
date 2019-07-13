from django.core.management.base import BaseCommand

from apps.boxes.models import Box


class Command(BaseCommand):
    help = "List boxes"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Box\tToken"))
        for box in Box.objects.all():
            msg = "{}\t{}".format(box.name, box.token.key)
            self.stdout.write(self.style.SUCCESS(msg))
