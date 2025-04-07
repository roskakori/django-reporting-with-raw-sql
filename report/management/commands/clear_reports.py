# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
from django.core.management.base import BaseCommand

from report.reports import clear_reports


class Command(BaseCommand):
    help = 'Remove all report related SQL components (but preserve the "report" schema)'

    def handle(self, *args, **options):
        clear_reports(self.stdout)
        self.stdout.write(self.style.SUCCESS("Successfully removed all report related SQL components."))
