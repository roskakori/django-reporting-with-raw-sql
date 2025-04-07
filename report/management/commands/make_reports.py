# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
from django.core.management.base import BaseCommand

from report.reports import clear_reports, make_reports


class Command(BaseCommand):
    help = "(Re-)Create report related schema and views"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            "-C",
            action="store_true",
            help="remove any possibly existing reports first",
        )

    def handle(self, *_args, **options):
        has_to_prune = options["clear"]
        if has_to_prune:
            clear_reports(self.stdout)
        make_reports(self.stdout)
        self.stdout.write(self.style.SUCCESS("Successfully (re-)created all report views."))
