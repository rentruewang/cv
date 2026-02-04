# Copyright (c) RenChu Wang - All Rights Reserved

from datetime import date as Date
from pathlib import Path

import rich
import typer
from jinja2 import Environment, FileSystemLoader, Template

from . import contacts, educations, positions, projects, skills

NAME = "Ren-Chu Wang"
"My name in the resume."

ROOT = Path(__file__).parent.parent
"Project root."

SOURCE = ROOT / "templates"
"The source directory."

BUILD = ROOT / "build"
"The build directory."


def main_template() -> Template:
    env = Environment(loader=FileSystemLoader(SOURCE))
    return env.get_template("resume.html.j2")


def main() -> None:
    out = main_template().render(
        name=NAME,
        build_date=Date.today().strftime("%B %d, %Y"),
        contacts=contacts.contacts(),
        skills=skills.skills(),
        educations=educations.educations(),
        positions=positions.positions(),
        projects=projects.projects(),
    )

    # Write output.
    output_and_print(out)


def output_and_print(out: str) -> None:
    BUILD.mkdir(exist_ok=True)
    with (BUILD / "index.html").open("w+") as f:
        print(out, file=f)
    _ = (SOURCE / "resume.css").copy_into(BUILD)

    rich.print(out)


if __name__ == "__main__":
    typer.run(main)
