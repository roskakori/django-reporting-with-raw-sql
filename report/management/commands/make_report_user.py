# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
from django.core.management.base import BaseCommand

from report.reports import REPORT_PASSWORD, REPORT_USERNAME, grant_user_access_to_reports, make_user_if_not_exists


class Command(BaseCommand):
    help = f"Create PostgreSQL user {REPORT_USERNAME!r} with read-only access to reports"

    def handle(self, *args, **options):
        make_user_if_not_exists(REPORT_USERNAME, REPORT_PASSWORD)
        grant_user_access_to_reports(REPORT_USERNAME)
        self.stdout.write(self.style.SUCCESS(f"Successfully created report user {REPORT_USERNAME!r}."))
