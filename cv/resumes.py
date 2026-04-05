# Copyright (c) RenChu Wang - All Rights Reserved

import datetime
import subprocess as sp
from collections import abc as cabc

from .files import get_template
from .sections import Section

__all__ = ["resume"]

NAME = "Ren-Chu Wang"
"My name in the resume."


def resume(sections: cabc.Iterable[Section]) -> str:
    today = datetime.date.today().strftime("%b %d, %Y")
    sha = git_sha()
    return get_template("resume").render(
        name=NAME,
        today=today,
        build=sha,
        sections=sections,
    )


def git_sha() -> str:
    return sp.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
