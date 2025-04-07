# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from minitrack.settings import DEFAULT_PASSWORD


class Command(BaseCommand):
    help = "Make demo data admin"

    def add_arguments(self, parser):
        parser.add_argument(
            "username",
            default="admin",
            nargs="?",
            metavar="USERNAME",
            help="Name of the admin user to create; default: %(default)s",
        )

    def handle(self, *_args, **options):
        username = options["username"]
        User.objects.create_superuser(username=username, password=DEFAULT_PASSWORD)
        self.stdout.write(self.style.SUCCESS(f"Successfully created admin user {username!r}."))
