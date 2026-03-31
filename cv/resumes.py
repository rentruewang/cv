# Copyright (c) RenChu Wang - All Rights Reserved

import datetime
import subprocess as sp
from collections import abc as cabc

from . import files, sections

__all__ = ["resume"]

NAME = "Ren-Chu Wang"
"My name in the resume."


def resume(sections: cabc.Iterable[sections.Section]) -> str:
    today = datetime.date.today().strftime("%b %d, %Y")
    sha = git_sha()
    return files.get_template("resume").render(
        name=NAME,
        today=today,
        build=sha,
        sections=sections,
    )


def git_sha() -> str:
    return sp.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
