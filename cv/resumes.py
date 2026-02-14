# Copyright (c) RenChu Wang - All Rights Reserved

import subprocess as sp
from collections.abc import Iterable, Sequence
from datetime import date as Date

from . import files
from .sections import SectionContent

__all__ = ["resume"]

NAME = "Ren-Chu Wang"
"My name in the resume."


def resume(sections: Iterable[SectionContent]) -> str:
    today = Date.today().strftime("%b %d, %Y")
    sha = git_sha()
    return files.get_template("resume").render(
        name=NAME,
        today=today,
        build=sha,
        sections=sections,
    )


def git_sha() -> str:
    return sp.check_output(["git", "rev-parse", "--short", "HEAD"]).decode().strip()
