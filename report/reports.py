# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
# Copyright (C) 2023-2025 by Siisurit e.U., Austria. All rights reserved.
import logging
import os
from typing import IO

from django.core.management.base import OutputWrapper
from django.db import connection

from minitrack.settings import DEFAULT_PASSWORD
from report.sql_tools import (
    checked_sql_name,
    run_report_ddl,
)

PUBLIC_SCHEMA = "public"
REPORT_SCHEMA = "report"

# Report user
REPORT_USERNAME = os.environ.get("MT_REPORT_USERNAME", "report")
REPORT_PASSWORD = os.environ.get("MT_REPORT_PASSWORD", DEFAULT_PASSWORD)

_log = logging.getLogger(__name__)


def output_info(output: IO | OutputWrapper | None, message: str):
    """
    Write an info message to ``output``. If ``output`` is ``None``, log an info message.
    """
    if output is None:
        _log.info(message)
    else:
        output.write(message + "\n")


def make_user_if_not_exists(username: str, password: str, output: IO | OutputWrapper | None = None):
    output_info(output, f"creating user {username!r} (if not exists yet)")
    checked_sql_name("username", username)
    run_report_ddl(
        "create_user_if_not_exists",
        parameters={"password": password, "username": username},
        variables={"username": username},
    )


def grant_user_access_to_reports(username: str, output: IO | OutputWrapper | None = None):
    output_info(output, f"granting user {username!r} access to reports")
    database_name = connection.settings_dict["NAME"]
    run_report_ddl(
        "grant_user_access_to_reports",
        variables={
            "database": checked_sql_name("database", database_name),
            "username": checked_sql_name("username", username),
        },
    )


def make_reports(output: IO | OutputWrapper | None = None):
    make_report_schema(output)
    make_report_views(output)


def make_report_schema(output: IO | OutputWrapper | None = None):
    output_info(output, "creating report schema")
    run_report_ddl("create_schema")


def make_report_views(output: IO | OutputWrapper | None = None):
    for view_name in [
        "user",
        "issue",  # Depends on view "user".
        "issue_labels",
        "issue_kind_missing",
        "issue_kind_multiples",
        "issue_kind_unique",
    ]:
        output_info(output, f"creating report view: {view_name}")
        base_name = f"create_view_{view_name}"
        run_report_ddl(base_name)


def clear_reports(output: IO | OutputWrapper | None = None):
    drop_report_views(output)


def drop_report_views(output: IO | OutputWrapper | None = None):
    output_info(output, "dropping report views")
    run_report_ddl("drop_views")
