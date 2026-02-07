# Copyright (c) RenChu Wang - All Rights Reserved

from collections.abc import Iterable
from datetime import date as Date

from . import files
from .sections import Section

__all__ = ["Section", "resume"]

NAME = "Ren-Chu Wang"
"My name in the resume."


def resume(sections: Iterable[Section]):
    return files.get_template("resume").render(
        name=NAME,
        build_date=Date.today().strftime("%B %d, %Y"),
        sections=sections,
    )
