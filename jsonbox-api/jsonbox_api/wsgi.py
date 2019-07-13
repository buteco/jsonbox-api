#!/usr/bin/env python
import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

PROJECT_PACKAGE = "jsonbox_api"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(PROJECT_PACKAGE))
_application = get_wsgi_application()

application = WhiteNoise(_application)
