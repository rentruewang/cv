# Copyright (c) RenChu Wang - All Rights Reserved

import shutil

import fire
import rich

from . import Section, files, resumes

SECTIONS = [
    "contacts",
    "positions",
    "educations",
    "projects",
    "skills",
]


def main():
    files.BUILD.mkdir(exist_ok=True)
    (files.BUILD / ".gitignore").write_text("*")
    generate_one(True, "alt.html")
    generate_one(False, "index.html")
    shutil.copy2(files.TEMPLATE / "resume.css", files.BUILD)


def generate_one(hide: bool, output: str) -> None:
    out = resumes.resume(Section(sec, hide=hide) for sec in SECTIONS)

    # Write output.
    output_and_print(out, output)


def output_and_print(out: str, output: str) -> None:
    with (files.BUILD / output).open("w+") as f:
        print(out, file=f)

    rich.print(out)


if __name__ == "__main__":
    fire.Fire(main)
