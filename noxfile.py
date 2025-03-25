import os
import typing as t

import nox
from nox import options

PATH_TO_PROJECT = os.path.join(".", "src")
SCRIPT_PATHS = [PATH_TO_PROJECT, "noxfile.py"]
SQLC_CONFIG = "sqlc.yaml"

options.default_venv_backend = "uv"
options.sessions = ["format", "pyright"]


# uv_sync taken from: https://github.com/hikari-py/hikari/blob/master/pipelines/nox.py#L48
#
# Copyright (c) 2020 Nekokatt
# Copyright (c) 2021-present davfsa
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
def uv_sync(
    session: nox.Session, /, *, include_self: bool = False, extras: t.Sequence[str] = (), groups: t.Sequence[str] = ()
) -> None:
    if extras and not include_self:
        raise RuntimeError("When specifying extras, set `include_self=True`.")

    args: list[str] = []
    for extra in extras:
        args.extend(("--extra", extra))

    group_flag = "--group" if include_self else "--only-group"
    for group in groups:
        args.extend((group_flag, group))

    session.run_install(
        "uv", "sync", "--frozen", *args, silent=True, env={"UV_PROJECT_ENVIRONMENT": session.virtualenv.location}
    )


@nox.session()
def format(session: nox.Session) -> None:
    uv_sync(session, groups=["dev"])
    session.run("python", "-m", "ruff", "format", *SCRIPT_PATHS)
    session.run("python", "-m", "ruff", "check", *SCRIPT_PATHS, "--fix")


@nox.session()
def format_check(session: nox.Session) -> None:
    uv_sync(session, groups=["dev"])
    session.run("python", "-m", "ruff", "format", *SCRIPT_PATHS, "--check")
    session.run("python", "-m", "ruff", "check", *SCRIPT_PATHS)


@nox.session()
def pyright(session: nox.Session) -> None:
    uv_sync(session, include_self=True, groups=["dev"])
    session.run("pyright", *SCRIPT_PATHS)

@nox.session()
def sqlc(session: nox.Session) -> None:
    """Run sqlc to generate queries and dataclasses"""
    # note: this required sqlc to be installed on the system.
    # https://docs.sqlc.dev/en/latest/overview/install.html
    session.run("sqlc generate", "-f", SQLC_CONFIG)



