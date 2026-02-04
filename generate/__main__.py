# Copyright (c) RenChu Wang - All Rights Reserved


import rich
import typer

from . import contacts, educations, files, positions, projects, resumes, skills


def main() -> None:
    sections = [
        contacts.contacts(),
        educations.educations(),
        positions.positions(),
        projects.projects(),
        skills.skills(),
    ]

    out = resumes.resume(sections)

    # Write output.
    output_and_print(out)


def output_and_print(out: str) -> None:
    files.BUILD.mkdir(exist_ok=True)
    with (files.BUILD / "index.html").open("w+") as f:
        print(out, file=f)
    _ = (files.SOURCE / "resume.css").copy_into(files.BUILD)

    rich.print(out)


if __name__ == "__main__":
    typer.run(main)
