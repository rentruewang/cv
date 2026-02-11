# Copyright (c) RenChu Wang - All Rights Reserved

import subprocess as sp
from collections.abc import Iterable
from datetime import date as Date

from . import files
from .sections import Section

__all__ = ["resume"]

NAME = "Ren-Chu Wang"
"My name in the resume."


def resume(sections: Iterable[Section]) -> str:
    today = Date.today().strftime("%B %d, %Y")
    sha = git_sha()
    return files.get_template("resume").render(
        name=NAME,
        build=f"{today} <br> Build: {sha}",
        sections=sections,
    )


def git_sha() -> str:
    return sp.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
