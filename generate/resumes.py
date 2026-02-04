# Copyright (c) RenChu Wang - All Rights Reserved

import dataclasses as dcls
from collections.abc import Iterable
from datetime import date as Date

import rich
import typer
from jinja2 import Environment, FileSystemLoader, Template

from . import files

__all__ = ["Section", "resume"]

NAME = "Ren-Chu Wang"
"My name in the resume."


@dcls.dataclass
class Section:
    name: str
    body: str

    @property
    def title(self):
        return self.name.upper()


def resume(sections: Iterable[Section]):
    return files.get_template("resume").render(
        name=NAME,
        build_date=Date.today().strftime("%B %d, %Y"),
        sections=sections,
    )
