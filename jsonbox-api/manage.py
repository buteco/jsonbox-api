#!/usr/bin/env python
import os
import sys

PROJECT_PACKAGE = "jsonbox_api"

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "{}.settings".format(PROJECT_PACKAGE))
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
