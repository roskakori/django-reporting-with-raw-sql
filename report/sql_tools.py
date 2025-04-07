# Copyright (c) 2025 Thomas Aglassinger. Distributed under the MIT license.
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

from django.db import connection, transaction

_VALID_SQL_NAME_REGEX = re.compile(r"^[a-zA-Z0-9_\-.]+$")
_DDL_FOLDER = Path(__file__).parent / "ddls"
_COLON_NAME_REGEX = re.compile(r"[^:]:(\w+)")
_VARIABLE_PREFIX = "${"
_VARIABLE_SUFFIX = "}"


def checked_sql_name(name: str, value: str, allow_empty: bool = False) -> str:
    if value in (None, ""):
        if not allow_empty:
            raise ValueError(f"SQL name for {name} must be specified")
    elif not _VALID_SQL_NAME_REGEX.match(value):
        raise ValueError(
            f"SQL name for {name} is {value!r} but must only contain "
            f"alphanumeric characters, dashes, underscores, or dots."
        )
    return value


@lru_cache(maxsize=128)
def percent_from_colon_parameters(sql: str) -> str:
    """Convert :parameter to %(parameter)s format."""
    # FIXME Properly treat quotes and escapes, possibly by using Pygments as parser.
    #  However, for the time being all actual SQL statements processed through this
    #  do not need that.
    return _COLON_NAME_REGEX.sub(r"%(\1)s", sql)


def run_report_ddl(
    base_name: str, parameters: dict[str, Any | None] | None = None, variables: dict[str, Any | None] | None = None
):
    ddl_source_code = _ddl_source_code(base_name)
    run_report_ddl_source_code(ddl_source_code, parameters, variables)


def check_parameters_and_variables(
    parameters: dict[str, Any | None] | None = None, variables: dict[str, Any | None] | None = None
):
    def check_value(kind: str, name: str, value: str, *, allow_any_type: bool = False) -> bool:
        if value is None:
            pass
        elif isinstance(value, str):
            if "${" in value:
                raise ValueError(f"{kind} {name} is {value!r} but must not contain {_VARIABLE_PREFIX!r}")
        elif not allow_any_type:
            raise ValueError(f"{kind} {name} is {value!r} but must be a string")

    if variables is not None:
        if parameters is not None:
            for parameter_name, parameter_value in parameters.items():
                check_value("Parameter", parameter_name, parameter_value, allow_any_type=True)
        for variable_name, variable_value in variables.items():
            check_value("Variable", variable_name, variable_value)
            checked_sql_name(variable_name, variable_value)


def replaced_variables(text: str, variables: dict[str, Any | None] | None = None) -> str:
    result = text
    if variables is not None:
        for variable_name, variable_value in variables.items():
            result = result.replace(f"{_VARIABLE_PREFIX}{variable_name}{_VARIABLE_SUFFIX}", variable_value)
    return result


def run_report_ddl_source_code(
    ddl_source_code: str,
    parameters: dict[str, Any | None] | None = None,
    variables: dict[str, Any | None] | None = None,
):
    actual_ddl_source_code = replaced_variables(ddl_source_code, variables)
    with transaction.atomic(), connection.cursor() as cursor:
        cursor.execute(actual_ddl_source_code, params=parameters)


def _ddl_source_code(base_name: str) -> str:
    ddl_source_path = _DDL_FOLDER / f"{base_name}.sql"
    return percent_from_colon_parameters(ddl_source_path.read_text())


def has_user(username: str) -> bool:
    sql = """
        select exists (
            select
                1
            from
                pg_catalog.pg_user
            where
                usename = %(username)s
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, params={"username": username})
        result = cursor.fetchone()
    return result[0]


def has_report_view(view_name: str) -> bool:
    sql = """
        select exists (
            select
                1
            from
                pg_catalog.pg_views
            where
                schemaname = 'report'
                and viewname = %(view_name)s
        )
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, {"view_name": view_name})
        result = cursor.fetchone()
    return result[0]
